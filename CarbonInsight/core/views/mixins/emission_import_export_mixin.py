from io import BytesIO
from typing import TypeVar, Type

from django.core.validators import FileExtensionValidator
from django.http import FileResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, inline_serializer
from import_export.results import RowResult
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, UnsupportedMediaType
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from tablib import Dataset

from core.permissions import ProductPermission
from core.resources.emission_resources import EmissionResource


T = TypeVar('T', bound=ModelViewSet)

class EmissionImportExportMixin:
    """
    Provides generalized methods for import and export of emissions for supported filetypes to avoid duplicate code.
     Provides export methods for .csv and .xlsx as well as an import method that parses .csv, .xls and .xlsx
    """

    emission_import_export_resource:Type[EmissionResource] = None

    @action(detail=False, methods=["get"],url_path="export/csv")
    def export_csv(self:T, request, *args, **kwargs):
        """
        Facilitates export of emissions for .csv file type.

        Args:
            request: request that arrives at the server that contains parameters
        Returns:
            .csv file
        """

        # Check if template is requested
        if request.query_params.get("template", "false").lower() == "true":
            queryset = self.get_queryset()[:0]  # Empty queryset for template
        else:
            queryset = self.get_queryset()
        dataset = self.emission_import_export_resource().export(queryset=queryset)
        csv_bytes = dataset.csv.encode("utf-8")
        file_io = BytesIO(csv_bytes)

        return FileResponse(
            file_io,
            as_attachment=True,
            filename=f"{self.get_parent_company().name}_transport_emissions.csv",
            content_type="text/csv",
        )

    @action(detail=False, methods=["get"],url_path="export/xlsx")
    def export_xlsx(self:T, request, *args, **kwargs):
        """
        Facilitates export of emissions for .xlsx file type.

        Args:
            request: request that arrives at the server that contains parameters
        Returns:
            .xlsx file
        """

        # Check if template is requested
        if request.query_params.get("template", "false").lower() == "true":
            queryset = self.get_queryset()[:0]  # Empty queryset for template
        else:
            queryset = self.get_queryset()
        dataset = self.emission_import_export_resource().export(queryset=queryset)
        result = dataset.export(format="xlsx")
        file_io = BytesIO(result)

        return FileResponse(
            file_io,
            as_attachment=True,
            filename=f"{self.get_parent_company().name}_products.xlsx",
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    @action(
        detail=False,
        methods=["post"],
        parser_classes=[MultiPartParser],
        permission_classes=[IsAuthenticated, ProductPermission],
        url_path="import/tabular",
        filter_backends=[]
    )
    def import_tabular(self:T, request, *args, **kwargs):
        """
        Facilitates import of emissions from .csv, .xls and .xlsx file types.

        Args:
            request: request that arrives at the server that contains parameters and the file
        Returns:
            HTTP 201 response
        Raises:
            ValidationError
        """

        if 'file' not in request.FILES or len(request.FILES) != 1:
            raise ValidationError({"file": "Please upload exactly one file under the 'file' key."})

        uploaded = request.FILES['file']

        # Validate extension
        allowed = ['csv', 'xls', 'xlsx']
        validator = FileExtensionValidator(allowed_extensions=allowed)
        try:
            validator(uploaded)
        except DjangoValidationError:
            raise UnsupportedMediaType("Invalid file extension. Only .csv, .xls, .xlsx are allowed.")

        # Read raw bytes and determine format
        name = uploaded.name
        ext = name.rsplit(".", 1)[1].lower()
        raw = uploaded.read()

        # Load into a Tablib Dataset
        if ext == 'csv':
            text = raw.decode('utf-8')
            dataset = Dataset().load(text, format='csv')
        else:
            fmt = 'xls' if ext == 'xls' else 'xlsx'
            dataset = Dataset().load(raw, format=fmt)

        # Perform import
        resource = self.emission_import_export_resource()
        result = resource.import_data(
            dataset,
            dry_run=False,
            product=self.get_parent_product(),
            retain_instance_in_row_result=True
        )

        # Success: serialize newly created products
        if not result.has_errors():
            created = []
            for row in result.rows:
                if row.import_type == RowResult.IMPORT_TYPE_NEW:
                    created.append(self.get_serializer(row.instance).data)
            return Response(created, status=status.HTTP_201_CREATED)

        # Failure: collect errors
        errors = []
        for err_row in result.error_rows:
            for err in err_row.errors:
                errors.append({
                    "row": err.row,
                    "error": repr(err.error),
                })
        raise ValidationError(errors)