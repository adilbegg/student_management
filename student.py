class Student:

    grade_scale = [(90, 'A'), (75, 'B'), (60, 'C'), (45, 'D'), (0, 'F')]

    def __init__(self, student_id, name, age, course, marks=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks or {}

    def get_percentage(self):
       sum = 0
       if len(self.marks):
        for key, value in self.marks.items():
           sum += value
        return sum/len(self.marks)
       
       else:
          return 0
        
    def get_grade(self):
       
       for min_mark, grade in self.grade_scale:
          if self.get_percentage() >= min_mark:
             return grade
       

if __name__ == '__main__':
 s = Student('SMS-0001', 'Aisha', 20, 'CS', {'Maths': 44, 'English': 44})
 print(s.student_id, s.name, s.marks)
 print(s.get_percentage())
 print(s.get_grade())