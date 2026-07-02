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

