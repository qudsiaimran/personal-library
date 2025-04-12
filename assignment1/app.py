import streamlit as st
import os

# Define the file path where books will be saved
file_path = "library.txt"

# Function to load books from a file
def load_books():
    books = []
    if os.path.exists(file_path):  # Check if the file exists
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                title, author, year, genre, read_status = line.strip().split(",")
                books.append({
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read_status": read_status == "True"
                })
    return books

# Function to save books to a file
def save_books(books):
    with open(file_path, "w") as file:
        for book in books:
            file.write(f"{book['title']},{book['author']},{book['year']},{book['genre']},{book['read_status']}\n")

# Load books from the file when the program starts
books = load_books()

# Streamlit UI
st.title("Personal Library Manager")

# Menu options
option = st.sidebar.selectbox("Choose an action", ["Add Book", "Remove Book", "Search Books", "Display Books", "Statistics"])

# Add Book
if option == "Add Book":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    year = st.number_input("Publication Year", min_value=1900, max_value=2025, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read")
    
    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        }
        books.append(new_book)
        save_books(books)
        st.success("Book added successfully!")

# Remove Book
elif option == "Remove Book":
    st.header("Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove:")
    
    if st.button("Remove Book"):
        books = [book for book in books if book['title'] != title_to_remove]
        save_books(books)
        st.success("Book removed successfully!")

# Search Books
elif option == "Search Books":
    st.header("Search for Books")
    search_term = st.text_input("Search by Title or Author")
    
    matching_books = [book for book in books if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()]
    
    if matching_books:
        for book in matching_books:
            st.write(f"**Title:** {book['title']} | **Author:** {book['author']} | **Year:** {book['year']} | **Genre:** {book['genre']} | **Read:** {'Yes' if book['read_status'] else 'No'}")
    else:
        st.write("No matching books found.")

# Display Books
elif option == "Display Books":
    st.header("All Books in the Library")
    if books:
        for book in books:
            st.write(f"**Title:** {book['title']} | **Author:** {book['author']} | **Year:** {book['year']} | **Genre:** {book['genre']} | **Read:** {'Yes' if book['read_status'] else 'No'}")
    else:
        st.write("No books in the library.")

# Statistics
elif option == "Statistics":
    total_books = len(books)
    read_books = sum(1 for book in books if book['read_status'])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.header("Library Statistics")
    st.write(f"Total Books: {total_books}")
    st.write(f"Books Read: {read_books}")
    st.write(f"Percentage of Books Read: {read_percentage:.2f}%")
