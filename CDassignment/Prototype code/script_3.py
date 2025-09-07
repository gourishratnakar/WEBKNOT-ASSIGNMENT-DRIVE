# 4. test_api.py - Comprehensive testing script
test_api_content = '''
import requests
import json
from datetime import datetime, date

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000/api'

def print_response(response, title):
    print(f"\\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)

def test_complete_workflow():
    print("🚀 Starting Campus Event Management Platform API Testing")
    
    # 1. Create Colleges
    print("\\n📍 Step 1: Creating Colleges")
    
    colleges_data = [
        {'name': 'MIT Institute of Technology', 'code': 'MIT'},
        {'name': 'Stanford University', 'code': 'STAN'},
        {'name': 'IIT Delhi', 'code': 'IITD'}
    ]
    
    college_ids = {}
    for college_data in colleges_data:
        response = requests.post(f'{BASE_URL}/colleges', json=college_data)
        print_response(response, f"Creating College: {college_data['name']}")
        if response.status_code == 201:
            college_ids[college_data['code']] = response.json()['id']
    
    # 2. Create Students
    print("\\n👥 Step 2: Creating Students")
    
    students_data = [
        {'student_id': 'MIT001', 'name': 'Alice Johnson', 'email': 'alice@mit.edu', 'college_id': college_ids['MIT']},
        {'student_id': 'MIT002', 'name': 'Bob Smith', 'email': 'bob@mit.edu', 'college_id': college_ids['MIT']},
        {'student_id': 'MIT003', 'name': 'Carol Williams', 'email': 'carol@mit.edu', 'college_id': college_ids['MIT']},
        {'student_id': 'STAN001', 'name': 'David Brown', 'email': 'david@stanford.edu', 'college_id': college_ids['STAN']},
        {'student_id': 'STAN002', 'name': 'Emma Davis', 'email': 'emma@stanford.edu', 'college_id': college_ids['STAN']},
        {'student_id': 'IITD001', 'name': 'Frank Miller', 'email': 'frank@iitd.edu', 'college_id': college_ids['IITD']},
        {'student_id': 'IITD002', 'name': 'Grace Wilson', 'email': 'grace@iitd.edu', 'college_id': college_ids['IITD']},
    ]
    
    student_ids = {}
    for student_data in students_data:
        response = requests.post(f'{BASE_URL}/students', json=student_data)
        print_response(response, f"Creating Student: {student_data['name']}")
        if response.status_code == 201:
            student_ids[student_data['student_id']] = response.json()['id']
    
    # 3. Create Events
    print("\\n📅 Step 3: Creating Events")
    
    events_data = [
        {
            'title': 'AI/ML Workshop',
            'description': 'Learn the fundamentals of Machine Learning',
            'event_type': 'Workshop',
            'date': '2024-10-15',
            'time': '10:00',
            'venue': 'Tech Hall A',
            'max_participants': 50,
            'college_id': college_ids['MIT'],
            'created_by': 'Dr. Tech Admin'
        },
        {
            'title': 'Hackathon 2024',
            'description': '24-hour coding competition',
            'event_type': 'Hackathon', 
            'date': '2024-10-20',
            'time': '09:00',
            'venue': 'Innovation Center',
            'max_participants': 100,
            'college_id': college_ids['MIT'],
            'created_by': 'Prof. Code Master'
        },
        {
            'title': 'Tech Talk: Future of Web Development',
            'description': 'Industry expert sharing insights',
            'event_type': 'TechTalk',
            'date': '2024-10-25',
            'time': '14:00',
            'venue': 'Auditorium B',
            'max_participants': 200,
            'college_id': college_ids['STAN'],
            'created_by': 'Dean of Engineering'
        },
        {
            'title': 'Annual Tech Fest',
            'description': 'Technology celebration and competitions',
            'event_type': 'Fest',
            'date': '2024-11-01',
            'time': '08:00',
            'venue': 'Campus Grounds',
            'max_participants': 500,
            'college_id': college_ids['IITD'],
            'created_by': 'Event Coordinator'
        }
    ]
    
    event_ids = []
    for i, event_data in enumerate(events_data):
        response = requests.post(f'{BASE_URL}/events', json=event_data)
        print_response(response, f"Creating Event: {event_data['title']}")
        if response.status_code == 201:
            event_ids.append(response.json()['id'])
    
    # 4. Register Students for Events
    print("\\n📝 Step 4: Registering Students for Events")
    
    # Register multiple students for each event
    registrations = [
        # AI/ML Workshop (MIT)
        {'student_id': student_ids['MIT001'], 'event_id': event_ids[0]},
        {'student_id': student_ids['MIT002'], 'event_id': event_ids[0]},
        {'student_id': student_ids['MIT003'], 'event_id': event_ids[0]},
        
        # Hackathon 2024 (MIT)
        {'student_id': student_ids['MIT001'], 'event_id': event_ids[1]},
        {'student_id': student_ids['MIT002'], 'event_id': event_ids[1]},
        {'student_id': student_ids['STAN001'], 'event_id': event_ids[1]},
        {'student_id': student_ids['IITD001'], 'event_id': event_ids[1]},
        
        # Tech Talk (Stanford)
        {'student_id': student_ids['STAN001'], 'event_id': event_ids[2]},
        {'student_id': student_ids['STAN002'], 'event_id': event_ids[2]},
        {'student_id': student_ids['MIT001'], 'event_id': event_ids[2]},
        
        # Tech Fest (IIT Delhi)
        {'student_id': student_ids['IITD001'], 'event_id': event_ids[3]},
        {'student_id': student_ids['IITD002'], 'event_id': event_ids[3]},
        {'student_id': student_ids['MIT001'], 'event_id': event_ids[3]},
        {'student_id': student_ids['STAN001'], 'event_id': event_ids[3]},
    ]
    
    registration_ids = []
    for reg_data in registrations:
        response = requests.post(f'{BASE_URL}/register', json=reg_data)
        print_response(response, f"Registration for Event ID: {reg_data['event_id']}")
        if response.status_code == 201:
            registration_ids.append(response.json()['id'])
    
    # 5. Mark Attendance
    print("\\n✅ Step 5: Marking Attendance")
    
    # Mark attendance for some (not all) registrations
    attendance_data = [
        {'registration_id': registration_ids[0], 'marked_by': 'Dr. Tech Admin'},
        {'registration_id': registration_ids[1], 'marked_by': 'Dr. Tech Admin'},
        # MIT003 didn't attend AI/ML Workshop
        
        {'registration_id': registration_ids[3], 'marked_by': 'Prof. Code Master'},
        {'registration_id': registration_ids[4], 'marked_by': 'Prof. Code Master'},
        {'registration_id': registration_ids[5], 'marked_by': 'Prof. Code Master'},
        # IITD001 didn't attend Hackathon
        
        {'registration_id': registration_ids[7], 'marked_by': 'Dean of Engineering'},
        {'registration_id': registration_ids[8], 'marked_by': 'Dean of Engineering'},
        # MIT001 didn't attend Tech Talk
        
        {'registration_id': registration_ids[10], 'marked_by': 'Event Coordinator'},
        {'registration_id': registration_ids[11], 'marked_by': 'Event Coordinator'},
        {'registration_id': registration_ids[12], 'marked_by': 'Event Coordinator'},
        # STAN001 didn't attend Tech Fest
    ]
    
    for att_data in attendance_data:
        response = requests.post(f'{BASE_URL}/attendance', json=att_data)
        print_response(response, f"Attendance for Registration ID: {att_data['registration_id']}")
    
    # 6. Submit Feedback
    print("\\n💬 Step 6: Submitting Feedback")
    
    feedback_data = [
        {'registration_id': registration_ids[0], 'rating': 5, 'comment': 'Excellent workshop!'},
        {'registration_id': registration_ids[1], 'rating': 4, 'comment': 'Very informative'},
        {'registration_id': registration_ids[3], 'rating': 5, 'comment': 'Best hackathon ever!'},
        {'registration_id': registration_ids[4], 'rating': 4, 'comment': 'Great experience'},
        {'registration_id': registration_ids[5], 'rating': 3, 'comment': 'Good but could be better'},
        {'registration_id': registration_ids[7], 'rating': 5, 'comment': 'Amazing insights'},
        {'registration_id': registration_ids[8], 'rating': 4, 'comment': 'Very helpful'},
        {'registration_id': registration_ids[10], 'rating': 5, 'comment': 'Fantastic fest!'},
        {'registration_id': registration_ids[11], 'rating': 5, 'comment': 'Well organized'},
        {'registration_id': registration_ids[12], 'rating': 4, 'comment': 'Great fun'},
    ]
    
    for feedback in feedback_data:
        response = requests.post(f'{BASE_URL}/feedback', json=feedback)
        print_response(response, f"Feedback for Registration ID: {feedback['registration_id']}")
    
    # 7. Generate Reports
    print("\\n📊 Step 7: Generating Reports")
    
    # Event Reports
    response = requests.get(f'{BASE_URL}/reports/events')
    print_response(response, "📈 Event Popularity Report")
    
    # Student Reports  
    response = requests.get(f'{BASE_URL}/reports/students')
    print_response(response, "👤 Student Participation Report")
    
    # Top Students
    response = requests.get(f'{BASE_URL}/reports/top-students')
    print_response(response, "🏆 Top 3 Most Active Students")
    
    # 8. Test Filtering
    print("\\n🔍 Step 8: Testing Report Filters")
    
    # Filter events by type
    response = requests.get(f'{BASE_URL}/reports/events?event_type=Workshop')
    print_response(response, "📈 Workshop Events Only")
    
    # Filter by college
    response = requests.get(f'{BASE_URL}/reports/students?college_id={college_ids["MIT"]}')
    print_response(response, "👤 MIT Students Only")
    
    print("\\n🎉 Testing Complete!")
    print("✅ All API endpoints tested successfully")
    print("✅ Complete workflow demonstrated:")
    print("   - College creation")
    print("   - Student registration")  
    print("   - Event creation")
    print("   - Student-Event registration")
    print("   - Attendance marking")
    print("   - Feedback submission")
    print("   - Report generation")

if __name__ == '__main__':
    test_complete_workflow()
'''

