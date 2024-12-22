import os
import json

progress_file = "users.json"

"""Class to handle user-related operations."""
class UserManager:
    __users = {}
    progress_file = "users.json"

    
    @staticmethod
    def load_users():
        try:
            if os.path.exists(UserManager.progress_file):
                with open(UserManager.progress_file, "r") as file:
                    UserManager.__users = json.load(file)
            else:
                UserManager.__users = {}
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading user data: {e}")
            UserManager.__users = {}
        return UserManager.__users

    @staticmethod
    def save_users():
        try:
            with open(UserManager.progress_file, "w") as file:
                json.dump(UserManager.__users, file)
        except IOError as e:
            print(f"Error saving user data: {e}")

    @staticmethod
    def add_user(username, password):
        if username in UserManager.__users:
            print("User already exists.")
            return False
        UserManager.__users[username] = {
            "password": password,
            "progress": {},  # Ensure progress is a dictionary
            "statistics": {"completed_lessons": 0, "quiz_accuracy": 0},
        }
        UserManager.save_users()
        return True

        
    @staticmethod
    def authenticate_user(username, password):
        if username not in UserManager.__users:
            print("User does not exist.")
            return False
        # Access the private password variable
        return UserManager.__users[username]["password"] == password
    
class Lesson:
    """Base class for all lessons."""
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def display(self):
        return f"Lesson: {self.title}\nContent: {self.content}"

class Quiz(Lesson):
    """Intermediate class demonstrating multilevel inheritance, inheriting from Lesson."""
    def __init__(self, title, content, questions):
        super().__init__(title, content)
        self.questions = questions

    def take_quiz(self):
        correct = 0
        for question, answer in self.questions:
            user_answer = input(f"{question} (Hint: {answer[0]}) ").strip().lower()
            if user_answer == answer.lower():
                correct += 1
                print("Correct!")
            else:
                print(f"Incorrect. The correct answer is '{answer}'.")
        return f"Quiz completed! You got {correct}/{len(self.questions)} correct."

class LessonProgress:
    """Additional class demonstrating multiple inheritance."""
    def __init__(self):
        self.completed_lessons = {}

    def mark_complete(self, lesson_id):
        self.completed_lessons[lesson_id] = True
        return "Lesson marked as complete!"

class AdvancedQuiz(Quiz, LessonProgress):
    """Derived class showcasing multiple inheritance (Quiz + LessonProgress)."""
    def __init__(self, title, content, questions, lesson_id):
        Quiz.__init__(self, title, content, questions)
        LessonProgress.__init__(self)
        self.lesson_id = lesson_id

    def complete_lesson_and_take_quiz(self):
        print(self.display())
        print(self.take_quiz())
        print(self.mark_complete(self.lesson_id))


