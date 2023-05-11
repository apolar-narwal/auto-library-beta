import os
import random
import requests

# define file paths
book_codes_file = "book_codes.txt"
book_index_file = "book_index.txt"
book_availability_file = "book_availability.txt"
book_list_file = "book_list_pretty.txt"

while True:
    # check if book codes file exists - create if it doesn't
    if not os.path.exists(book_codes_file):
        with open(book_codes_file, 'w') as f:
            f.write("0")

    # read current book code from file
    with open(book_codes_file, 'r') as f:
        contents = f.read().strip()
        if contents:
            current_code = int(contents)
        else:
            current_code = 0

    # generate new book code
    new_code = random.randint(10000, 99999)
    while new_code <= current_code:
        new_code = random.randint(10000, 99999)

    # update book codes file with new current code
    with open(book_codes_file, 'w') as f:
        f.write(str(new_code))

    # get book details from user
    isbn = input("Enter the ISBN of the book (or 'q' to quit): ")
    if isbn.lower() == 'q':
        break

    # Fetch book details from the web using the ISBN
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch book details. Please try again.")
        continue

    book_data = response.json()
    title = book_data['title']
    author = book_data['author']

    # add book to book index file with assigned code
    with open(book_index_file, 'a') as f:
        f.write(f"{new_code},{title}\n")

    # add book to pretty list with assigned code
    with open(book_list_file, 'a') as f:
        f.write(f"Code: {new_code} | Title: {title} | Author: {author} | ISBN: {isbn}\n")

    # add book to book availability file with assigned code
    with open(book_availability_file, 'a') as f:
        f.write(f"{new_code},yes\n")

    print("Book added successfully.")

print("Program terminated.")