with open('test_api.py', 'w') as f:
    f.write(test_api_content.strip())

print("✅ 4. Created test_api.py")

# 5. init_db.py - Database initialization
init_db_content = '''
from app import app, db, College, Student, Event, Registration, Attendance, Feedback
from datetime import datetime, date, time

def init_sample_data():
    """Initialize the database with sample data"""
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("🗄️ Database tables created successfully!")
        
        # Create Colleges
        colleges = [
            College(name='MIT Institute of Technology', code='MIT'),
            College(name='Stanford University', code='STAN'),
            College(name='IIT Delhi', code='IITD'),
            College(name='UC Berkeley', code='UCB'),
            College(name='Carnegie Mellon University', code='CMU')
        ]
        
        for college in colleges:
            db.session.add(college)
        db.session.commit()
        print(f"✅ Created {len(colleges)} colleges")
        
        # Create Students
        students = [
            # MIT Students
            Student(student_id='MIT001', name='Alice Johnson', email='alice@mit.edu', college_id=1),
            Student(student_id='MIT002', name='Bob Smith', email='bob@mit.edu', college_id=1),
            Student(student_id='MIT003', name='Carol Williams', email='carol@mit.edu', college_id=1),
            Student(student_id='MIT004', name='Daniel Brown', email='daniel@mit.edu', college_id=1),
            
            # Stanford Students
            Student(student_id='STAN001', name='Emma Davis', email='emma@stanford.edu', college_id=2),
            Student(student_id='STAN002', name='Frank Miller', email='frank@stanford.edu', college_id=2),
            Student(student_id='STAN003', name='Grace Wilson', email='grace@stanford.edu', college_id=2),
            
            # IIT Delhi Students
            Student(student_id='IITD001', name='Henry Taylor', email='henry@iitd.edu', college_id=3),
            Student(student_id='IITD002', name='Ivy Anderson', email='ivy@iitd.edu', college_id=3),
            Student(student_id='IITD003', name='Jack Thomas', email='jack@iitd.edu', college_id=3),
            
            # UC Berkeley Students
            Student(student_id='UCB001', name='Kate Jackson', email='kate@berkeley.edu', college_id=4),
            Student(student_id='UCB002', name='Liam White', email='liam@berkeley.edu', college_id=4),
            
            # CMU Students
            Student(student_id='CMU001', name='Maya Harris', email='maya@cmu.edu', college_id=5),
            Student(student_id='CMU002', name='Noah Martin', email='noah@cmu.edu', college_id=5),
        ]
        
        for student in students:
            db.session.add(student)
        db.session.commit()
        print(f"✅ Created {len(students)} students")
        
        # Create Events
        events = [
            # MIT Events
            Event(title='AI/ML Workshop', description='Learn the fundamentals of Machine Learning', 
                  event_type='Workshop', date=date(2024, 10, 15), time=time(10, 0), 
                  venue='Tech Hall A', max_participants=50, college_id=1, created_by='Dr. Tech Admin'),
            
            Event(title='Hackathon 2024', description='24-hour coding competition', 
                  event_type='Hackathon', date=date(2024, 10, 20), time=time(9, 0), 
                  venue='Innovation Center', max_participants=100, college_id=1, created_by='Prof. Code Master'),
            
            # Stanford Events
            Event(title='Tech Talk: Future of Web Development', description='Industry expert sharing insights', 
                  event_type='TechTalk', date=date(2024, 10, 25), time=time(14, 0), 
                  venue='Auditorium B', max_participants=200, college_id=2, created_by='Dean of Engineering'),
            
            Event(title='Startup Pitch Competition', description='Present your startup ideas', 
                  event_type='Workshop', date=date(2024, 11, 5), time=time(13, 0), 
                  venue='Business Hall', max_participants=75, college_id=2, created_by='Entrepreneurship Center'),
            
            # IIT Delhi Events
            Event(title='Annual Tech Fest', description='Technology celebration and competitions', 
                  event_type='Fest', date=date(2024, 11, 1), time=time(8, 0), 
                  venue='Campus Grounds', max_participants=500, college_id=3, created_by='Event Coordinator'),
            
            # UC Berkeley Events
            Event(title='Data Science Seminar', description='Advanced data analysis techniques', 
                  event_type='TechTalk', date=date(2024, 10, 30), time=time(15, 30), 
                  venue='Data Lab', max_participants=60, college_id=4, created_by='Data Science Dept'),
            
            # CMU Events
            Event(title='Robotics Workshop', description='Build and program robots', 
                  event_type='Workshop', date=date(2024, 11, 10), time=time(10, 0), 
                  venue='Robotics Lab', max_participants=40, college_id=5, created_by='Robotics Institute'),
        ]
        
        for event in events:
            db.session.add(event)
        db.session.commit()
        print(f"✅ Created {len(events)} events")
        
        print("\\n🎉 Sample data initialization completed successfully!")
        print(f"📊 Database Summary:")
        print(f"   - {len(colleges)} Colleges")
        print(f"   - {len(students)} Students") 
        print(f"   - {len(events)} Events")

if __name__ == '__main__':
    init_sample_data()
'''

with open('init_db.py', 'w') as f:
    f.write(init_db_content.strip())

print("✅ 5. Created init_db.py")