# BB&N English Course Selection Sorting Program

import csv

class Student:
    # constants for class size range
    MAX_CLASS_SIZE = 15
    MIN_CLASS_SIZE = 11

    # constants for class score calculations
    FIRST_IMPORTANCE = 40
    SECOND_IMPORTANCE = 30
    LARGE_CLASS_IMPORTANCE = -100
    SMALL_CLASS_IMPORTANCE = 40
    GENDER_IMPORTANCE = 50
    NOT_SELECETD_CLASS_IMPORTANCE = -100
    NO_PREFERENCE_IMPORTANCE = 0
    
    def __init__(self, name, first, second, third, gender):
        self.name = name
        self.first = int(first) - 1
        self.second = int(second) - 1
        self.third = int(third) - 1
        self.gender = gender

    def is_male(self):
        return self.gender == 'M'

    def is_female(self):
        return self.gender == 'F'

    def is_other_gender(self):
        return self.gender == 'O'

    def calculate_class_score(self, klass, klass_id):
        score = 0
        
        # prioritize class size
        if len(klass) > self.MAX_CLASS_SIZE: # deprioritize large class
            return self.LARGE_CLASS_IMPORTANCE
        if len(klass) < self.MIN_CLASS_SIZE: # prioritize small class
            score += self.SMALL_CLASS_IMPORTANCE
        score += 2 * (self.MAX_CLASS_SIZE - len(klass))**2 # prioritize smaller classes within range

        # prioritize first/second/third choice
        if klass_id == self.first: # prioritize first choice
            score += self.FIRST_IMPORTANCE
        elif klass_id == self.second: # prioritize second choice
            score += self.SECOND_IMPORTANCE
        elif self.first < 0 or self.second < 0 or self.third < 0: # no prioritization for no preference
            score += self.NO_PREFERENCE_IMPORTANCE
        elif klass_id != self.third: # deprioritize non choice
            return self.NOT_SELECETD_CLASS_IMPORTANCE
        
        # prioritize gender balance
        males = len([1 for student in klass if student.is_male()]) # number of males
        females = len([1 for student in klass if student.is_female()]) # number of females
        if males > females:
            if self.is_male():
                score -= self.GENDER_IMPORTANCE # deprioritize males in male-heavy class
            else:
                score += self.GENDER_IMPORTANCE # prioritize females in male-heavy class
        elif females > males:
            if self.is_male():
                score += self.GENDER_IMPORTANCE # prioritize males in female-heavy class
            else:
                score -= self.GENDER_IMPORTANCE # deprioritize females in female-heavy class
    
        return score

# get data from csv
firstLine = True
students = []
with open('CourseSelectionData.csv', newline='') as f:
    reader = csv.reader(f)
    for student_row in reader:
        if firstLine: # skip first line (labels)
            firstLine = False
            continue
        students.append(Student(student_row[0], student_row[1], student_row[2], student_row[3], student_row[4]))

# count number of classes
num_classes = []
for student in students:
    num_classes.extend([student. first,student.second, student.third])
for num in num_classes:
    if num == -1:
        num_classes.remove(num)

# first sort
klasses = []
for i in range(len(set(num_classes))):
    klasses.append([])
for student in students:
    scores = []
    for i, klass in enumerate(klasses):
        scores.append(student.calculate_class_score(klass, i)) # get scores for each student in each class

    klasses[scores.index(max(scores))].append(student) # choose class with highest score for student in class

# resort (rearrange students and reevaluate scores)
for i in range(100):
    for klass_out in klasses:
        temp_class = klass_out[:]
        for t,student in enumerate(temp_class):
            klass_out.pop(0)
            scores = []
            for i,klass in enumerate(klasses):
                scores.append(student.calculate_class_score(klass,i))            
            klasses[scores.index(max(scores))].append(student)

# print classes in output file
outfile = open("english_courses_output.txt", "w") # clear previous text
outfile.close()
outfile = open("english_courses_output.txt", "a")
outfile.write("SORTED BB&N ENGLISH COURSES (M/F/O)")
for i,klass in enumerate(klasses):
    outfile.write("\n\n{} ({}/{}/{})".format(i + 1, len([1 for student in klass if student.is_male()]), len([1 for student in klass if student.is_female()]), len([1 for student in klass if student.is_other_gender()])))
    for student in klasses[i]:
        student_choice = 0
        if student.first == i or student.first < 0:
            student_choice = 1
        elif student.second == i or student.second < 0:
            student_choice = 2
        elif student.third == i or student.third < 0:
            student_choice = 3
        outfile.write("\n" + student.name + " (" + student.gender + ") - " + str(student_choice))
outfile.write("\n\n")
outfile.close()
