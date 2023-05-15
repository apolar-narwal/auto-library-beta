lending_file = 'lending.txt'

lending_data = {}
with open(lending_file, 'r') as f:
    for line in f:
        data = line.strip().split(',')
        if len(data) >= 5:
            name, email, code, book_title, timestamp = data
            lending_data[book_title] = {
                'name': name,
                'email': email,
                'book_title': book_title,
                'timestamp': timestamp
            }
        else:
            # Handle the case where the line does not have enough values
            print(f"Invalid line: {line}")