from datetime import date, timedelta
import json

DATA_FILE = "library_data.json"
RECORDS_FILE = "borrowing_records.txt"

default_books = [
    {
        "id": 101,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "available": True,
        "borrower": None,
        "borrow_date": None,
        "due_date": None
    },
    {
        "id": 102,
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "available": True,
        "borrower": None,
        "borrow_date": None,
        "due_date": None
    }
]

default_records = []

def load_data():
    global books
    global borrowing_records

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

            books = data["books"]
            borrowing_records = data["borrowing_records"]

            # Convert stored date strings back to date objects
            for book in books:

                if book["borrow_date"] is not None:
                    book["borrow_date"] = date.fromisoformat(
                        book["borrow_date"]
                    )

                if book["due_date"] is not None:
                    book["due_date"] = date.fromisoformat(
                        book["due_date"]
                    )

            for record in borrowing_records:

                if record["borrow_date"] is not None:
                    record["borrow_date"] = date.fromisoformat(
                        record["borrow_date"]
                    )

                if record["due_date"] is not None:
                    record["due_date"] = date.fromisoformat(
                        record["due_date"]
                    )

                if record["return_date"] is not None:
                    record["return_date"] = date.fromisoformat(
                        record["return_date"]
                    )

            print("Library data loaded successfully.")

    except FileNotFoundError:

        books = default_books.copy()
        borrowing_records = default_records.copy()

        save_data()

        print("New library data created.")

def save_data():

    data = {
        "books": [],
        "borrowing_records": []
    }

    # Convert book dates to strings
    for book in books:

        book_copy = book.copy()

        if book_copy["borrow_date"] is not None:
            book_copy["borrow_date"] = str(book_copy["borrow_date"])

        if book_copy["due_date"] is not None:
            book_copy["due_date"] = str(book_copy["due_date"])

        data["books"].append(book_copy)

    # Convert record dates to strings
    for record in borrowing_records:

        record_copy = record.copy()

        if record_copy["borrow_date"] is not None:
            record_copy["borrow_date"] = str(record_copy["borrow_date"])

        if record_copy["due_date"] is not None:
            record_copy["due_date"] = str(record_copy["due_date"])

        if record_copy["return_date"] is not None:
            record_copy["return_date"] = str(record_copy["return_date"])

        data["borrowing_records"].append(record_copy)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_book():

    try:
        book_id = int(input("Enter book ID: "))

    except ValueError:
        print("Book ID must be a number.")
        return

    # Check duplicate ID
    for book in books:

        if book["id"] == book_id:
            print("A book with this ID already exists.")
            return

    title = input("Enter book title: ")
    author = input("Enter author name: ")

    book = {
        "id": book_id,
        "title": title,
        "author": author,
        "available": True,
        "borrower": None,
        "borrow_date": None,
        "due_date": None
    }

    books.append(book)

    save_data()

    print("Book added successfully!")
    
def search_book():
    search_title = input("Enter book title to search: ")

    for book in books:
        if book["title"].lower() == search_title.lower():
            print("\nBook found!")
            print("ID:", book["id"])
            print("Title:", book["title"])
            print("Author:", book["author"])

            if book["available"]:
                print("Status: Available")
            else:
                print("Status: Borrowed")
                print("Borrower:", book["borrower"])
                print("Due Date:", book["due_date"])

            return

    print("Book not found.")

def borrow_book():

    try:
        book_id = int(input("Enter book ID to borrow: "))

    except ValueError:
        print("Book ID must be a number.")
        return

    borrower = input("Enter borrower name: ")

    for book in books:

        if book["id"] == book_id:

            # Check availability
            if not book["available"]:

                print("Sorry, this book is already borrowed.")
                print("Current borrower:", book["borrower"])
                print("Due date:", book["due_date"])

                return

            borrow_date = date.today()
            due_date = borrow_date + timedelta(days=7)

            # Update current book information
            book["available"] = False
            book["borrower"] = borrower
            book["borrow_date"] = borrow_date
            book["due_date"] = due_date

            # Create borrowing record
            record = {
                "book_id": book["id"],
                "book_title": book["title"],
                "borrower": borrower,
                "borrow_date": borrow_date,
                "due_date": due_date,
                "return_date": None,
                "overdue": None
            }

            borrowing_records.append(record)

            # Save immediately
            save_data()

            print("\nBook borrowed successfully!")
            print("Book:", book["title"])
            print("Borrower:", borrower)
            print("Borrow Date:", borrow_date)
            print("Due Date:", due_date)

            return

    print("Book not found.")

