import csv
import statistics

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.scores = []

    def add_score(self, score):
        if 0 <= score <= 20:  # اعتبارسنجی نمره
            self.scores.append(score)
        else:
            print("❌ Invalid score. Please enter a score between 0 and 20.")

    def average_score(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0

    def highest_score(self):
        return max(self.scores) if self.scores else None

    def lowest_score(self):
        return min(self.scores) if self.scores else None

    def median_score(self):
        return statistics.median(self.scores) if self.scores else None


class StudentManager:
    def __init__(self):
        self.students = {}

    def load_from_file(self):
        try:
            with open("students.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the first row with column headers
                for row in reader:
                    student_id = row[0]
                    name = row[1]
                    scores = list(map(float, row[2].split(',')))  # Convert scores from string to float
                    student = Student(student_id, name)
                    student.scores = scores
                    self.students[student_id] = student
        except FileNotFoundError:
            pass  # If the file does not exist, nothing happens

    def save_to_file(self):
        with open("students.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Scores"])  # Column headers
            for student in self.students.values():
                writer.writerow([student.student_id, student.name, ','.join(map(str, student.scores))])

    def backup_data(self):
        with open("students_backup.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Scores"])  # Column headers
            for student in self.students.values():
                writer.writerow([student.student_id, student.name, ','.join(map(str, student.scores))])
        print("✅ Data backed up successfully.")

    def restore_data(self):
        self.load_from_file()
        print("✅ Data restored successfully.")

    def add_student(self):
        student_id = input("Enter student ID: ")
        name = input("Enter student name: ")
        student = Student(student_id, name)
        
        while True:
            score = input("Enter a score for the student (press Enter without typing to stop): ")
            if score == "":  # If Enter is pressed without typing anything, stop entering scores
                break
            try:
                score = float(score)
                student.add_score(score)
            except ValueError:
                print("❌ Invalid input. Please enter a valid number for the score.")
        
        self.students[student_id] = student
        print("✅ Student added successfully.")

    def view_students(self):
        if not self.students:
            print("❌ No students are registered.")
        else:
            for student in self.students.values():
                print(f"ID: {student.student_id}, Name: {student.name}, Scores: {student.scores}, "
                      f"Average: {student.average_score():.2f}, Highest: {student.highest_score()}, "
                      f"Lowest: {student.lowest_score()}")

    def search_student(self):
        search_id = input("Enter student ID or name to search: ")
        found = False
        for student in self.students.values():
            if search_id in student.student_id or search_id.lower() in student.name.lower():
                print(f"ID: {student.student_id}, Name: {student.name}, Scores: {student.scores}, "
                      f"Average: {student.average_score():.2f}")
                found = True
        if not found:
            print("❌ No student found with the given ID or name.")

    def delete_student(self):
        student_id = input("Enter the student ID you want to delete: ")
        if student_id in self.students:
            del self.students[student_id]
            print("✅ Student deleted successfully.")
        else:
            print("❌ Student with this ID not found.")

    def edit_score(self):
        student_id = input("Enter the student ID whose scores you want to edit: ")
        if student_id in self.students:
            new_score = input("Enter the new score to add: ")
            try:
                new_score = float(new_score)
                self.students[student_id].add_score(new_score)
                print("✅ Score added successfully.")
            except ValueError:
                print("❌ Invalid input.")
        else:
            print("❌ Student with this ID not found.")

    def calculate_student_average(self):
        student_id = input("Enter the student ID whose average you want to calculate: ")
        if student_id in self.students:
            average = self.students[student_id].average_score()
            print(f"Average score for {self.students[student_id].name}: {average:.2f}")
        else:
            print("❌ Student with this ID not found.")

    def calculate_average(self):
        if not self.students:
            print("❌ No students are registered.")
        else:
            total_scores = 0
            total_students = 0
            for student in self.students.values():
                total_scores += sum(student.scores)
                total_students += len(student.scores)
            average = total_scores / total_students if total_students > 0 else 0
            print(f"Average score of all students: {average:.2f}")

    def rank_students(self):
        if not self.students:
            print("❌ No students are registered.")
        else:
            ranked_students = sorted(self.students.values(), key=lambda student: student.average_score(), reverse=True)
            print("Ranking of students based on average score:")
            for rank, student in enumerate(ranked_students, start=1):
                print(f"{rank}. {student.name} - Average: {student.average_score():.2f}")


def main():
    manager = StudentManager()
    manager.load_from_file()

    while True:
        print("\n------ Student Grade Management Menu ------")
        print("1. Add a new student")
        print("2. View list of students")
        print("3. Search for a student")
        print("4. Edit student scores")
        print("5. Delete student")
        print("6. Calculate average score for a student")
        print("7. Calculate average score for all students")
        print("8. Rank students by average score")
        print("9. Backup data")
        print("10. Restore data")
        print("11. Save data to file")
        print("12. Exit")
        
        choice = input("Choose an option (1-12): ")
        
        if choice == "1":
            manager.add_student()
        elif choice == "2":
            manager.view_students()
        elif choice == "3":
            manager.search_student()
        elif choice == "4":
            manager.edit_score()
        elif choice == "5":
            manager.delete_student()
        elif choice == "6":
            manager.calculate_student_average()
        elif choice == "7":
            manager.calculate_average()
        elif choice == "8":
            manager.rank_students()
        elif choice == "9":
            manager.backup_data()
        elif choice == "10":
            manager.restore_data()
        elif choice == "11":
            manager.save_to_file()
            print("✅ Data saved to file successfully.")
        elif choice == "12":
            print("Exiting the program...")
            break
        else:
            print("❌ Invalid selection.")

if __name__ == "__main__":
    main()
