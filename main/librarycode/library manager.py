from sched import scheduler
import tkinter as tk
from tkinter import messagebox
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import ttk
from ttkthemes import ThemedStyle

def lend_book():
    # get inputs from GUI
    name = name_entry.get()
    email = email_entry.get()
    code = code_entry.get()
    code_new = code_entry.get()

    # check if inputs are valid
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return
    if not email:
        messagebox.showerror("Error", "Please enter an email")
        return
    if "@" not in email:
        messagebox.showerror("Error", "Please enter a valid email address")
        return
    if not code:
        messagebox.showerror("Error", "Please enter a Code")
        return

    # check if lending already exists
    with open('lending.txt', 'r') as f:
        for line in f:
            fields = line.strip().split(',',1)
            if len(fields) > 1 and fields[3] == code:
                messagebox.showerror("Error", "This book has already been lent")
                return

    # load the book index file
    book_index = {}
    with open('book_index.txt', 'r') as f:
        for line in f:
            icode, title = line.strip().split(',',1)
            book_index[icode] = title

    # get the book title from the index file
    if code not in book_index:
        messagebox.showerror("Error", "Invalid Code")
        return
    book_title = book_index[code]

    # update book availability file
    book_availability = {}
    with open('book_availability.txt', 'r') as f:
        for line in f:
            icode, available = line.strip().split(',')
            book_availability[icode] = available
    book_availability[code] = 'no'
    with open('book_availability.txt', 'w') as f:
        for code, available in book_availability.items():
            f.write(f"{code},{available}\n")

    # store inputs, book title, and timestamp in a text file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('lending.txt', 'a') as f:
        f.write(f"{name},{email},{code_new},{book_title},{timestamp}\n")
    messagebox.showinfo("Success", "Book lent successfully for two weeks")

    # log the lending action to a file
    with open('library_log.txt', 'a') as f:
        f.write(f"LENT: Name: {name} | Email: {email} | Title: {book_title} | Time: {timestamp}\n")

def return_book():
    # get inputs from GUI
    name = name_entry.get()
    email = email_entry.get()
    code = code_entry.get()
    code_new = code_entry.get()

    # check if inputs are valid
    if not name:
        messagebox.showerror("Error", "Please enter a name")
        return
    if not email:
        messagebox.showerror("Error", "Please enter an email")
        return
    if not code:
        messagebox.showerror("Error", "Please enter a code")
        return

    # remove book from text file
    with open('lending.txt', 'r') as f:
        lines = f.readlines()
    with open('lending.txt', 'w') as f:
        lending_removed = False
        for line in lines:
            if f"{name},{email},{code}" in line:
                lending_removed = True
            else:
                f.write(line)
        if not lending_removed:
            messagebox.showerror("Error", "This book has not been lent")
            return
    messagebox.showinfo("Success", "Book returned successfully")

    # update book availability file
    book_availability = {}
    with open('book_availability.txt', 'r') as f:
        for line in f.readlines():
            icode, available = line.strip().split(',')
            book_availability[icode] = available
    book_availability[code] = 'yes'
    with open('book_availability.txt', 'w') as f:
        for code, available in book_availability.items():
            f.write(f"{code},{available}\n")

    # load the book index file
    book_index = {}
    with open('book_index.txt', 'r') as f:
        for line in f:
            icode, title = line.strip().split(',',1)
            book_index[icode] = title
    book_title = book_index[code_new]

    print(book_title)

    # log the Returning action to a file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('library_log.txt', 'a') as f:
        f.write(f"RETURNED: Name: {name} | Email: {email} | Title: {book_title} | Time: {timestamp}\n")

    # send notification email to administrator
    subject = f"Book {code} has been returned by {name}"
    body = f"Dear Administrator,\n\nThe book {book_title} has been returned by {name}.\n\nBest regards,\nThe CWS Library"
    send_email(to="admin_email@gmail.com", subject=subject, body=body)

    # schedule overdue reminder
    due_date = datetime.datetime.now() + datetime.timedelta(days=14)
    scheduler.add_job(send_overdue_email, "date", run_date=due_date, args=[name, email, code])


# Create GUI
root = tk.Tk()
root.title("Library Lending System")
root.attributes("-fullscreen", True)  # Set the window to full-screen

# Set the theme to 'breeze'
style = ThemedStyle(root)
style.set_theme("breeze")

# Create main frame
main_frame = ttk.Frame(root, padding=50)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create entry fields
name_label = ttk.Label(main_frame, text="Name")
name_label.pack()
name_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=30)
name_entry.pack(pady=10)

email_label = ttk.Label(main_frame, text="Email")
email_label.pack()
email_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=30)
email_entry.pack(pady=10)

code_label = ttk.Label(main_frame, text="Code")
code_label.pack()
code_entry = ttk.Entry(main_frame, font=("Helvetica", 16), width=30)
code_entry.pack(pady=10)

# Create lend button
lend_button = ttk.Button(main_frame, text="Lend Book", command=lend_book)
lend_button.pack(pady=20)

# Create return button
return_button = ttk.Button(main_frame, text="Return Book", command=return_book)
return_button.pack(pady=10)

# Run GUI
root.mainloop()

def send_email(to, subject, body, attachment=None):
    # configure SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "chicagowaldorflibrary@gmail.com"
    smtp_password = "Student@CWS"
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.ehlo()
    smtp_connection.starttls()
    smtp_connection.login(smtp_username, smtp_password)

    # create email message
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment)
        part["Content-Disposition"] = f"attachment; filename={attachment}"
        message.attach(part)

    # send email message
    smtp_connection.send_message(message)
    smtp_connection.quit()

def send_overdue_email(name, email, code):
    # check if book is still lent
    with open('lending.txt', 'r') as f:
        lendings = f.read().splitlines()
    lending = f"{name},{email},{code}"
    if lending not in lendings:
        return

    # load the book index file
    book_index = {}
    with open('book_index.txt', 'r') as f:
        for line in f:
            code, title = line.strip().split(',')
            book_title = book_index[code]

    # send overdue reminder email
    subject = f"Reminder: Book {book_title} is overdue"
    body = f"Dear {name},\n\nPlease return the book {book_title} as soon as possible. You are past the checkout limit of two weeks.\n\nBest regards,\nThe CWS Library"
    send_email(to=email, subject=subject, body=body)
    send_email(to="admin_email@gmail.com", subject=subject, body=body)

    # schedule next overdue reminder
    scheduler.add_job(send_overdue_email, "interval", days=1, args=[name, email, code])