def return_book():

    try:
        book_id = int(input("Enter book ID to return: "))

    except ValueError:
        print("Book ID must be a number.")
        return

    for book in books:

        if book["id"] == book_id:

            if book["available"]:

                print("This book is already available in the library.")
                return

            return_date = date.today()

            # Find active borrowing record
            for record in borrowing_records:

                if (
                    record["book_id"] == book_id
                    and record["return_date"] is None
                ):

                    record["return_date"] = return_date

                    if return_date > record["due_date"]:
                        record["overdue"] = True
                    else:
                        record["overdue"] = False

                    break

            # Update current book status
            book["available"] = True
            book["borrower"] = None
            book["borrow_date"] = None
            book["due_date"] = None

            # Save immediately
            save_data()

            print("\nBook returned successfully!")
            print("Book:", book["title"])
            print("Return Date:", return_date)

            return

    print("Book not found.")

def show_overdue_books():
    today = date.today()
    found = False

    print("\n--- Overdue Books ---")

    for book in books:

        if not book["available"]:

            if today > book["due_date"]:

                print("Book ID:", book["id"])
                print("Title:", book["title"])
                print("Borrower:", book["borrower"])
                print("Due Date:", book["due_date"])
                print()

                found = True

    if not found:
        print("No overdue books.")

def library_summary():
    total_books = len(books)
    available_books = 0
    borrowed_books = 0

    for book in books:

        if book["available"]:
            available_books += 1
        else:
            borrowed_books += 1

    print("\n--- Library Summary ---")
    print("Total books:", total_books)
    print("Available books:", available_books)
    print("Borrowed books:", borrowed_books)

def show_borrowing_records():
    print("\n--- Borrowing Records ---")

    if len(borrowing_records) == 0:
        print("No borrowing records found.")
        return

    for record in borrowing_records:

        print("Book ID:", record["book_id"])
        print("Book:", record["book_title"])
        print("Borrower:", record["borrower"])
        print("Borrow Date:", record["borrow_date"])
        print("Due Date:", record["due_date"])
        print("Return Date:", record["return_date"])
        print("Overdue:", record["overdue"])
        print("-----------------------------")

def save_records():
    with open(RECORDS_FILE, "w") as file:

        if len(borrowing_records) == 0:
            file.write("No borrowing records found.\n")
        else:

            for record in borrowing_records:

                file.write("Book ID: " + str(record["book_id"]) + "\n")
                file.write("Book: " + record["book_title"] + "\n")
                file.write("Borrower: " + record["borrower"] + "\n")
                file.write("Borrow Date: " + str(record["borrow_date"]) + "\n")
                file.write("Due Date: " + str(record["due_date"]) + "\n")
                file.write("Return Date: " + str(record["return_date"]) + "\n")
                file.write("Overdue: " + str(record["overdue"]) + "\n")
                file.write("-----------------------------\n")

    print("Borrowing records saved to borrowing_records.txt")

def main():

    load_data()

    while True:

        print("\n==============================")
        print("     MINI LIBRARY SYSTEM")
        print("==============================")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show Overdue Books")
        print("6. Library Summary")
        print("7. Show Borrowing Records")
        print("8. Save Records")
        print("9. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()

        elif choice == "2":
            search_book()

        elif choice == "3":
            borrow_book()

        elif choice == "4":
            return_book()

        elif choice == "5":
            show_overdue_books()

        elif choice == "6":
            library_summary()

        elif choice == "7":
            show_borrowing_records()

        elif choice == "8":
            save_records()

        elif choice == "9":
            save_data()
            save_records()
            print("Thank you for using the Mini Library System!")
            break

        else:
            print("Invalid choice. Please try again.")

main()