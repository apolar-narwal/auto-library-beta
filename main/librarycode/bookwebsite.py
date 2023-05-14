from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Define the list of text files to be hosted
text_files = [
    {'name': 'Catalogue', 'booklist': 'book_list_pretty.txt'},
    {'name': 'Lenders', 'lenders': 'lending.txt'},
    {'name': 'Logs', 'log': 'library_log.txt'}
]

# Route for the home page
@app.route('/')
def home():
    # Get a list of text files in the current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')]
    return render_template('index.html', files=files)

# Route to serve text files
@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run()