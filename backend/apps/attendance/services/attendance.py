from rest_framework.exceptions import ValidationError
from django.db import transaction
from apps.attendance.models import Attendance
from apps.students.models import Student
from apps.students.models.choices import StudentStatus
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from django.db.models import QuerySet
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
