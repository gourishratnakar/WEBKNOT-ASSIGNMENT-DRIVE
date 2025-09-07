# Let's recreate all the files in one go so they can be downloaded

print("🔄 RECREATING ALL 14 FILES FOR DOWNLOAD")
print("="*60)

# 1. app.py - Main Flask application
app_py_content = '''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat()
        }

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    college = db.relationship('College', backref=db.backref('students', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'college_id': self.college_id,
            'college_name': self.college.name,
            'created_at': self.created_at.isoformat()
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # Workshop, Hackathon, TechTalk, Fest
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, default=100)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    created_by = db.Column(db.String(100), nullable=False)  # Admin name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    college = db.relationship('College', backref=db.backref('events', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'event_type': self.event_type,
            'date': self.date.isoformat(),
            'time': self.time.isoformat(),
            'venue': self.venue,
            'max_participants': self.max_participants,
            'college_id': self.college_id,
            'college_name': self.college.name,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_cancelled = db.Column(db.Boolean, default=False)
    
    student = db.relationship('Student', backref=db.backref('registrations', lazy=True))
    event = db.relationship('Event', backref=db.backref('registrations', lazy=True))
    
    __table_args__ = (db.UniqueConstraint('student_id', 'event_id', name='unique_registration'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student.name,
            'event_id': self.event_id,
            'event_title': self.event.title,
            'registered_at': self.registered_at.isoformat(),
            'is_cancelled': self.is_cancelled
        }

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    marked_by = db.Column(db.String(100), nullable=False)  # Admin name
    
    registration = db.relationship('Registration', backref=db.backref('attendance', uselist=False, lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'student_name': self.registration.student.name,
            'event_title': self.registration.event.title,
            'marked_at': self.marked_at.isoformat(),
            'marked_by': self.marked_by
        }

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    registration = db.relationship('Registration', backref=db.backref('feedback', uselist=False, lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'student_name': self.registration.student.name,
            'event_title': self.registration.event.title,
            'rating': self.rating,
            'comment': self.comment,
            'submitted_at': self.submitted_at.isoformat()
        }

# API Routes

@app.route('/')
def index():
    return jsonify({
        'message': 'Campus Event Management Platform API',
        'version': '1.0',
        'endpoints': [
            'GET /api/colleges - List all colleges',
            'POST /api/colleges - Create college',
            'GET /api/students - List all students',
            'POST /api/students - Create student',
            'GET /api/events - List all events',
            'POST /api/events - Create event',
            'POST /api/register - Register student for event',
            'POST /api/attendance - Mark attendance',
            'POST /api/feedback - Submit feedback',
            'GET /api/reports/events - Event reports',
            'GET /api/reports/students - Student reports',
            'GET /api/reports/top-students - Top active students'
        ]
    })

# College Management
@app.route('/api/colleges', methods=['GET'])
def get_colleges():
    colleges = College.query.all()
    return jsonify([college.to_dict() for college in colleges])

@app.route('/api/colleges', methods=['POST'])
def create_college():
    data = request.get_json()
    
    if not data or 'name' not in data or 'code' not in data:
        return jsonify({'error': 'Missing required fields: name, code'}), 400
    
    college = College(name=data['name'], code=data['code'])
    
    try:
        db.session.add(college)
        db.session.commit()
        return jsonify(college.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'College code already exists'}), 400

# Student Management
@app.route('/api/students', methods=['GET'])
def get_students():
    college_id = request.args.get('college_id')
    if college_id:
        students = Student.query.filter_by(college_id=college_id).all()
    else:
        students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    
    required_fields = ['student_id', 'name', 'email', 'college_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    student = Student(
        student_id=data['student_id'],
        name=data['name'],
        email=data['email'],
        college_id=data['college_id']
    )
    
    try:
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Student ID or email already exists'}), 400

# Event Management
@app.route('/api/events', methods=['GET'])
def get_events():
    college_id = request.args.get('college_id')
    event_type = request.args.get('event_type')
    is_active = request.args.get('is_active', 'true').lower() == 'true'
    
    query = Event.query.filter_by(is_active=is_active)
    
    if college_id:
        query = query.filter_by(college_id=college_id)
    if event_type:
        query = query.filter_by(event_type=event_type)
    
    events = query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/api/events', methods=['POST'])
def create_event():
    data = request.get_json()
    
    required_fields = ['title', 'event_type', 'date', 'time', 'venue', 'college_id', 'created_by']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    try:
        event = Event(
            title=data['title'],
            description=data.get('description', ''),
            event_type=data['event_type'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(data['time'], '%H:%M').time(),
            venue=data['venue'],
            max_participants=data.get('max_participants', 100),
            college_id=data['college_id'],
            created_by=data['created_by']
        )
        
        db.session.add(event)
        db.session.commit()
        return jsonify(event.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Registration Management
@app.route('/api/register', methods=['POST'])
def register_student():
    data = request.get_json()
    
    required_fields = ['student_id', 'event_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    # Check if event exists and is active
    event = Event.query.get(data['event_id'])
    if not event or not event.is_active:
        return jsonify({'error': 'Event not found or inactive'}), 404
    
    # Check if student exists
    student = Student.query.get(data['student_id'])
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Check if already registered
    existing_reg = Registration.query.filter_by(
        student_id=data['student_id'], 
        event_id=data['event_id'],
        is_cancelled=False
    ).first()
    
    if existing_reg:
        return jsonify({'error': 'Student already registered for this event'}), 400
    
    # Check capacity
    active_registrations = Registration.query.filter_by(
        event_id=data['event_id'],
        is_cancelled=False
    ).count()
    
    if active_registrations >= event.max_participants:
        return jsonify({'error': 'Event is full'}), 400
    
    registration = Registration(
        student_id=data['student_id'],
        event_id=data['event_id']
    )
    
    try:
        db.session.add(registration)
        db.session.commit()
        return jsonify(registration.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/registrations', methods=['GET'])
def get_registrations():
    event_id = request.args.get('event_id')
    student_id = request.args.get('student_id')
    
    query = Registration.query.filter_by(is_cancelled=False)
    
    if event_id:
        query = query.filter_by(event_id=event_id)
    if student_id:
        query = query.filter_by(student_id=student_id)
    
    registrations = query.all()
    return jsonify([reg.to_dict() for reg in registrations])

# Attendance Management
@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    
    required_fields = ['registration_id', 'marked_by']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    # Check if registration exists
    registration = Registration.query.get(data['registration_id'])
    if not registration or registration.is_cancelled:
        return jsonify({'error': 'Registration not found or cancelled'}), 404
    
    # Check if attendance already marked
    existing_attendance = Attendance.query.filter_by(registration_id=data['registration_id']).first()
    if existing_attendance:
        return jsonify({'error': 'Attendance already marked for this registration'}), 400
    
    attendance = Attendance(
        registration_id=data['registration_id'],
        marked_by=data['marked_by']
    )
    
    try:
        db.session.add(attendance)
        db.session.commit()
        return jsonify(attendance.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    event_id = request.args.get('event_id')
    
    if event_id:
        attendances = db.session.query(Attendance).join(Registration).filter(
            Registration.event_id == event_id
        ).all()
    else:
        attendances = Attendance.query.all()
    
    return jsonify([att.to_dict() for att in attendances])

# Feedback Management
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    
    required_fields = ['registration_id', 'rating']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
    
    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    # Check if registration exists and has attendance
    registration = Registration.query.get(data['registration_id'])
    if not registration:
        return jsonify({'error': 'Registration not found'}), 404
    
    if not registration.attendance:
        return jsonify({'error': 'Feedback can only be submitted after attending the event'}), 400
    
    # Check if feedback already exists
    existing_feedback = Feedback.query.filter_by(registration_id=data['registration_id']).first()
    if existing_feedback:
        return jsonify({'error': 'Feedback already submitted for this event'}), 400
    
    feedback = Feedback(
        registration_id=data['registration_id'],
        rating=data['rating'],
        comment=data.get('comment', '')
    )
    
    try:
        db.session.add(feedback)
        db.session.commit()
        return jsonify(feedback.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Reports
@app.route('/api/reports/events', methods=['GET'])
def event_reports():
    college_id = request.args.get('college_id')
    event_type = request.args.get('event_type')
    
    # Base query for events with registration and attendance counts
    query = db.session.query(
        Event.id,
        Event.title,
        Event.event_type,
        Event.date,
        Event.college_id,
        College.name.label('college_name'),
        db.func.count(Registration.id).label('total_registrations'),
        db.func.count(Attendance.id).label('total_attendance')
    ).join(College).outerjoin(Registration, 
        (Registration.event_id == Event.id) & (Registration.is_cancelled == False)
    ).outerjoin(Attendance, Registration.id == Attendance.registration_id).group_by(Event.id)
    
    if college_id:
        query = query.filter(Event.college_id == college_id)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    
    results = query.all()
    
    reports = []
    for result in results:
        # Calculate attendance percentage
        attendance_percentage = 0
        if result.total_registrations > 0:
            attendance_percentage = round((result.total_attendance / result.total_registrations) * 100, 2)
        
        # Get average feedback
        avg_feedback = db.session.query(
            db.func.avg(Feedback.rating)
        ).join(Registration).filter(
            Registration.event_id == result.id
        ).scalar()
        
        reports.append({
            'event_id': result.id,
            'title': result.title,
            'event_type': result.event_type,
            'date': result.date.isoformat(),
            'college_id': result.college_id,
            'college_name': result.college_name,
            'total_registrations': result.total_registrations,
            'total_attendance': result.total_attendance,
            'attendance_percentage': attendance_percentage,
            'average_feedback': round(float(avg_feedback), 2) if avg_feedback else None
        })
    
    # Sort by total registrations (popularity)
    reports.sort(key=lambda x: x['total_registrations'], reverse=True)
    
    return jsonify({
        'reports': reports,
        'summary': {
            'total_events': len(reports),
            'total_registrations': sum(r['total_registrations'] for r in reports),
            'total_attendance': sum(r['total_attendance'] for r in reports),
            'overall_attendance_rate': round(
                (sum(r['total_attendance'] for r in reports) / 
                 max(sum(r['total_registrations'] for r in reports), 1)) * 100, 2
            )
        }
    })

@app.route('/api/reports/students', methods=['GET'])
def student_reports():
    college_id = request.args.get('college_id')
    
    # Query for student participation
    query = db.session.query(
        Student.id,
        Student.name,
        Student.student_id,
        Student.college_id,
        College.name.label('college_name'),
        db.func.count(Registration.id).label('total_registrations'),
        db.func.count(Attendance.id).label('total_attendance')
    ).join(College).outerjoin(Registration, 
        (Registration.student_id == Student.id) & (Registration.is_cancelled == False)
    ).outerjoin(Attendance, Registration.id == Attendance.registration_id).group_by(Student.id)
    
    if college_id:
        query = query.filter(Student.college_id == college_id)
    
    results = query.all()
    
    reports = []
    for result in results:
        attendance_percentage = 0
        if result.total_registrations > 0:
            attendance_percentage = round((result.total_attendance / result.total_registrations) * 100, 2)
        
        reports.append({
            'student_id': result.id,
            'name': result.name,
            'student_number': result.student_id,
            'college_id': result.college_id,
            'college_name': result.college_name,
            'total_registrations': result.total_registrations,
            'total_attendance': result.total_attendance,
            'attendance_percentage': attendance_percentage
        })
    
    # Sort by total attendance (participation)
    reports.sort(key=lambda x: x['total_attendance'], reverse=True)
    
    return jsonify({
        'reports': reports,
        'summary': {
            'total_students': len(reports),
            'active_students': len([r for r in reports if r['total_registrations'] > 0]),
            'average_registrations_per_student': round(
                sum(r['total_registrations'] for r in reports) / max(len(reports), 1), 2
            )
        }
    })

@app.route('/api/reports/top-students', methods=['GET'])
def top_students():
    college_id = request.args.get('college_id')
    limit = int(request.args.get('limit', 3))
    
    # Query for most active students (by attendance)
    query = db.session.query(
        Student.id,
        Student.name,
        Student.student_id,
        Student.college_id,
        College.name.label('college_name'),
        db.func.count(Registration.id).label('total_registrations'),
        db.func.count(Attendance.id).label('total_attendance')
    ).join(College).outerjoin(Registration, 
        (Registration.student_id == Student.id) & (Registration.is_cancelled == False)
    ).outerjoin(Attendance, Registration.id == Attendance.registration_id).group_by(Student.id).having(
        db.func.count(Attendance.id) > 0
    ).order_by(db.func.count(Attendance.id).desc()).limit(limit)
    
    if college_id:
        query = query.filter(Student.college_id == college_id)
    
    results = query.all()
    
    top_students = []
    for i, result in enumerate(results, 1):
        attendance_percentage = round((result.total_attendance / result.total_registrations) * 100, 2)
        
        top_students.append({
            'rank': i,
            'student_id': result.id,
            'name': result.name,
            'student_number': result.student_id,
            'college_id': result.college_id,
            'college_name': result.college_name,
            'total_registrations': result.total_registrations,
            'total_attendance': result.total_attendance,
            'attendance_percentage': attendance_percentage
        })
    
    return jsonify({'top_students': top_students})

# Database initialization
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
'''

with open('app.py', 'w') as f:
    f.write(app_py_content.strip())

print("✅ 1. Created app.py")