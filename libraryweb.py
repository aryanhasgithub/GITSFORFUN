from flask import Flask, render_template, request, jsonify

# Import the Library class from your existing code
class Library:
    def __init__(self, book_list):
        self.booklist = book_list
        self.lended = {}

    def displaybooks(self):
        return self.booklist

    def lend(self, username, book):
        if book not in self.booklist:
            return "Book is not present in the library."
        elif book in self.lended:
            return "Book is already lended."
        else:
            self.lended[book] = username
            return f"Book '{book}' has been lended to {username}."

    def addbook(self, book):
        self.booklist.append(book)
        return f"Book '{book}' has been added to the library."

    def returnbook(self, book):
        if book in self.lended:
            del self.lended[book]
            return f"Book '{book}' has been returned."
        else:
            return "Book was not borrowed from us."


# Initialize Flask app and Library instance
app = Flask(__name__)
books = Library(['IKIGAI', 'Harry Potter', 'Room on the Roof', 'Blue Umbrella'])

# Route to serve the main HTML page
@app.route('/')
def home():
    return render_template('index.html')

# API to display books
@app.route('/displaybooks', methods=['GET'])
def display_books():
    return jsonify(books.displaybooks())

# API to lend a book
@app.route('/lendbook', methods=['POST'])
def lend_book():
    data = request.json
    username = data['username']
    book = data['book']
    result = books.lend(username, book)
    return jsonify({'message': result})

# API to add a book
@app.route('/addbook', methods=['POST'])
def add_book():
    data = request.json
    book = data['book']
    result = books.addbook(book)
    return jsonify({'message': result})

# API to return a book
@app.route('/returnbook', methods=['POST'])
def return_book():
    data = request.json
    book = data['book']
    result = books.returnbook(book)
    return jsonify({'message': result})

if __name__ == '__main__':
    app.run(debug=True)
