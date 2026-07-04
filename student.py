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
        percentage = self.get_percentage()

        for min_mark, grade in self.grade_scale:
          if percentage >= min_mark:
             return grade
          
        return 'F'
       
    def is_passing(self):
      if self.get_percentage() >= 45:
         return True
      else:
         return False 
      
    def __str__(self):
       return f"[{self.student_id}] {self.name} | Age: {self.age} | Course: {self.course}"


    def to_csv_row(self):
       marks_str = ';'.join(f"{subject}:{mark}" for subject, mark in self.marks.items())
       return [self.student_id, self.name, self.age, self.course, marks_str]
       

    @staticmethod
    def from_csv_row(row):
       student_id, name, age, course, marks_str = row
       marks = dict()

       if marks_str:
          for i in marks_str.split(';'):
             if i:
                subject, mark = i.split(':')
                marks[subject] = int(mark)
                
       return Student(student_id=student_id, name=name, age=int(age), course=course, marks=marks)


# if __name__ == '__main__':
 
#  s = Student('SMS-0001', 'Aisha', 20, 'CS', {'Maths': 44, 'English': 44})
#  print(s.student_id, s.name, s.marks)
#  print(s.get_percentage())
#  print(s.get_grade())
#  print(s.is_passing())
#  print(s)

# row = s.to_csv_row()
# print(row)

# s2 = Student.from_csv_row(row)
# print(s2.name, s2.marks)