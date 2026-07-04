import csv
from tabulate import tabulate
from student import Student

DATA_FILE = 'students.csv'

CSV_HEADERS = ['id', 'name', 'age', 'course', 'marks']

COURSES = [
"Computer Science", "Mathematics", "Physics",
"Chemistry", "Biology", "Commerce", "Arts",
]

SUBJECTS = [
"Mathematics", "Physics", "Chemistry", "Biology",
"Computer Science", "English", "History", "Economics", "Physical Education",
]

class StudentManager():
   
    def __init__(self):
        self.students = []
        self._next_id = 1
        self.load_from_file()
        self._next_id = self._calculate_next_id()

    def _generate_id(self):
        sid = f'SMS-{self._next_id:04d}'
        self._next_id += 1
        return sid

    def add_student(self, name, age, course):
        student_id = self._generate_id()
        student = Student(student_id, name, age, course)
        self.students.append(student)
        return student
    
    def id_exists(self, sid):
       if self.find_by_id(sid) is not None:
          return self.find_by_id(sid)

    def find_by_id(self, sid):
       for student in self.students:
          if student.student_id == sid:
             return student
       return None
       
    def add_marks(self, student_id, subject, mark):
        student = self.find_by_id(student_id)
        if student is None:
            raise ValueError(f'Student {student_id} not found.')
        if not (0 <= mark <= 100):
            raise ValueError('Mark must be between 0 and 100.')
            
        student.marks[subject] = mark
        return student
    
    def delete_student(self, sid):
       student = self.find_by_id(sid)
       if student is not None:
          self.students.remove(student)
          return True
       else:
          return False

    def get_students_by_course(self, course):
       return [s for s in self.students if s.course.lower() == course.lower()]
    
    def _calculate_next_id(self):
       
       if not self.students:
          return 1
       numbers = [int(s.student_id.split('-')[1]) for s in self.students]
       return max(numbers) + 1

    def display_all_students(self):
       rows = []

       for student in self.students:
          if student.marks:
             percentage = f"{student.get_percentage():.2f}"
          else:
             percentage = "-"

          rows.append([student.student_id, student.name, student.age, student.course, len(student.marks), percentage])

       headers = ["ID", "Name", "Age", "Course", "Subjects", "Percentage"]
       print(tabulate(rows, headers=headers, tablefmt="grid"))

    def display_student_card(self, student):
       info_rows = [["ID", student.student_id],
                    ["Name", student.name],
                    ["Age", student.age],
                    ["Course", student.course],
                    ["Percentage", f"{student.get_percentage():.2f}"],
                    ["Grade", student.get_grade() if student.marks else "-"]
                    ]
       print(tabulate(info_rows,headers=["Field", "Value"], tablefmt="grid"))

       if student.marks:
          marks_rows = [[subject, mark] for subject, mark in student.marks.items()]
          print("\nMarks:")
          print(tabulate(marks_rows, headers=["Subject", "Marks"], tablefmt= "grid"))

    def display_report_card(self, student_id):
       print(f"Student ID: {student_id}")

       student = self.find_by_id(student_id)

       if student is None:
          print(f"Student {student_id} not found")
          return None
       
       rows = []
       for subject, mark in student.marks.items():
          if mark >= 45:
             status = "Pass"
          else:
             status = "Fail"
          rows.append([subject, mark, status])

       print("\nReport Card: ", student.name)
       print("Course: ", student.course)
       print()
       print(tabulate(rows, headers=["Subject", "Mark", "Status"], tablefmt="simple"))

       percentage = student.get_percentage()
       grade = student.get_grade()
       if student.is_passing():
          overall = "Pass"
       else:
          overall = "Fail"

       print(f"\nPercentafe: {percentage:.2f}")
       print(f"Grade: {grade}")
       print(f"Overall Result: {overall}")
        
    def display_course_filter(self):
        print("\nAvailable Courses:")
        for i, course in enumerate(COURSES, 1):
            print(f"{i}. {course}")

        while True:
            try:
                choice = int(input("Select Course (1-7): ").strip())
                if 1 <= choice <= len(COURSES):
                    selected_course = COURSES[choice - 1]
                    break
                print("Invalid selection. Please choose a number from 1 to 7.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"\nSelected: {selected_course}")

        students = self.get_students_by_course(selected_course)

        if students:
            print(f"\nStudents in {selected_course}:")
            rows = []
            for student in students:
                avg = f"{student.get_percentage():.2f}" if student.marks else "-"
                rows.append([
                    student.student_id,
                    student.name,
                    student.age,
                    student.course,
                    len(student.marks),
                    avg
                ])

            print(tabulate(
                rows,
                headers=["ID", "Name", "Age", "Course", "Subjects", "Avg"],
                tablefmt="grid"
            ))
        else:
            print(f"No students found in {selected_course}.")

        print(f"\n{len(students)} student(s) found.")

    def save_to_file(self):
        try:
            with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
                for student in self.students:
                    writer.writerow(student.to_csv_row())
        except IOError as e:
            print(f'Error saving data: {e}')

    def load_from_file(self):
        try:
            with open(DATA_FILE, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader) # skip header
                for row in reader:
                    try:
                        student = Student.from_csv_row(row)
                        self.students.append(student)
                    except Exception as e:
                        print(f'Warning: Skipping bad row: {e}')
        except FileNotFoundError:
            pass # First run, file does not exist yet. That is fine.
        except Exception as e:
            print(f'Error loading data: {e}')

if __name__ == '__main__':

    # Run 1: add students, then save
    m = StudentManager()
    m.add_student('Aisha Khan', 20, 'Computer Science')
    m.add_student('Rahul Sharma', 22, 'Mathematics')
    m.save_to_file()

    # Run 2: create a new manager, confirm data loaded
    m2 = StudentManager()
    m2.display_all_students() # should show Aisha and Rahul

    # Add another student, confirm ID continues correctly
    s3 = m2.add_student('Priya Mehta', 21, 'Physics')
    print(s3.student_id) # should be SMS-0003, not SMS-0001
