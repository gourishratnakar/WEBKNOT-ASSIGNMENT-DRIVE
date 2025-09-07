							MY PERSONAL UNDERSTANDING 

I built this for the Webknot assignment. It’s a small backend that lets colleges post events, students sign up, attendance gets marked, and then it shows simple reports so admins don’t have to guess what’s working.

Now you may ask why I made it this way?...its easy,the task said “basic reports,” but students don’t stay inside one college. They jump across campuses for fests and workshops. So I kept one shared database instead of splitting by college. That makes comparisons easier, queries simpler, and the whole thing less painful to run.

USES:
1] Create events (workshops, hackathons, tech talks, fests) with capacity.
2] Register students, block duplicates, and stop overbooking.
3] Mark attendance and collect 1–5 ratings with comments.
4] Reports that are actually useful:
   a] Popular events: registrations, attendance %, average feedback.
   b] Student activity: registrations vs attendance per student.
   c] Top students: ranked by attendance, with percentages.

DECISIONS I TOOK:
1] Flask + SQLite. Flask is quick to ship; SQLite is perfect locally and can move to Postgres later without any issue.
2] REST + JSON so it works with Postman or a tiny frontend.
3] Single DB for all colleges so analytics make sense and the queries stay clean.

DETAILS:
1] College: basic info about the college.
2] Student: belongs to a college.
3] Event: title, type, date/time, venue, capacity, and which college owns it.
4] Registration: connects a student to an event; supports cancel.
5]Attendance: one per registration.
6] Feedback: 1–5 rating plus optional comment linked to a registration.

THINGS I CARED ABOUT:
1] Real HTTP status codes and helpful error messages.
2] Unique constraints so two people can’t register the same student for the same event at the exact same moment.

Appreciate you taking the time to read this. The project is intentionally small, clean, and easy to spin up so it’s simple to review—and just as easy to extend. If there’s a report, filter, or tiny feature that would help you evaluate it better, let me know and I’ll turn it around quickly. I’m excited to learn, iterate fast, and make this genuinely useful for the team.






