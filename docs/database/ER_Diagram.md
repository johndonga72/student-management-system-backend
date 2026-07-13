# Entity Relationship (ER) Diagram

---

## Document Information

| Field | Details |
|--------|---------|
| Project Name | Student Management System Backend |
| Document Type | Entity Relationship Diagram |
| Version | 1.0 |
| Prepared By | Backend Development Team |
| Database | PostgreSQL |
| ORM | Django ORM |
| Status | Design Phase |
| Date | 12 July 2026 |

---

# Table of Contents

1. Introduction
2. Purpose
3. Entity Overview
4. Relationship Summary
5. Entity Relationships
6. Cardinality
7. Business Rules
8. ER Diagram
9. Django Model Mapping
10. Future Enhancements
11. Conclusion

---

# 1. Introduction

The Entity Relationship (ER) Diagram provides a conceptual representation of the database structure for the Student Management System Backend. It illustrates how the core entities interact with one another and defines the relationships that maintain data consistency.

This document serves as the foundation for implementing Django models and database migrations.

---

# 2. Purpose

The ER Diagram is intended to:

- Identify the core entities of the system.
- Define relationships between entities.
- Establish primary and foreign key relationships.
- Reduce data redundancy.
- Support scalable database design.

---

# 3. Entity Overview

The following entities are included in Version 1.0 of the system:

| Entity | Description |
|----------|-------------|
| User | Authentication and authorization |
| Student | Student profile and academic information |
| Teacher | Teacher profile |
| Department | Academic departments |
| Course | Courses offered by departments |
| Subject | Subjects within a course |
| Attendance | Student attendance records |
| Examination | Examination information |
| Result | Examination results |

---

# 4. Relationship Summary

| Parent Entity | Child Entity | Relationship |
|---------------|--------------|--------------|
| Department | Student | One-to-Many |
| Department | Teacher | One-to-Many |
| Department | Course | One-to-Many |
| Course | Subject | One-to-Many |
| Teacher | Subject | One-to-Many |
| Student | Attendance | One-to-Many |
| Student | Result | One-to-Many |
| Examination | Result | One-to-Many |
| Subject | Result | One-to-Many |

---

# 5. Entity Relationships

## Department → Student

One department can have many students.

Each student belongs to one department.

---

## Department → Teacher

One department can have many teachers.

Each teacher belongs to one department.

---

## Department → Course

One department offers multiple courses.

Each course belongs to one department.

---

## Course → Subject

Each course contains multiple subjects.

Each subject belongs to one course.

---

## Teacher → Subject

A teacher may teach multiple subjects.

Each subject is assigned to one teacher.

---

## Student → Attendance

Each student can have multiple attendance records.

Every attendance record belongs to one student.

---

## Student → Result

Each student can have multiple examination results.

Every result belongs to one student.

---

## Examination → Result

One examination produces many student results.

Each result is associated with one examination.

---

## Subject → Result

Each subject has multiple result entries.

Every result belongs to one subject.

---

# 6. Cardinality

| Relationship | Cardinality |
|--------------|-------------|
| Department → Student | 1 : N |
| Department → Teacher | 1 : N |
| Department → Course | 1 : N |
| Course → Subject | 1 : N |
| Teacher → Subject | 1 : N |
| Student → Attendance | 1 : N |
| Student → Result | 1 : N |
| Examination → Result | 1 : N |
| Subject → Result | 1 : N |

---

# 7. Business Rules

- Every student must belong to one department.
- Every teacher must belong to one department.
- Every course belongs to one department.
- Every subject belongs to one course.
- Every subject is assigned to a teacher.
- Attendance cannot exist without a valid student.
- Results cannot exist without a valid student, examination, and subject.
- Primary and foreign key constraints enforce referential integrity.

---

# 8. ER Diagram

The ER diagram is stored separately as an image.

**Location:**

```text
docs/
└── diagrams/
    └── database/
        └── er_diagram.png
```

The diagram illustrates:

- Entities
- Attributes
- Primary Keys
- Foreign Keys
- Relationship cardinality

---

# 9. Django Model Mapping

| Entity | Django Model |
|----------|--------------|
| User | User |
| Student | Student |
| Teacher | Teacher |
| Department | Department |
| Course | Course |
| Subject | Subject |
| Attendance | Attendance |
| Examination | Examination |
| Result | Result |

Each entity will be implemented as a Django model using appropriate field types and relationships (`ForeignKey`, `OneToOneField`, or `ManyToManyField` where required).

---

# 10. Future Enhancements

Future entities may include:

- Parent
- Fee
- Library
- Hostel
- Timetable
- Notification
- Audit Log
- File Attachment

The database design is modular and allows these entities to be added without significant structural changes.

---

# 11. Conclusion

The ER Diagram defines the conceptual data model for the Student Management System Backend. It establishes clear relationships between entities and provides the foundation for implementing Django models using PostgreSQL and Django ORM. This document will guide database migration, application development, and future system enhancements.