from flask import Flask, render_template, request

app = Flask(__name__)

# Define the paths to text files
lending_file = 'lending.txt'
index_file = 'book_index.txt'
list_file = 'book_list_pretty.txt'
availability_file = 'book_availability.txt'

# Read the lending file and create a dictionary to map codes to lending information
lending_data = {}
with open(lending_file, 'r') as f:
    for line in f:
        name, email, code, book_title, timestamp = line.strip().split(',',1)
        lending_data[code] = {
            'name': name,
            'email': email,
            'code': code,
            'book_title': book_title,
            'timestamp': timestamp
        }

# Read the index file and create a dictionary to map titles to codes
book_index = {}
with open(index_file, 'r') as f:
    for line in f:
        code, title = line.strip().split(',', 1)
        book_index[title] = code

# Read the list file and populate the books data structure
books = []
with open(index_file, 'r') as f:
    for line in f:
        code, _ = line.strip().split(',', 1)
        title = book_index.get(code, '')
        books.append({"code": code, "title": title})

# Read the availability file and update the availability for each book
with open(availability_file, 'r') as f:
    for line in f:
        code, availability = line.strip().split(',', )
        book = next((book for book in books if book['code'] == code), None)
        if book:
            book['availability'] = availability

@app.route('/')
def home():
    text_files = [lending_file, index_file, list_file, availability_file]
    file_content = {}

    for file in text_files:
        with open(file, 'r') as f:
            content = f.read()
            file_content[file] = content

    search_query = request.args.get('search')

    search_results = []
    search_results_index = []

    if search_query:
        if search_query.isdigit():
            book = next((book for book in books if book['code'] == search_query), None)
            if book:
                if book['code'] in lending_data:
                    lending_info = lending_data[book['code']]
                    search_results_index.append({
                        'book_title': book['title'],
                        'status': 'Lent',
                        'name': lending_info['name'],
                        'email': lending_info['email'],
                        'timestamp': lending_info['timestamp']
                    })
                else:
                    search_results_index.append({
                        'book_title': book['title'],
                        'status': 'Available'
                    })
        else:
            for book in books:
                if search_query.lower() in book['title'].lower():
                    search_results.append(book)

            for title, code in book_index.items():
                if search_query.lower() in title.lower():
                    search_results_index.append({"code": code, "book_title": title})

    return render_template('bookwebsite.html', files=text_files, file_content=file_content,
                        search_query=search_query, search_results=search_results,
                        search_results_index=search_results_index)

if __name__ == '__main__':
    app.run()