# Lessons grouped by categories
lessons = {
    "Python Basics": {
        "1": {
            "name": "Python Syntax",
            "content": """Python syntax defines how Python programs are structured. Python uses indentation to define blocks of code instead of braces or keywords. Statements end with a newline, and the language is case-sensitive.

            Example:
            ```python
            def greet():
            print("Hello, World!")

            greet()
            ```""",
            "quiz": [
                ("What function prints text?", "print"),
                ("What is used to define a block of code?", "indentation"),
            ],
        },
        "2": {
            "name": "Variables",
            "content": """Variables in Python store data values. They are created by assigning values using the '=' operator. Variable names must start with a letter or underscore and cannot contain spaces.

            Example:
            ```python
            name = "Alice"
            age = 25
            print(f"{name} is {age} years old.")
            ```""",
            "quiz": [
                ("What operator assigns values?", "="),
                ("Can variable names start with numbers?", "no"),
            ],
        },
        "3": {
            "name": "Data Types",
            "content": """Python supports data types like integers, floats, strings, booleans, and more. Data types determine the kind of data stored and the operations that can be performed.

            Example:
            ```python
            integer = 10
            floating_point = 3.14
            string = "Hello"
            boolean = True

            print(type(integer), type(floating_point), type(string), type(boolean))
            ```""",
            "quiz": [
                ("What type represents text?", "str"),
                ("What type stores numbers with decimal points?", "float"),
            ],
        },
        "4": {
            "name": "Comments",
            "content": """Comments in Python are used to explain code. They are ignored during execution. Use `#` for single-line comments and triple quotes for multi-line comments.

            Example:
            ```python
            # This is a single-line comment

            '''
            This is a multi-line comment.
            It can span multiple lines.
            '''

            print("Comments help explain code.")
            ```""",
            "quiz": [
                ("What symbol starts a comment?", "#"),
                ("Are comments executed by Python?", "no"),
            ],
        },
        "5": {
            "name": "Numbers",
            "content": """Python supports various types of numbers like integers (int), floating-point numbers (float), and complex numbers. Mathematical operations are supported using operators like +, -, *, and /.

            Example:
            ```python
            a = 10
            b = 3
            print(a + b)  # Addition
            print(a - b)  # Subtraction
            print(a * b)  # Multiplication
            print(a / b)  # Division
            print(a % b)  # Modulus
            ```""",
            "quiz": [
                ("Which type stores decimal numbers?", "float"),
                ("What operator adds numbers?", "+"),
            ],
        },
    },
    "Data Types and Structures": {
        "6": {
            "name": "Strings",
            "content": """Strings are sequences of characters enclosed in quotes. They support operations like concatenation (+), slicing, and methods like upper(), lower(), and split().

            Example:
            ```python
            text = "hello world"
            print(text.upper())      # Convert to uppercase
            print(text.split())      # Split string by spaces
            print(text[:5])          # Slicing the first 5 characters
            ```""",
            "quiz": [
                ("What type represents text?", "string"),
                ("How do you concatenate strings?", "+"),
            ],
        },
        "7": {
            "name": "Booleans",
            "content": """Booleans have two values: True and False. They are used in logical operations and control structures.

            Example:
            ```python
            a = True
            b = False
            print(a and b)   # False
            print(a or b)    # True
            print(not a)     # False
            ```""",
            "quiz": [
                ("What are the two Boolean values?", "True and False"),
                ("What operator returns True if both operands are True?", "and"),
            ],
        },
        "8": {
            "name": "Lists",
            "content": """Lists are ordered collections of items, which can be of any type. Lists are mutable, meaning they can be changed after creation.

            Example:
            ```python
            fruits = ["apple", "banana", "cherry"]
            fruits.append("orange")   # Add an item
            fruits.remove("banana")   # Remove an item
            print(fruits)
            ```""",
            "quiz": [
                ("Are lists mutable?", "yes"),
                ("What method adds an item to a list?", "append"),
            ],
        },
        "9": {
            "name": "Tuples",
            "content": """Tuples are immutable collections of items, which means their values cannot be changed after creation.

            Example:
            ```python
            coordinates = (10, 20)
            print(coordinates[0])  # Accessing elements
            # coordinates[0] = 15  # This will raise an error
            ```""",
            "quiz": [
                ("Are tuples immutable?", "yes"),
                ("How are tuples defined?", "parentheses"),
            ],
        },
        "10": {
            "name": "Sets",
            "content": """Sets store unique, unordered items. They do not allow duplicate values.

            Example:
            ```python
            numbers = {1, 2, 3, 4}
            numbers.add(5)      # Add an element
            numbers.remove(2)   # Remove an element
            print(numbers)
            ```""",
            "quiz": [
                ("Do sets allow duplicates?", "no"),
                ("What function creates a set?", "set"),
            ],
        },
        "11": {
            "name": "Dictionaries",
            "content": """Dictionaries store key-value pairs. Keys must be unique and immutable.

            Example:
            ```python
            person = {"name": "Alice", "age": 25, "city": "New York"}
            print(person["name"])  # Access value by key
            person["job"] = "Engineer"  # Add a new key-value pair
            print(person)
            ```""",
            "quiz": [
                ("What data type uses key-value pairs?", "dictionary"),
                ("Can dictionary keys be mutable?", "no"),
                ("How do you access a value in a dictionary?", "key"),
            ],
        },
    },
        "Operators and Control Flow": {
        "12": {
            "name": "Operators",
            "content": """Operators perform operations on variables and values. Types include arithmetic, comparison, and logical operators.

            Example:
            ```python
            a = 10
            b = 3
            print(a + b)       # Arithmetic: Addition
            print(a == b)      # Comparison: Equals
            print(a > b and b < 5)  # Logical: AND
            ```""",
            "quiz": [
                ("What operator adds values?", "+"),
                ("What operator checks for equality?", "=="),
                ("What operator combines conditions?", "and"),
                ("What operator assigns a value?", "="),
                ("What is the modulus operator?", "%"),
            ],
        },
        "13": {
            "name": "If-Else Statements",
            "content": """If-else statements execute code based on conditions.

            Example:
            ```python
            score = 85
            if score >= 90:
                print("Grade: A")
            elif score >= 80:
                print("Grade: B")
            else:
                print("Grade: C")
            ```""",
            "quiz": [
                ("What keyword starts a condition?", "if"),
                ("What keyword provides an alternative condition?", "elif"),
                ("What keyword specifies the default action?", "else"),
            ],
        },
        "14": {
            "name": "Loops",
            "content": """Loops repeat code. 'for' loops iterate over sequences, while 'while' loops repeat based on conditions.

            Example:
            ```python
            for i in range(5):
                print(i)  # Prints 0 to 4
            count = 0
            while count < 3:
                print("Count:", count)
                count += 1
            ```""",
            "quiz": [
                ("Which loop iterates over a sequence?", "for"),
                ("Which loop continues while a condition is true?", "while"),
                ("What statement exits a loop early?", "break"),
            ],
        },
    },
    "Functions and Advanced Concepts": {
        "15": {
            "name": "Functions",
            "content": """Functions encapsulate reusable code blocks.

            Example:
            ```python
            def greet(name):
                return f"Hello, {name}!"

            print(greet("Alice"))
            ```""",
            "quiz": [
                ("What keyword defines a function?", "def"),
                ("What keyword returns a value from a function?", "return"),
                ("Can functions have default parameter values?", "yes"),
            ],
        },
        "16": {
            "name": "Arrays",
            "content": """Arrays store elements of the same type (from the 'array' module).

            Example:
            ```python
            import array
            arr = array.array('i', [1, 2, 3, 4])
            print(arr)
            arr.append(5)  # Add element
            print(arr)
            ```""",
            "quiz": [
                ("Which module supports arrays?", "array"),
                ("Can arrays store elements of different types?", "no"),
                ("What method adds an element to an array?", "append"),
            ],
        },
        "17": {
            "name": "Inheritance",
            "content": """Inheritance lets a class derive properties from another class.

            Example:
            ```python
            class Animal:
                def speak(self):
                    print("Animal speaks")

            class Dog(Animal):
                def bark(self):
                    print("Woof!")

            dog = Dog()
            dog.speak()  # Inherited method
            dog.bark()
            ```""",
            "quiz": [
                ("What is the base class in inheritance called?", "parent"),
                ("Can a derived class override parent methods?", "yes"),
                ("What keyword is used to inherit from a class?", "class"),
            ],
        },
        "18": {
            "name": "Polymorphism",
            "content": """Polymorphism allows methods to behave differently based on the object.

            Example:
            ```python
            class Cat:
                def sound(self):
                    return "Meow"

            class Dog:
                def sound(self):
                    return "Woof"

            animals = [Cat(), Dog()]
            for animal in animals:
                print(animal.sound())
            ```""",
            "quiz": [
                ("Does polymorphism allow method overriding?", "yes"),
                ("What principle allows a subclass to override a method?", "polymorphism"),
                ("Is polymorphism only used with methods?", "no"),
            ],
        },
        "19": {
            "name": "Exception Handling",
            "content": """Exception handling manages errors during execution.

            Example:
            ```python
            try:
                result = 10 / 0
            except ZeroDivisionError:
                print("Cannot divide by zero!")
            finally:
                print("This block always executes.")
            ```""",
            "quiz": [
                ("What block catches exceptions?", "except"),
                ("What block always executes?", "finally"),
                ("What exception is raised for division by zero?", "ZeroDivisionError"),
            ],
        },
    },
    "NumPy Basics": {
        "20": {
            "name": "NumPy Arrays",
            "content": "NumPy provides powerful tools for array manipulation. Arrays are created using 'numpy.array'. They support advanced operations like broadcasting, slicing, and mathematical computations.",
            "quiz": [
                ("Which library is used for numerical computations?", "numpy"),
                ("What function creates a NumPy array?", "array"),
                ("Can NumPy arrays store multiple data types?", "no"),
            ],
        },
    },
}

