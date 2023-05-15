from flask import Flask, render_template

app = Flask(__name__)

# Define the paths to the text files
book_list_file = 'book_list_pretty.txt'
book_log_file = 'library_log.txt'
lenders_file = 'lending.txt'

@app.route('/')
def home():
    # Read the contents of the text files
    with open(book_list_file, 'r') as f:
        book_list_content = f.read()

    with open(book_log_file, 'r') as f:
        book_log_content = f.read()

    with open(lenders_file, 'r') as f:
        lenders_content = f.read()

    return render_template('adminwebsite.html', book_list_content=book_list_content,
                        book_log_content=book_log_content, lenders_content=lenders_content)

if __name__ == '__main__':
    app.run(port=8000)
