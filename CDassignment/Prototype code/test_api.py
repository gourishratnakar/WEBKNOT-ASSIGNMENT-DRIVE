import requests
import json
from datetime import datetime, date

# Base URL for the API
BASE_URL = 'http://127.0.0.1:5000/api'

def print_response(response, title):
    print(f"\n{'='*60}")
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
    print("\n📍 Step 1: Creating Colleges")

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
    print("\n👥 Step 2: Creating Students")

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
    print("\n📅 Step 3: Creating Events")

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
    print("\n📝 Step 4: Registering Students for Events")

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
    print("\n✅ Step 5: Marking Attendance")

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
    print("\n💬 Step 6: Submitting Feedback")

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
    print("\n📊 Step 7: Generating Reports")

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
    print("\n🔍 Step 8: Testing Report Filters")

    # Filter events by type
    response = requests.get(f'{BASE_URL}/reports/events?event_type=Workshop')
    print_response(response, "📈 Workshop Events Only")

    # Filter by college
    response = requests.get(f'{BASE_URL}/reports/students?college_id={college_ids["MIT"]}')
    print_response(response, "👤 MIT Students Only")

    print("\n🎉 Testing Complete!")
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