# List all the files that were created in this session
import os
import glob

print("📁 CHECKING FILES CREATED IN THIS SESSION")
print("="*60)

# Get all files in current directory
all_files = []
for file in os.listdir('.'):
    if os.path.isfile(file):
        all_files.append(file)

print(f"Files found in current directory: {len(all_files)}")
print()

# List the files we created
created_files = [
    'app.py',
    'requirements.txt', 
    'init_db.py',
    'test_api.py',
    'run_demo.py',
    'README.md',
    'DESIGN_DOCUMENT.md',
    'AI_CONVERSATION_LOG.md',
    'campus_events.db',
    'sample_api_responses.json',
    'project_files_summary.csv',
    'HOW_TO_START.md',
    'WHERE_TO_RUN_COMMANDS.md',
    'SUBMISSION_PACKAGE.md'
]

print("📋 EXPECTED FILES FOR SUBMISSION:")
print("-" * 40)

existing_files = []
missing_files = []

for i, filename in enumerate(created_files, 1):
    if filename in all_files:
        size = os.path.getsize(filename)
        print(f"✅ {i:2d}. {filename} ({size:,} bytes)")
        existing_files.append(filename)
    else:
        print(f"❌ {i:2d}. {filename} (MISSING)")
        missing_files.append(filename)

print(f"\n📊 SUMMARY:")
print(f"✅ Files present: {len(existing_files)}")
print(f"❌ Files missing: {len(missing_files)}")

if missing_files:
    print(f"\n⚠️  MISSING FILES:")
    for file in missing_files:
        print(f"   - {file}")

print(f"\n📁 ALL FILES IN DIRECTORY:")
for file in sorted(all_files):
    size = os.path.getsize(file)
    print(f"   {file} ({size:,} bytes)")

# Show current working directory
print(f"\n📍 CURRENT LOCATION: {os.getcwd()}")