def display_menu(current_user):
    print("\n--- Python Learning Program ---")
    if current_user:
        print(f"Logged in as: {current_user}")
        print("1. View Lessons")
        print("2. View Progress")
        print("3. Log Out")
        print("4. Exit")
    else:
        print("1. Log in / Sign up")
        print("2. Exit")
    try:
        return input("Enter your choice: ")
    except EOFError:
        print("Input error! Please try again.")
        return None


def log_in(users):
    try:
        print("\n--- Log In / Sign Up ---")
        username = input("Enter your username: ")
        
        # Load users from UserManager
        all_users = UserManager.load_users()

        if username in all_users:  # Correctly accessing the loaded users
            print("Welcome back, returning user!")
            password = input("Enter your password or type 'reset' to reset it: ")
            
            if password.lower() == "reset":
                print("Resetting your password...")
                new_password = input("Enter your new password: ")
                confirm_password = input("Confirm your new password: ")
                if new_password == confirm_password:
                    all_users[username]["password"] = new_password  # Update password
                    UserManager.save_users()  # Save updated users
                    print("Password reset successfully!")
                    return username
                else:
                    print("Passwords do not match. Please try again.")
                    return None
            
            if UserManager.authenticate_user(username, password):
                print(f"Welcome back, {username}!")
                return username
            else:
                print("Incorrect password. Try again or type 'reset' to reset it.")
                return None
        else:
            print("Username not found. Creating a new account...")
            new_password = input("Set your password: ")
            confirm_password = input("Confirm your password: ")
            if new_password == confirm_password:
                UserManager.add_user(username, new_password)
                print("Account created successfully!")
                return username
            else:
                print("Passwords do not match. Please try again.")
                return None
    except Exception as e:
        print(f"An error occurred during login/signup: {e}")
        return None


