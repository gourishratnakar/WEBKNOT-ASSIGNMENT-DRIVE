# Campus Event Management Platform - Design Document

 1. Project Overview

This document outlines the design and implementation of a Campus Event Management Platform backend system for Webknot Technologies. The system enables college administrators to manage events and students to register, attend, and provide feedback.

 2. Assumptions and Decisions

 2.1 Key Assumptions
- Scale: 50 colleges, 500 students each, 20 events per semester
- Event IDs: Unique across the entire platform (global scope)
- Data Architecture: Single unified database for all colleges (easier analytics and management)
- User Roles: Admin (event creation) and Student (registration/feedback)
- Event Types: Workshop, Hackathon, TechTalk, Fest, Seminar

 2.2 Design Decisions
- Database: SQLite for prototype (easily scalable to PostgreSQL/MySQL)
- Architecture: RESTful API backend with JSON responses
- Framework: Flask with SQLAlchemy ORM for rapid development
- Data Integrity: Foreign key constraints and validation rules
- Attendance Logic: Only registered students can have attendance marked
- Feedback Logic: Only students who attended can provide feedback

 3. Database Schema Design

 3.1 Tables Overview
1. College - Institution details
2. Student - Student information linked to colleges
3. Event - Event details created by admins
4. Registration - Student-Event registrations
5. Attendance - Attendance tracking for registrations
6. Feedback - Student feedback with ratings

 3.2 Detailed Schema

 College Table
- id (PK) - Auto-increment primary key
- name - College name (VARCHAR 100)
- code - Unique college code (VARCHAR 10)
- created_at - Timestamp

 Student Table
- id (PK) - Auto-increment primary key
- student_id - Unique student identifier (VARCHAR 20)
- name - Student full name (VARCHAR 100)
- email - Unique email address (VARCHAR 120)
- college_id (FK) - References College.id
- created_at - Timestamp

 Event Table
- id (PK) - Auto-increment primary key
- title - Event title (VARCHAR 200)
- description - Event details (TEXT)
- event_type - Category: Workshop/Hackathon/TechTalk/Fest
- date - Event date
- time - Event start time
- venue - Event location (VARCHAR 100)
- max_participants - Capacity limit (INTEGER)
- college_id (FK) - References College.id
- created_by - Admin name (VARCHAR 100)
- created_at - Timestamp
- is_active - Boolean flag for active events

 Registration Table
- id (PK) - Auto-increment primary key
- student_id (FK) - References Student.id
- event_id (FK) - References Event.id
- registered_at - Registration timestamp
- is_cancelled - Boolean flag for cancellations
- UNIQUE(student_id, event_id) - Prevent duplicate registrations

 Attendance Table
- id (PK) - Auto-increment primary key
- registration_id (FK) - References Registration.id
- marked_at - Attendance timestamp
- marked_by - Admin who marked attendance (VARCHAR 100)

 Feedback Table
- id (PK) - Auto-increment primary key
- registration_id (FK) - References Registration.id
- rating - 1-5 star rating (INTEGER with CHECK constraint)
- comment - Optional text feedback (TEXT)
- submitted_at - Feedback timestamp

 3.3 Relationships
- College → Student (One-to-Many)
- College → Event (One-to-Many)
- Student → Registration (One-to-Many)
- Event → Registration (One-to-Many)
- Registration → Attendance (One-to-One)
- Registration → Feedback (One-to-One)

 4. API Design

 4.1 Base URL
`http://localhost:5000/api`

 4.2 Endpoints

 College Management
- `GET /colleges` - List all colleges
- `POST /colleges` - Create new college
  - Body: `{"name": "College Name", "code": "CODE"}`

 Student Management
- `GET /students` - List students (optional: ?college_id=X)
- `POST /students` - Register new student
  - Body: `{"student_id": "ID", "name": "Name", "email": "email", "college_id": 1}`

 Event Management
- `GET /events` - List events (optional: ?college_id=X&event_type=Workshop)
- `POST /events` - Create new event
  - Body: `{"title": "Event", "event_type": "Workshop", "date": "2024-10-15", "time": "10:00", "venue": "Hall", "college_id": 1, "created_by": "Admin"}`

 Registration System
- `POST /register` - Register student for event
  - Body: `{"student_id": 1, "event_id": 1}`
- `GET /registrations` - View registrations (optional: ?event_id=X&student_id=Y)

 Attendance System
- `POST /attendance` - Mark attendance
  - Body: `{"registration_id": 1, "marked_by": "Admin"}`
- `GET /attendance` - View attendance records

 Feedback System
- `POST /feedback` - Submit feedback
  - Body: `{"registration_id": 1, "rating": 5, "comment": "Great event!"}`

 Reporting System
- `GET /reports/events` - Event popularity and analytics
- `GET /reports/students` - Student participation analytics
- `GET /reports/top-students` - Top 3 most active students

 5. Workflows

 5.1 Student Registration Workflow
1. Student selects event from available events
2. System validates:
   - Event is active and not full
   - Student not already registered
   - Student exists in system
3. Creates registration record
4. Returns confirmation

 5.2 Attendance Workflow
1. Admin accesses attendance marking interface
2. System shows list of registered students for event
3. Admin marks attendance for present students
4. System creates attendance records
5. Updates attendance statistics

 5.3 Feedback Workflow
1. Student attends event (attendance marked)
2. System enables feedback submission
3. Student provides 1-5 rating and optional comment
4. System validates and stores feedback
5. Updates event rating analytics

 6. Edge Cases and Validations

 6.1 Registration Edge Cases
- Duplicate Registration: Prevented by unique constraint
- Event Capacity: Checked before allowing registration
- Inactive Events: Only active events allow registration
- Cross-College Registration: Allowed for inter-college events

 6.2 Attendance Edge Cases
- No Registration: Attendance only for registered students
- Duplicate Attendance: Prevented by one-to-one relationship
- Late Registration: Cannot mark attendance without registration

 6.3 Feedback Edge Cases
- No Attendance: Feedback only from students who attended
- Duplicate Feedback: Prevented by one-to-one relationship
- Invalid Ratings: CHECK constraint ensures 1-5 range

 7. Technology Stack Rationale

 7.1 Backend Choice: Flask
- Pros: Lightweight, flexible, rapid prototyping
- Alternative: Django (more features but heavier)

 7.2 Database Choice: SQLite → PostgreSQL
- Development: SQLite for simplicity
- Production: PostgreSQL for scalability

 7.3 ORM Choice: SQLAlchemy
- Pros: Database abstraction, relationship handling
- Alternative: Raw SQL (more control, less abstraction)

 8. Testing Strategy

 8.1 Integration Testing
- End-to-end workflow testing
- Database relationship verification
- API chain testing (register → attend → feedback)
- Report accuracy validation

 Conclusion

This design provides a solid foundation for a scalable Campus Event Management Platform. The unified database approach enables comprehensive analytics while maintaining simplicity.