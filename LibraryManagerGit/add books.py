import os
import random
import requests

# Define file paths
book_codes_file = "book_codes.txt"
book_index_file = "book_index.txt"
book_availability_file = "book_availability.txt"
book_list_file = "book_list_pretty.txt"

while True:
    # Get book details from user
    isbn = input("Enter the ISBN of the book (or 'q' to quit): ")
    
    new_code = input("Enter the code you wish to assign: ") 

    if isbn.lower() == 'exit':
        break

    # Make request to Open Library API
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    response = requests.get(url)

    if response.status_code == 200:
        book_data = response.json()
        title = book_data.get("title")

    else:
        print("Failed to retrieve book details from Open Library. Using default values.")
        title = "Unknown Title"

    # Add book to book index file with assigned code
    with open(book_index_file, 'a') as f:
        f.write(f"{new_code},{title}\n")

    # Add book to pretty list file with assigned code
    with open(book_list_file, 'a') as f:
        f.write(f"Code: {new_code} | Title: {title} | ISBN: {isbn}\n")

    # Add book to book availability file with assigned code
    with open(book_availability_file, 'a') as f:
        f.write(f"{new_code},yes\n")
