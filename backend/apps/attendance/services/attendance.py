from django.core.exceptions import ValidationError
from django.db import transaction
from apps.attendance.models import Attendance
from apps.students.models import Student
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
    def _get_attendance(cls, attendance_id: int) -> Attendance:
        """
        Retrieve attendance by ID.
        """

        try:
            return (
                Attendance.objects
                .select_related(
                    "student__user",
                    "teacher__user",
                    "subject__course__department",
                )
                .get(id=attendance_id)
            )
        except Attendance.DoesNotExist:
                raise ValidationError(
            {
                "attendance": "Attendance record does not exist."
            }
        )

    @classmethod
    def _validate_teacher(cls, teacher_id: int) -> Teacher:
        """
        Validate teacher.
        """

        try:
            teacher = Teacher.objects.prefetch_related(
                "subjects"
            ).get(id=teacher_id)

        except Teacher.DoesNotExist:
            raise ValidationError(
                {
                    "teacher": "Teacher does not exist."
                }
            )

        if not teacher.is_active:
            raise ValidationError(
                "Teacher account is inactive."
            )

        return teacher
    @classmethod
    def _validate_student(cls, student_id: int) -> Student:
        """
        Validate student.
        """

        try:
            student = Student.objects.select_related(
                "department",
                "user",
            ).get(id=student_id)

        except Student.DoesNotExist:
            raise ValidationError(
                {
                    "student": "Student does not exist."
                }
            )

        if not student.is_active:
            raise ValidationError(
                "Student account is inactive."
            )

        return student
    @classmethod
    def _validate_subject(cls, subject_id: int) -> Subject:
        """
        Validate subject.
        """

        try:
            subject = Subject.objects.select_related(
                "course__department"
            ).get(id=subject_id)

        except Subject.DoesNotExist:
            raise ValidationError(
                {
                    "subject": "Subject does not exist."
                }
            )
        if not subject.is_active:
            raise ValidationError(
                "Subject is inactive."
            )
        return subject

    @classmethod
    def _validate_teacher_subject(
        cls,
        teacher: Teacher,
        subject: Subject,
    ) -> None:
        """
        Ensure teacher is assigned
        to the given subject.
        """

        if not teacher.subjects.filter(
            id=subject.id
        ).exists():

            raise ValidationError(
                "Teacher is not assigned to this subject."
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
        if teacher.department_id != student.department_id:

            raise ValidationError(
                "Teacher cannot mark attendance for students from another department."
            )
    @classmethod
    def _check_duplicate_attendance(
        cls,
        student: Student,
        subject: Subject,
        attendance_date,
    ) -> None:
        """
        Prevent duplicate attendance.
        """
        attendance_exists = Attendance.objects.filter(
            student=student,
            subject=subject,
            attendance_date=attendance_date,
        ).exists()

        if attendance_exists:

            raise ValidationError(
                "Attendance has already been marked for this student."
            )
    # =====================================================
    # Bussiness Logic methods
    # =====================================================
        @classmethod
        @transaction.atomic
        def create_attendance(
            cls,
            validated_data: dict,
        ) -> Attendance:
            """
            Create a new attendance record.

            Args:
                validated_data:
                    Validated serializer data.

            Returns:
                Attendance:
                    Newly created attendance record.
            """

            # Extract validated data
            teacher_id = validated_data["teacher"].id
            student_id = validated_data["student"].id
            subject_id = validated_data["subject"].id

            attendance_date = validated_data["attendance_date"]
            status = validated_data["status"]
            remarks = validated_data.get("remarks")

            # Validate related objects
            teacher = cls._validate_teacher(
                teacher_id,
            )

            student = cls._validate_student(
                student_id,
            )

            subject = cls._validate_subject(
                subject_id,
            )

            # Validate business rules
            cls._validate_teacher_subject(
                teacher=teacher,
                subject=subject,
            )

            cls._validate_teacher_department(
                teacher=teacher,
                student=student,
            )

            cls._check_duplicate_attendance(
                student=student,
                subject=subject,
                attendance_date=attendance_date,
            )

            # Create attendance record
            attendance = Attendance.objects.create(
                teacher=teacher,
                student=student,
                subject=subject,
                attendance_date=attendance_date,
                status=status,
                remarks=remarks,
            )

            return attendance
    @classmethod
    def get_attendance_by_id(cls, attendance_id: int) -> Attendance:
        """
        Retrieve a single attendance record by its ID.
        """
        return cls._get_attendance(attendance_id)
    @classmethod
    def list_attendance(cls) -> QuerySet[Attendance]:
        """
        Retrieve all attendance records.
        """
        return (
            Attendance.objects
            .select_related(
                "student__user",
                "student__department",
                "teacher__user",
                "teacher__department",
                "subject__course__department",
            )
            .all()
        )
    @classmethod
    @transaction.atomic
    def update_attendance(
        cls,
        attendance_id: int,
        validated_data: dict,
    ) -> Attendance:
        """
        Update an existing attendance record.
        """

        attendance = cls._get_attendance(attendance_id)

        attendance.status = validated_data["status"]
        attendance.remarks = validated_data.get("remarks")

        attendance.save(
            update_fields=[
                "status",
                "remarks",
                "updated_at",
            ]
        )

        return attendance