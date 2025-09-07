# Continue with remaining files

# 8. Create the database and sample data
import sqlite3
from datetime import datetime, date, time

def create_sample_database():
    conn = sqlite3.connect('campus_events.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS college (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            code VARCHAR(10) UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            college_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (college_id) REFERENCES college (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            event_type VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            venue VARCHAR(100) NOT NULL,
            max_participants INTEGER DEFAULT 100,
            college_id INTEGER NOT NULL,
            created_by VARCHAR(100) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (college_id) REFERENCES college (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            event_id INTEGER NOT NULL,
            registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_cancelled BOOLEAN DEFAULT 0,
            FOREIGN KEY (student_id) REFERENCES student (id),
            FOREIGN KEY (event_id) REFERENCES event (id),
            UNIQUE(student_id, event_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL,
            marked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            marked_by VARCHAR(100) NOT NULL,
            FOREIGN KEY (registration_id) REFERENCES registration (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (registration_id) REFERENCES registration (id)
        )
    ''')
    
    # Insert sample data
    colleges = [
        ('MIT Institute of Technology', 'MIT'),
        ('Stanford University', 'STAN'),
        ('IIT Delhi', 'IITD'),
        ('UC Berkeley', 'UCB'),
        ('Carnegie Mellon University', 'CMU')
    ]
    cursor.executemany('INSERT INTO college (name, code) VALUES (?, ?)', colleges)
    
    students = [
        ('MIT001', 'Alice Johnson', 'alice@mit.edu', 1),
        ('MIT002', 'Bob Smith', 'bob@mit.edu', 1),
        ('MIT003', 'Carol Williams', 'carol@mit.edu', 1),
        ('MIT004', 'Daniel Brown', 'daniel@mit.edu', 1),
        ('STAN001', 'Emma Davis', 'emma@stanford.edu', 2),
        ('STAN002', 'Frank Miller', 'frank@stanford.edu', 2),
        ('STAN003', 'Grace Wilson', 'grace@stanford.edu', 2),
        ('IITD001', 'Henry Taylor', 'henry@iitd.edu', 3),
        ('IITD002', 'Ivy Anderson', 'ivy@iitd.edu', 3),
        ('IITD003', 'Jack Thomas', 'jack@iitd.edu', 3),
        ('UCB001', 'Kate Jackson', 'kate@berkeley.edu', 4),
        ('UCB002', 'Liam White', 'liam@berkeley.edu', 4),
        ('CMU001', 'Maya Harris', 'maya@cmu.edu', 5),
        ('CMU002', 'Noah Martin', 'noah@cmu.edu', 5),
    ]
    cursor.executemany('INSERT INTO student (student_id, name, email, college_id) VALUES (?, ?, ?, ?)', students)
    
    events = [
        ('AI/ML Workshop', 'Learn the fundamentals of Machine Learning', 'Workshop', '2024-10-15', '10:00', 'Tech Hall A', 50, 1, 'Dr. Tech Admin'),
        ('Hackathon 2024', '24-hour coding competition', 'Hackathon', '2024-10-20', '09:00', 'Innovation Center', 100, 1, 'Prof. Code Master'),
        ('Tech Talk: Future of Web Development', 'Industry expert sharing insights', 'TechTalk', '2024-10-25', '14:00', 'Auditorium B', 200, 2, 'Dean of Engineering'),
        ('Startup Pitch Competition', 'Present your startup ideas', 'Workshop', '2024-11-05', '13:00', 'Business Hall', 75, 2, 'Entrepreneurship Center'),
        ('Annual Tech Fest', 'Technology celebration and competitions', 'Fest', '2024-11-01', '08:00', 'Campus Grounds', 500, 3, 'Event Coordinator'),
        ('Data Science Seminar', 'Advanced data analysis techniques', 'TechTalk', '2024-10-30', '15:30', 'Data Lab', 60, 4, 'Data Science Dept'),
        ('Robotics Workshop', 'Build and program robots', 'Workshop', '2024-11-10', '10:00', 'Robotics Lab', 40, 5, 'Robotics Institute'),
    ]
    cursor.executemany('INSERT INTO event (title, description, event_type, date, time, venue, max_participants, college_id, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', events)
    
    # Sample registrations (29 total)
    registrations = [
        # AI/ML Workshop (4 registrations)
        (1, 1), (2, 1), (3, 1), (4, 1),
        # Hackathon 2024 (5 registrations)
        (1, 2), (2, 2), (5, 2), (8, 2), (11, 2),
        # Tech Talk (5 registrations)
        (5, 3), (6, 3), (7, 3), (1, 3), (13, 3),
        # Startup Pitch (3 registrations)
        (5, 4), (6, 4), (11, 4),
        # Tech Fest (6 registrations)
        (8, 5), (9, 5), (10, 5), (1, 5), (5, 5), (13, 5),
        # Data Science Seminar (3 registrations)
        (11, 6), (12, 6), (1, 6),
        # Robotics Workshop (3 registrations)
        (13, 7), (14, 7), (8, 7),
    ]
    cursor.executemany('INSERT INTO registration (student_id, event_id) VALUES (?, ?)', registrations)
    
    # Sample attendance (23 out of 29)
    attendances = [
        (1, 'Dr. Tech Admin'), (2, 'Dr. Tech Admin'), (3, 'Dr. Tech Admin'),  # AI/ML (3/4)
        (5, 'Prof. Code Master'), (6, 'Prof. Code Master'), (7, 'Prof. Code Master'), (8, 'Prof. Code Master'),  # Hackathon (4/5)
        (10, 'Dean of Engineering'), (11, 'Dean of Engineering'), (12, 'Dean of Engineering'), (14, 'Dean of Engineering'),  # Tech Talk (4/5)
        (15, 'Entrepreneurship Center'), (17, 'Entrepreneurship Center'),  # Startup Pitch (2/3)
        (18, 'Event Coordinator'), (19, 'Event Coordinator'), (20, 'Event Coordinator'), (21, 'Event Coordinator'), (23, 'Event Coordinator'),  # Tech Fest (5/6)
        (24, 'Data Science Dept'), (26, 'Data Science Dept'),  # Data Science (2/3)
        (27, 'Robotics Institute'), (28, 'Robotics Institute'), (29, 'Robotics Institute'),  # Robotics (3/3)
    ]
    cursor.executemany('INSERT INTO attendance (registration_id, marked_by) VALUES (?, ?)', attendances)
    
    # Sample feedback (23 feedback entries)
    feedbacks = [
        (1, 5, 'Excellent workshop! Learned a lot about ML fundamentals.'),
        (2, 4, 'Very informative, but could use more hands-on exercises.'),
        (3, 5, 'Outstanding presentation and materials.'),
        (5, 5, 'Best hackathon ever! Great team collaboration.'),
        (6, 4, 'Great experience, loved the competitive environment.'),
        (7, 5, 'Amazing event, well organized and inspiring.'),
        (8, 3, 'Good event but could have better mentorship.'),
        (10, 5, 'Amazing insights into the future of web development.'),
        (11, 4, 'Very helpful for understanding industry trends.'),
        (12, 4, 'Great speaker, relevant content.'),
        (14, 5, 'Inspiring talk, gave me new ideas for my projects.'),
        (15, 4, 'Great networking opportunity and learned about pitching.'),
        (17, 5, 'Excellent event for aspiring entrepreneurs.'),
        (18, 5, 'Fantastic fest with great competitions and exhibitions.'),
        (19, 5, 'Well organized, lots of fun activities.'),
        (20, 4, 'Good fest, enjoyed the technical competitions.'),
        (21, 5, 'Amazing experience, met many like-minded people.'),
        (23, 4, 'Great fest, good variety of events.'),
        (24, 5, 'Advanced techniques explained clearly.'),
        (26, 4, 'Valuable insights for my research work.'),
        (27, 5, 'Hands-on robotics experience was incredible!'),
        (28, 4, 'Good introduction to robotics programming.'),
        (29, 5, 'Amazing workshop, want to attend more robotics events.'),
    ]
    cursor.executemany('INSERT INTO feedback (registration_id, rating, comment) VALUES (?, ?, ?)', feedbacks)
    
    conn.commit()
    conn.close()
    return True

# Create the database
create_sample_database()
print("✅ 8. Created campus_events.db with sample data")

# 9. sample_api_responses.json
sample_responses = {
    "event_popularity_report": {
        "reports": [
            {
                "event_id": 5,
                "title": "Annual Tech Fest",
                "event_type": "Fest",
                "date": "2024-11-01",
                "college_id": 3,
                "college_name": "IIT Delhi",
                "total_registrations": 6,
                "total_attendance": 5,
                "attendance_percentage": 83.33,
                "average_feedback": 4.6
            },
            {
                "event_id": 2,
                "title": "Hackathon 2024",
                "event_type": "Hackathon",
                "date": "2024-10-20",
                "college_id": 1,
                "college_name": "MIT Institute of Technology",
                "total_registrations": 5,
                "total_attendance": 4,
                "attendance_percentage": 80.0,
                "average_feedback": 4.25
            }
        ],
        "summary": {
            "total_events": 7,
            "total_registrations": 29,
            "total_attendance": 23,
            "overall_attendance_rate": 79.31
        }
    },
    "top_students_report": {
        "top_students": [
            {
                "rank": 1,
                "student_id": 1,
                "name": "Alice Johnson",
                "student_number": "MIT001",
                "college_id": 1,
                "college_name": "MIT Institute of Technology",
                "total_registrations": 5,
                "total_attendance": 4,
                "attendance_percentage": 80.0
            },
            {
                "rank": 2,
                "student_id": 5,
                "name": "Emma Davis",
                "student_number": "STAN001",
                "college_id": 2,
                "college_name": "Stanford University",
                "total_registrations": 4,
                "total_attendance": 3,
                "attendance_percentage": 75.0
            },
            {
                "rank": 3,
                "student_id": 8,
                "name": "Henry Taylor",
                "student_number": "IITD001",
                "college_id": 3,
                "college_name": "IIT Delhi",
                "total_registrations": 3,
                "total_attendance": 3,
                "attendance_percentage": 100.0
            }
        ]
    }
}

import json
with open('sample_api_responses.json', 'w') as f:
    json.dump(sample_responses, f, indent=2)

print("✅ 9. Created sample_api_responses.json")