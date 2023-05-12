import os
import random
import requests

# define file paths
book_codes_file = "book_codes.txt"
book_index_file = "book_index.txt"
book_availability_file = "book_availability.txt"
book_list_file = "book_list_pretty.txt"

# check if book codes file exists, create it if not
if not os.path.exists(book_codes_file):
    with open(book_codes_file, 'w') as f:
        f.write("0")

while True:
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

    # fetch book details from Open Library API
    response = requests.get(f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json")
    data = response.json()

    # extract title and author from API response
    book_info = data.get(f"ISBN:{isbn}")
    if book_info:
        title = book_info.get("title", "Unknown Title")
        authors = book_info.get("authors", [])
        author = authors[0]["name"] if authors else "Unknown Author"
    else:
        title = "Unknown Title"
        author = "Unknown Author"

    # add book to book index file with assigned code
    with open(book_index_file, 'a') as f:
        f.write(f"{new_code},{title}\n")

    # add book to pretty list file with assigned code
    with open(book_list_file, 'a') as f:
        f.write(f"Code: {new_code} | Title: {title} | Author: {author} | ISBN: {isbn}\n")

    # add book to book availability file with assigned code
    with open(book_availability_file, 'a') as f:
        f.write(f"{new_code},yes\n")


