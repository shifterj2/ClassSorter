import csv
import argparse

class Student:
    # constants for class size range
    MAX_CLASS_SIZE = 15
    MIN_CLASS_SIZE = 11

    # constants for class score calculations
    LARGE_CLASS_IMPORTANCE = -100
    SMALL_CLASS_IMPORTANCE = 40
    GENDER_IMPORTANCE = 50
    NOT_SELECETD_CLASS_IMPORTANCE = -100
    
    def __init__(self, name, preferences, gender):
        self.name = name
        self.preferences = [int(i) - 1 for i in preferences]
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
        found_class = False
        priority_importance = len(self.preferences) * 10;
        for index, choice in enumerate(self.preferences):
            if klass_id == choice:
                score += priority_importance - index * 10
                found_class = True
                break
        if not found_class:
            score += self.NOT_SELECETD_CLASS_IMPORTANCE
        
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
def create_students(selection_data, students):
    firstLine = True
    with open(selection_data, newline='') as f:
        reader = csv.reader(f)
        for student_row in reader:
            if firstLine:
                firstLine = False
                continue
            preferences = [student_row[i+1] for i in range(len(student_row)-2)]
            students.append(Student(student_row[0], preferences, student_row[-1]))

# count number of classes
def count_classes(students, num_classes):
    for student in students:
        num_classes.extend(student.preferences)
    for num in num_classes:
        if num == -1:
            num_classes.remove(num);

# first sort
def first_sort(students, klasses, num_classes):
    for i in range(len(set(num_classes))):
        klasses.append([])
    for student in students:
        scores = []
        for i, klass in enumerate(klasses):
            scores.append(student.calculate_class_score(klass, i)) # get scores for each student in each class

        klasses[scores.index(max(scores))].append(student) # choose class with highest score for student in class

# resort (rearrange students and reevaluate scores) a given number of times
def sort_again(students, klasses, iterations):
    for i in range(iterations):
        for klass_out in klasses:
            temp_class = klass_out[:]
            for t,student in enumerate(temp_class):
                klass_out.pop(0)
                scores = []
                for i,klass in enumerate(klasses):
                    scores.append(student.calculate_class_score(klass,i))            
                klasses[scores.index(max(scores))].append(student)

#print results in outfile
def write_outfile(outfile_name, klasses):
    outfile = open(outfile_name, "w") # clear previous text
    outfile.close()
    outfile = open(outfile_name, "a")
    outfile.write("Sorted Classes")
    for i,klass in enumerate(klasses):
        outfile.write("\n\n{} ({}/{}/{})".format(i + 1, len([1 for student in klass if student.is_male()]), len([1 for student in klass if student.is_female()]), len([1 for student in klass if student.is_other_gender()])))
        for student in klasses[i]:
            student_choice = 0
            for index, preference in enumerate(student.preferences):
                if preference == i or preference < 0:
                    student_choice = index + 1
            outfile.write("\n" + student.name + " (" + student.gender + ") - " + str(student_choice))
    outfile.write("\n\n")
    outfile.close()

def main(students, klasses, num_classes, iterations, selection_data, outfile_name):
    create_students(selection_data, students)
    count_classes(students, num_classes)
    first_sort(students, klasses, num_classes)
    sort_again(students, klasses, iterations)
    write_outfile(outfile_name, klasses);

parser = argparse.ArgumentParser(description='Sort students into preferred classes.')
parser.add_argument('--input', dest='input_file', default="CourseSelectionData.csv",
    help='valid input csv')
parser.add_argument('--output', dest='output_file', default="classes_output",
    help='valid output csv')
args = parser.parse_args()

students = []
num_classes = []
klasses = []
iterations = 100

main(students, klasses, num_classes, iterations, args.input_file, args.output_file)
