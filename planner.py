from datetime import date


class Assignment:
#Represents an assignment for a subject. Stores assignment title and due date.
    def __init__(self, title, due_date):
        self.title = title
        self.due_date = due_date


class Subject:
#Represents a university subject with attendance and assignments
    def __init__(self, name, code, professor):
        self.name = name
        self.code = code
        self.professor = professor
        self.total_classes = 0
        self.attended_classes = 0
        self.assignments = []


class TimetableEntry:
#Represents a single class session in the timetable.
    def __init__(self, subject, day, start_time, end_time):
        self.subject = subject
        self.day = day
        self.start_time = start_time
        self.end_time = end_time


# ATTENDANCE
def mark_attendance(subject, present):
    #Updates attendance for a subject. Increments total classes and attended classes if present.
    subject.total_classes += 1
    if present:
        subject.attended_classes += 1


def attendance_percentage(subject):
    #Calculates and returns attendance percentage for a subject.
    if subject.total_classes == 0:
        return 100
    return (subject.attended_classes / subject.total_classes) * 100


def attendance_alert(subject):
#Returns True if attendance is below 75%
    return attendance_percentage(subject) < 75


# ASSIGNMENT
def add_assignment(subject, title, due_date):
    #Adds a new assignment to the given subject.
    subject.assignments.append(Assignment(title, due_date))


def upcoming_assignments(subjects, today):
    #Returns a sorted list of upcoming assignments of all subjects.
    result = []
    for sub in subjects:
        for a in sub.assignments:
            if a.due_date >= today:
                result.append((sub.name, a.title, a.due_date))
    return sorted(result, key=lambda x: x[2])



# TIMETABLE
def todays_classes(timetable, today_day):
    #Returns all timetable entries for the given day.
    return [t for t in timetable if t.day == today_day]


# DASHBOARD
def dashboard(subjects, timetable):
    #  Displays today's classes, upcoming assignments and attendance alerts.
    today = date.today()
    today_day = today.strftime("%a")

    print("\n====== DASHBOARD ======\n")

    print("Today's Classes:")
    classes = todays_classes(timetable, today_day)
    if not classes:
        print("No classes today")
    for c in classes:
        print(f"- {c.subject.name} ({c.start_time} - {c.end_time})")

    print("\n Upcoming Assignments:")
    upcoming = upcoming_assignments(subjects, today)
    if not upcoming:
        print("No upcoming assignments")
    for sub, title, due in upcoming:
        print(f"- {title} ({sub}) due on {due}")

    print("\n Attendance Alerts:")
    alerts = False
    for s in subjects:
        if attendance_alert(s):
            alerts = True
            print(f"- {s.name}: {attendance_percentage(s):.2f}%")
    if not alerts:
        print("All attendance above 75%")

def find_subject(subjects, code):
    """Finds and returns a subject by its code"""
    for s in subjects:
        if s.code == code:
            return s
    return None


def menu():
    """Displays the main menu options"""
    print("\n===== UNIVERSITY PLANNER =====")
    print("1. Add Subject")
    print("2. Mark Attendance")
    print("3. Add Assignment")
    print("4. View Dashboard")
    print("5. Add Timetable Entry")
    print("6. Exit")
    


if __name__ == "__main__":
    subjects = []
    timetable = []

    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == "1":                    #add a subject
            name = input("Subject name: ")
            code = input("Subject code: ")
            prof = input("Professor name: ")
            subjects.append(Subject(name, code, prof))
            print("Subject added successfully.")
        elif choice == "2":                  #mark attendance
            code = input("Enter subject code: ")
            subject = find_subject(subjects, code)
            if subject:
                present = input("Present? (y/n): ").lower() == "y"
                mark_attendance(subject, present)
                print("Attendance updated.")
            else:
                print("Subject not found.")
        elif choice == "3":                   #add assignment
            code = input("Enter subject code: ")
            subject = find_subject(subjects, code)
            if subject:
                title = input("Assignment title: ")
                due = input("Due date (YYYY-MM-DD): ")
                add_assignment(subject, title, date.fromisoformat(due))
                print("Assignment added.")
            else:
                print("Subject not found.")
        elif choice == "4":                 #view dashboard
            dashboard(subjects, timetable)
        elif choice == "5":                 #add timetable entry
            code = input("Enter subject code: ")
            subject = find_subject(subjects, code)
            if subject:
                day = input("Day (Mon/Tue/Wed/Thu/Fri/Sat/Sun): ")
                start = input("Start time (HH:MM): ")
                end = input("End time (HH:MM): ")
                timetable.append(TimetableEntry(subject, day, start, end))
                print("Timetable entry added.")
            else:
                print("Subject not found.")
        elif choice == "6":                 #exit
            print("Exiting planner...")
            break
        else:
            print("Invalid choice. Try again.")
