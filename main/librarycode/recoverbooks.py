book_list_file = "book_list_pretty.txt"
book_index_file = "book_index.txt"
book_availability_file = "book_availability.txt"

# Open the book list file
with open(book_list_file, 'r') as f:
    lines = f.readlines()

# Process each line in the file
for line in lines:
    parts = line.strip().split("|")
    if len(parts) >= 3:
        code = parts[0].strip().split(":")[1].strip()
        title = parts[1].strip().split(":")[1].strip()
        isbn = parts[2].strip().split(":")[1].strip()
        availability = "yes"  # Set default availability as "yes"

        # Update book index file with assigned code and title
        with open(book_index_file, 'a') as index_file:
            index_file.write(f"{code},{title}\n")

        # Update book availability file with assigned code and availability
        with open(book_availability_file, 'a') as availability_file:
            availability_file.write(f"{code},{availability}\n")

        # Print the extracted data (optional)
        print(f"Code: {code} | Title: {title} | ISBN: {isbn}")
