from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.attendance.models import Attendance
from apps.students.models import Student
from apps.students.models.choices import StudentStatus
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from django.db.models import QuerySet
from typing import Any

# Import your custom exceptions
# from apps.attendance.exceptions import AttendanceNotFoundException
# from apps.students.exceptions import StudentNotFoundException
# from apps.subjects.exceptions import SubjectNotFoundException
# from apps.teachers.exceptions import TeacherNotFoundException
class AttendanceService:
    """
    Service class for attendance business logic.
    """
    # =====================================================
    # Private Helper Methods
    # =====================================================

    @classmethod
    def _get_attendance(
        cls,
        tenant,
        attendance_id: int,
    ) -> Attendance:
        """
        Retrieve an attendance record within the tenant.
        """

        try:
            return (
                Attendance.objects
                .for_tenant(tenant)
                .select_related(
                    "student__user",
                    "teacher__user",
                    "subject__course__department",
                )
                .get(
                    id=attendance_id,
                )
            )

        except Attendance.DoesNotExist as exc:
            raise ValidationError(
                {
                    "attendance": (
                        "Attendance record does not exist."
                    ),
                }
            ) from exc

    @classmethod
    def _validate_teacher(
        cls,
        tenant,
        teacher_id: int,
    ) -> Teacher:
        """
        Validate a teacher within the current tenant.
        """

        try:
            teacher = (
                Teacher.objects
                .select_related(
                    "department",
                )
                .prefetch_related(
                    "subjects",
                )
                .get(
                    id=teacher_id,
                    tenant=tenant,
                    is_deleted=False,
                )
            )

        except Teacher.DoesNotExist as exc:
            raise ValidationError(
                {
                    "teacher": (
                        "Teacher does not exist."
                    ),
                }
            ) from exc

        if not teacher.is_active:
            raise ValidationError(
                {
                    "teacher": (
                        "Teacher account is inactive."
                    ),
                }
            )

        return teacher
    @classmethod
    def _validate_student(
        cls,
        tenant,
        student_id: int,
    ) -> Student:
        """
        Validate a student within the current tenant.
        """

        try:
            student = (
                Student.objects
                .select_related(
                    "department",
                    "user",
                )
                .get(
                    id=student_id,
                    tenant=tenant,
                    is_deleted=False,
                )
            )
        except Student.DoesNotExist as exc:
            raise ValidationError(
                {
                    "student": (
                        "Student does not exist."
                    ),
                }
            ) from exc

        if student.status != StudentStatus.APPROVED:
            raise ValidationError(
                {
                    "student": (
                        "Student account is not approved."
                    ),
                }
            )

        return student

    @classmethod
    def _validate_subject(
        cls,
        tenant,
        subject_id: int,
    ) -> Subject:
        """
        Validate a subject within the current tenant.
        """

        try:
            subject = (
                Subject.objects
                .select_related(
                    "course__department",
                )
                .get(
                    id=subject_id,
                    tenant=tenant,
                    is_deleted=False,
                )
            )

        except Subject.DoesNotExist as exc:
            raise ValidationError(
                {
                    "subject": (
                        "Subject does not exist."
                    ),
                }
            ) from exc

        if not subject.is_active:
            raise ValidationError(
                {
                    "subject": (
                        "Subject is inactive."
                    ),
                }
            )

        return subject

    @classmethod
    def _validate_teacher_subject(
        cls,
        teacher: Teacher,
        subject: Subject,
    ) -> None:
        """
        Ensure the teacher is assigned to the subject.
        """

        if not teacher.subjects.filter(
            id=subject.id,
        ).exists():
            raise ValidationError(
                {
                    "subject": (
                        "Teacher is not assigned "
                        "to this subject."
                    ),
                }
            )

    @classmethod
    def _validate_teacher_department(
        cls,
        teacher: Teacher,
        student: Student,
    ) -> None:
        """
        Ensure teacher and student belong
        to the same department.
        """

        if (
            teacher.department_id
            != student.department_id
        ):
            raise ValidationError(
                {
                    "department": (
                        "Teacher cannot mark attendance "
                        "for students from another department."
                    ),
                }
            )

    @classmethod
    def _check_duplicate_attendance(
        cls,
        tenant,
        student: Student,
        subject: Subject,
        attendance_date,
    ) -> None:
        """
        Prevent duplicate attendance within the tenant.
        """

        attendance_exists = (
            Attendance.objects
            .for_tenant(tenant)
            .filter(
                student=student,
                subject=subject,
                attendance_date=attendance_date,
            )
            .exists()
        )

        if attendance_exists:
            raise ValidationError(
                {
                    "attendance_date": (
                        "Attendance has already been marked "
                        "for this student for the selected subject "
                        "on this date."
                    ),
                }
            )
    @staticmethod
    def _validate_student_instance(
        student: Student,
    ) -> None:
        """
        Validate an already-resolved student.
        """

        if student.status != StudentStatus.APPROVED:
            raise ValidationError(
                {
                    "student_number": (
                        f"Student '{student.student_number}' "
                        "is not approved."
                    )
                }
            )
    @staticmethod
    def _validate_teacher_instance(
        teacher: Teacher,
    ) -> None:
        """
        Validate an already-resolved teacher.
        """

        if not teacher.is_active:
            raise ValidationError(
                {
                    "employee_id": (
                        f"Teacher '{teacher.employee_id}' "
                        "is inactive."
                    )
                }
            )
    @staticmethod
    def _validate_subject_instance(
        subject: Subject,
    ) -> None:
        """
        Validate an already-resolved subject.
        """

        if not subject.is_active:
            raise ValidationError(
                {
                    "subject_code": (
                        f"Subject '{subject.subject_code}' "
                        "is inactive."
                    )
                }
            )
    # =====================================================
    # Bussiness Logic methods
    # =====================================================
    @classmethod
    @transaction.atomic
    def create_attendance(
        cls,
        tenant,
        validated_data: dict,
    ) -> Attendance:
        """
        Create a new attendance record within the current tenant.

        Args:
            tenant:
                Current tenant resolved from the request.

            validated_data:
                Validated serializer data.

        Returns:
            Attendance:
                Newly created attendance record.
        """

        teacher = validated_data["teacher"]
        student = validated_data["student"]
        subject = validated_data["subject"]

        attendance_date = validated_data[
            "attendance_date"
        ]

        status = validated_data["status"]

        remarks = validated_data.get(
            "remarks",
            "",
        )

        # =====================================================
        # Validate Related Objects
        # =====================================================

        teacher = cls._validate_teacher(
            tenant=tenant,
            teacher_id=teacher.id,
        )

        student = cls._validate_student(
            tenant=tenant,
            student_id=student.id,
        )

        subject = cls._validate_subject(
            tenant=tenant,
            subject_id=subject.id,
        )

        # =====================================================
        # Validate Business Rules
        # =====================================================

        cls._validate_teacher_subject(
            teacher=teacher,
            subject=subject,
        )

        cls._validate_teacher_department(
            teacher=teacher,
            student=student,
        )

        cls._check_duplicate_attendance(
            tenant=tenant,
            student=student,
            subject=subject,
            attendance_date=attendance_date,
        )

        # =====================================================
        # Create Attendance
        # =====================================================

        attendance = Attendance.objects.create(
            tenant=tenant,
            teacher=teacher,
            student=student,
            subject=subject,
            attendance_date=attendance_date,
            status=status,
            remarks=remarks,
        )

        return attendance


    @classmethod
    def get_attendance_by_id(
        cls,
        tenant,
        attendance_id: int,
    ) -> Attendance:
        """
        Retrieve a single attendance record
        within the current tenant.
        """

        return cls._get_attendance(
            tenant=tenant,
            attendance_id=attendance_id,
        )


    @classmethod
    def list_attendance(
        cls,
        tenant,
    ) -> QuerySet[Attendance]:
        """
        Retrieve all attendance records
        belonging to the current tenant.
        """

        return (
            Attendance.objects
            .for_tenant(tenant)
            .select_related(
                "student__user",
                "student__department",
                "teacher__user",
                "teacher__department",
                "subject__course__department",
            )
            .order_by(
                "-attendance_date",
                "student",
            )
        )


    @classmethod
    @transaction.atomic
    def update_attendance(
        cls,
        tenant,
        attendance_id: int,
        validated_data: dict,
    ) -> Attendance:
        """
        Update an attendance record within
        the current tenant.
        """

        attendance = cls._get_attendance(
            tenant=tenant,
            attendance_id=attendance_id,
        )

        attendance.status = validated_data[
            "status"
        ]

        if "remarks" in validated_data:
            attendance.remarks = validated_data[
                "remarks"
            ]

        attendance.save(
            update_fields=[
                "status",
                "remarks",
                "updated_at",
            ],
        )

        return attendance
    @classmethod
    def validate_excel_rows(
        cls,
        tenant,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Resolve Excel identifiers and validate attendance rows.

        This method performs validation only.
        It does not create or update attendance records.
        """

        if not rows:
            raise ValidationError(
                {
                    "file": "Excel file contains no attendance records."
                }
            )

        student_numbers = {
            row.get("student_number")
            for row in rows
            if row.get("student_number")
        }

        employee_ids = {
            row.get("employee_id")
            for row in rows
            if row.get("employee_id")
        }

        subject_codes = {
            row.get("subject_code")
            for row in rows
            if row.get("subject_code")
        }

        students = (
            Student.objects
            .filter(
                tenant=tenant,
                is_deleted=False,
                student_number__in=student_numbers,
            )
            .select_related(
                "user",
                "department",
            )
        )

        teachers = (
            Teacher.objects
            .filter(
                tenant=tenant,
                is_deleted=False,
                employee_id__in=employee_ids,
            )
            .select_related(
                "user",
                "department",
            )
            .prefetch_related("subjects")
        )

        subjects = (
            Subject.objects
            .filter(
                tenant=tenant,
                is_deleted=False,
                subject_code__in=subject_codes,
            )
            .select_related(
                "course__department",
            )
        )

        student_map = {
            student.student_number: student
            for student in students
        }

        teacher_map = {
            teacher.employee_id: teacher
            for teacher in teachers
        }

        subject_map = {
            subject.subject_code: subject
            for subject in subjects
        }

        validated_rows = []
        errors = []

        for row_number, row in enumerate(rows, start=2):
            try:
                validated_row = cls._validate_excel_row(
                    tenant=tenant,
                    row=row,
                    row_number=row_number,
                    student_map=student_map,
                    teacher_map=teacher_map,
                    subject_map=subject_map,
                )

                validated_rows.append(validated_row)

            except ValidationError as exc:
                errors.append(
                    {
                        "row": row_number,
                        "errors": exc.detail,
                    }
                )

        if errors:
            raise ValidationError(
                {
                    "message": (
                        "Attendance Excel validation failed. "
                        "No records were imported."
                    ),
                    "errors": errors,
                }
            )

        return validated_rows
    @classmethod
    def _validate_excel_row(
        cls,
        tenant,
        row: dict[str, Any],
        row_number: int,
        student_map: dict[str, Student],
        teacher_map: dict[str, Teacher],
        subject_map: dict[str, Subject],
    ) -> dict[str, Any]:
        """
        Resolve identifiers and validate one Excel attendance row.
        """

        student_number = row.get("student_number")
        employee_id = row.get("employee_id")
        subject_code = row.get("subject_code")

        row_errors = {}

        student = student_map.get(student_number)

        if student is None:
            row_errors["student_number"] = (
                f"Student '{student_number}' does not exist "
                "for the current tenant."
            )

        teacher = teacher_map.get(employee_id)

        if teacher is None:
            row_errors["employee_id"] = (
                f"Teacher '{employee_id}' does not exist "
                "for the current tenant."
            )

        subject = subject_map.get(subject_code)

        if subject is None:
            row_errors["subject_code"] = (
                f"Subject '{subject_code}' does not exist "
                "for the current tenant."
            )

        if row_errors:
            raise ValidationError(row_errors)

        cls._validate_student_instance(student)

        cls._validate_teacher_instance(teacher)

        cls._validate_subject_instance(subject)

        cls._validate_teacher_subject(
            teacher=teacher,
            subject=subject,
        )

        cls._validate_teacher_department(
            teacher=teacher,
            student=student,
        )

        cls._check_duplicate_attendance(
            tenant=tenant,
            student=student,
            subject=subject,
            attendance_date=row["attendance_date"],
        )

        return {
            "student": student,
            "teacher": teacher,
            "subject": subject,
            "attendance_date": row["attendance_date"],
            "status": row["status"],
            "remarks": row.get("remarks") or "",
        }
    @classmethod
    @transaction.atomic
    def bulk_create_attendance(
        cls,
        tenant,
        validated_rows: list[dict[str, Any]],
    ) -> list[Attendance]:
        """
        Create multiple attendance records in a single database operation.

        The rows must already be validated before calling this method.
        """
        attendance_records = [
            Attendance(
                tenant=tenant,
                student=row["student"],
                teacher=row["teacher"],
                subject=row["subject"],
                attendance_date=row["attendance_date"],
                status=row["status"],
                remarks=row.get("remarks", ""),
            )
            for row in validated_rows
        ]

        if not attendance_records:
            return []

        return Attendance.objects.bulk_create(
            attendance_records,
        )