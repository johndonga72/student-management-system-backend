from typing import Any
class AttendanceExcelValidator:
    """
    Validates the structure of an attendance Excel file.

    This class is responsible only for Excel-specific validation.
    Business validation is handled by serializers and services.
    """
    REQUIRED_COLUMNS = {
        "student_number",
        "employee_id",
        "subject_code",
        "attendance_date",
        "status",
    }

    OPTIONAL_COLUMNS = {
        "remarks",
    }

    ALLOWED_COLUMNS = REQUIRED_COLUMNS | OPTIONAL_COLUMNS

    @classmethod
    def validate_headers(
        cls,
        headers: list[str],
    ) -> None:
        """
        Validate the Excel column headers.

        Raises:
            ValueError: If the headers are invalid.
        """

        cls._validate_duplicate_headers(headers)
        cls._validate_empty_headers(headers)
        cls._validate_required_columns(headers)
        cls._validate_unknown_columns(headers)

    @classmethod
    def _validate_duplicate_headers(
        cls,
        headers: list[str],
    ) -> None:
        """
        Check for duplicate column names.
        """
        seen = set()
        duplicates = set()

        for header in headers:
            if header in seen:
                duplicates.add(header)

            seen.add(header)

        if duplicates:
            duplicate_columns = ", ".join(
                sorted(duplicates)
            )

            raise ValueError(
                f"Duplicate Excel columns found: "
                f"{duplicate_columns}."
            )

    @staticmethod
    def _validate_empty_headers(
        headers: list[str],
    ) -> None:
        """
        Check for empty column headers.
        """

        if "" in headers:
            raise ValueError(
                "Excel contains an empty column header."
            )

    @classmethod
    def _validate_required_columns(
        cls,
        headers: list[str],
    ) -> None:
        """
        Check that all required columns are present.
        """

        header_set = set(headers)

        missing_columns = (
            cls.REQUIRED_COLUMNS - header_set
        )

        if missing_columns:
            missing = ", ".join(
                sorted(missing_columns)
            )

            raise ValueError(
                f"Missing required Excel columns: {missing}."
            )

    @classmethod
    def _validate_unknown_columns(
        cls,
        headers: list[str],
    ) -> None:
        """
        Check for unsupported Excel columns.
        """

        unknown_columns = (
            set(headers) - cls.ALLOWED_COLUMNS
        )

        if unknown_columns:
            unknown = ", ".join(
                sorted(unknown_columns)
            )

            raise ValueError(
                f"Unknown Excel columns found: {unknown}."
            )