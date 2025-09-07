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

        print("\n🎉 Sample data initialization completed successfully!")
        print(f"📊 Database Summary:")
        print(f"   - {len(colleges)} Colleges")
        print(f"   - {len(students)} Students") 
        print(f"   - {len(events)} Events")

if __name__ == '__main__':
    init_sample_data()