# Fiero Washington
#CIS261
#WK!) VIBE Coding

from pathlib import Path


DATA_FILE = Path("student_grades.txt")


class Student:
	"""Store a student's identifying information and calculated grade."""

	def __init__(self, name, student_id, test1, test2, test3):
		self.name = name
		self.student_id = student_id
		self.test_scores = [float(test1), float(test2), float(test3)]
		self.average = sum(self.test_scores) / len(self.test_scores)
		self.grade = calculate_letter_grade(self.average)

	def to_file_line(self):
		scores = "|".join(f"{score:.2f}" for score in self.test_scores)
		return f"{self.name}|{self.student_id}|{scores}|{self.average:.2f}|{self.grade}\n"


def calculate_letter_grade(average):
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def load_students():
	students = []
	try:
		with DATA_FILE.open("r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					student = Student(fields[0], fields[1], fields[2], fields[3], fields[4])
				except ValueError:
					print(f"Skipping record with invalid scores on line {line_number}.")
					continue
				students.append(student)
	except FileNotFoundError:
		return students
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def save_students(students):
	try:
		with DATA_FILE.open("w", encoding="utf-8") as file:
			file.writelines(student.to_file_line() for student in students)
		print(f"Saved {len(students)} student record(s) to {DATA_FILE}.")
	except OSError as error:
		print(f"Could not save student records: {error}")


def prompt_for_score(test_number):
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	if not name or not student_id or "|" in name or "|" in student_id:
		print("Name and ID are required and cannot contain '|'.")
		return
	scores = [prompt_for_score(number) for number in range(1, 4)]
	student = Student(name, student_id, *scores)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("No student records found.")
		return
	print("\nStudent Records")
	print(f"{'Name':<20} {'ID':<12} {'Test 1':>8} {'Test 2':>8} {'Test 3':>8} {'Average':>9} {'Grade':>5}")
	print("-" * 76)
	for student in students:
		print(
			f"{student.name:<20.20} {student.student_id:<12.12} "
			f"{student.test_scores[0]:>8.2f} {student.test_scores[1]:>8.2f} "
			f"{student.test_scores[2]:>8.2f} {student.average:>9.2f} {student.grade:>5}"
		)


def display_statistics(students):
	if not students:
		print("No student records found.")
		return
	averages = [student.average for student in students]
	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	print("\nClass Statistics")
	print(f"Highest average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest average:  {lowest.average:.2f} ({lowest.name})")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = input("\nEnter student name to search: ").strip().casefold()
	matches = [student for student in students if student.name.casefold() == search_name]
	if not matches:
		print("No student found with that name.")
		return
	display_students(matches)


def display_menu():
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Display class statistics")
	print("4. Search by name")
	print("5. Save records")
	print("Press ESC at the menu prompt to save and exit.")


def main():
	students = load_students()
	print(f"Loaded {len(students)} student record(s).")
	while True:
		display_menu()
		choice = input("Choose an option: ")
		if choice == "\x1b":
			save_students(students)
			print("Goodbye!")
			return
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Invalid option. Choose 1-5 or press ESC to exit.")


if __name__ == "__main__":
	main()