class LessonHandler:
    """Class to manage lessons and quizzes."""
    def __init__(self, lessons):
        self.lessons = lessons

    def view_categories(self, progress):
        try:
            while True:
                print("\n--- Categories ---")
                categories = list(self.lessons.keys())
                for i, category in enumerate(categories, start=1):
                    print(f"{i}. {category}")
                print("m. Main Menu")
                choice = input("\nEnter the category number or 'm' to return to the main menu: ")

                if choice.isdigit() and 1 <= int(choice) <= len(categories):
                    category = categories[int(choice) - 1]
                    self.view_lessons(category, progress)
                
                    # Check if all lessons in the category are completed
                    all_completed = all(lesson_id in progress for lesson_id in self.lessons[category].keys())
                    if all_completed:
                        print(f"\n🎉 Congratulations! You've completed all the lessons in '{category}'! 🎉")
                elif choice.lower() == 'm':
                    return
                else:
                    print("Invalid choice!")
        except Exception as e:
            print(f"An error occurred: {e}")


    def view_lessons(self, category, progress):
        try:
            while True:
                print(f"\n--- {category} Lessons ---")
                for lesson_id, lesson in self.lessons[category].items():
                    status = "✅" if lesson_id in progress else "❌"
                    print(f"{lesson_id}. {lesson['name']} {status}")
                print("m. Main Menu")

                choice = input("\nEnter the lesson number to view or 'm' to return to the main menu: ")
                if choice in self.lessons[category]:
                    self.view_lesson(category, choice, progress)
                elif choice.lower() == "m":
                    return
                else:
                    print("Invalid choice!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def view_lesson(self, category, lesson_id, progress):
        try:
            lesson = self.lessons[category][lesson_id]
            print(f"\n--- {lesson['name']} ---")
            print(lesson["content"])
            input("\nPress Enter to take the quiz...")

            correct = 0
            for question, answers in lesson["quiz"]:
                user_answer = input(f"{question} ").strip().lower()  # Convert user input to lowercase
                if isinstance(answers, list):
                    # Convert all possible correct answers to lowercase for case-insensitive comparison
                    if user_answer.lower() in [ans.lower() for ans in answers]:
                        correct += 1
                        print("Correct!")
                    else:
                        print(f"Incorrect. Acceptable answers are: {', '.join(answers)}")
                else:
                    # Handle single-answer case
                    if user_answer == answers.lower():
                        correct += 1
                        print("Correct!")
                    else:
                        print(f"Incorrect. The correct answer is '{answers}'.")

            print(f"\nQuiz completed! You got {correct}/{len(lesson['quiz'])} correct.")
            if correct == len(lesson["quiz"]):
                progress[lesson_id] = True
                print("Lesson marked as complete!")
        except Exception as e:
            print(f"An error occurred while viewing the lesson: {e}")

def log_out():
    print("\n--- Logging Out ---")
    print("You have been logged out successfully. Returning to the main menu...")
    return None  # Clears the current user session


class UserProgress:
    """Class to manage user progress."""
    def __init__(self, username, lessons):
        self.username = username
        # self.users = users
        self.lessons = lessons  # Added lessons as an instance variable

    def view_progress(self):
        try:
            user_data = UserManager._UserManager__users.get(self.username)
            if not user_data:
                print(f"User '{self.username}' does not exist or has no progress data.")
                return
        
            print(f"\n--- {self.username}'s Progress ---")
            progress = user_data.get("progress", {})
        
            for category, lessons_data in self.lessons.items():
                print(f"{category}:")
                if not isinstance(lessons_data, dict):
                    print("Invalid lesson data format.")
                    continue
                for lesson_id, lesson in lessons_data.items():
                    if not isinstance(lesson, dict):
                        print(f"Invalid lesson format for lesson ID {lesson_id}")
                        continue
                    status = "Completed" if lesson_id in progress else "Not Completed"
                    print(f"  {lesson['name']}: {status}")
        except Exception as e:
            print(f"An error occurred while viewing progress: {e}")


def main():
    users = UserManager.load_users()  # Now this will correctly load the users dictionary
    current_user = None
    lesson_handler = LessonHandler(lessons)

    while True:
        try:
            choice = display_menu(current_user)
            if current_user:
                if current_user not in UserManager._UserManager__users:
                    print("User session invalid. Please log in again.")
                    current_user = None
                    continue
                if choice == "1":
                    progress = UserManager._UserManager__users[current_user].get("progress", {})
                    lesson_handler.view_categories(progress)
                elif choice == "2":
                    progress = UserManager._UserManager__users[current_user].get("progress", {})
                    UserProgress(current_user, lessons).view_progress()
                elif choice == "3":
                    current_user = log_out()
                elif choice == "4":
                    print("Saving progress and exiting. Goodbye!")
                    UserManager.save_users()
                    break
                else:
                    print("Invalid choice! Please try again.")
            else:
                if choice == "1":
                    current_user = log_in(users)
                elif choice == "2":
                    print("Exiting the program. Goodbye!")
                    break
                else:
                    print("Invalid choice! Please try again.")
        except KeyboardInterrupt:
            print("\nExiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
