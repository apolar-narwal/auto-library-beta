from sched import scheduler
import tkinter as tk
from tkinter import messagebox
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tkinter import ttk

def lend_book():
    # get inputs from GUI
    name = name_entry.get()
    email = email_entry.get()
    code = code_entry.get()

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
            fields = line.strip().split(',')
            if len(fields) > 1 and fields[3] == code:
                messagebox.showerror("Error", "This lending already exists")
                return

    # load the book index file
    book_index = {}
    with open('book_index.txt', 'r') as f:
        for line in f:
            code, title = line.strip().split(',')
            book_index[code] = title

    # get the book title from the index file
    if code not in book_index:
        messagebox.showerror("Error", "Invalid Code")
        return
    book_title = book_index[code]

    # check if the person has already borrowed three books
    lending_count = 0
    with open('lending.txt', 'r') as f:
        for line in f:
            fields = line.strip().split(',')
            if len(fields) > 1 and fields[1] == email:
                lending_count += 1
    if lending_count >= 3:
        messagebox.showerror("Error", "You have already borrowed three books. Please return one to continue.")
        return

    # update book availability file
    book_availability = {}
    with open('book_availability.txt', 'r') as f:
        for line in f:
            code_, available = line.strip().split(',')
            book_availability[code_] = available
    book_availability[code] = 'no'
    with open('book_availability.txt', 'w') as f:
        for code_, available in book_availability.items():
            f.write(f"{code_},{available}\n")

    # store inputs, book title, and timestamp in a text file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('lending.txt', 'a') as f:
        f.write(f"{name},{email},{code},{book_title},{timestamp}\n")
    messagebox.showinfo("Success", "Book lent successfully")

    # log the lending action to a file
    with open('library_log.txt', 'a') as f:
        f.write(f"LENT: Name: {name} | Email: {email} | Title: {book_title} | Time: {timestamp}\n")

def return_book():
    # get inputs from GUI
    name = name_entry.get()
    email = email_entry.get()
    code = code_entry.get()

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
            messagebox.showerror("Error", "This lending does not exist")
            return
    messagebox.showinfo("Success", "Book returned successfully")

    # update book availability file
    book_availability = {}
    with open('book_availability.txt', 'r') as f:
        for line in f.readlines():
            code, available = line.strip().split(',')
            book_availability[code] = available
    book_availability[code] = 'yes'
    with open('book_availability.txt', 'w') as f:
        for code, available in book_availability.items():
            f.write(f"{code},{available}\n")

    # load the book index file
    book_index = {}
    with open('book_index.txt', 'r') as f:
        for line in f:
            code, title = line.strip().split(',')
            book_title = book_index[code]

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

# create GUI
root = tk.Tk()
root.title("Library Lending System")
root.geometry('1920x1080')
root.configure(bg='black')

# create main frame
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# create entry fields
name_label = ttk.Label(main_frame, text="Name", foreground='white', background='black', font=("Helvetica", 14))
name_label.pack()
name_entry = ttk.Entry(main_frame, font=("Helvetica", 14))
name_entry.pack()

email_label = ttk.Label(main_frame, text="Email", foreground='white', background='black', font=("Helvetica", 14))
email_label.pack()
email_entry = ttk.Entry(main_frame, font=("Helvetica", 14))
email_entry.pack()

code_label = ttk.Label(main_frame, text="code", foreground='white', background='black', font=("Helvetica", 14))
code_label.pack()
code_entry = ttk.Entry(main_frame, font=("Helvetica", 14))
code_entry.pack()

# create lend button
lend_button = ttk.Button(main_frame, text="Lend Book", command=lend_book, style='DarkButton.TButton')
lend_button.pack()

# create return button
return_button = ttk.Button(main_frame, text="Return Book", command=return_book, style='DarkButton.TButton')
return_button.pack()

# create custom style for button
s = ttk.Style()
s.configure('DarkButton.TButton', foreground='white', background='black', font=("Helvetica", 14))

# run GUI
root.mainloop()

def send_email(to, subject, body, attachment=None):
    # configure SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "your_email@gmail.com"
    smtp_password = "your_email_password"
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
    body = f"Dear {name},\n\nPlease return the book {book_title} as soon as possible.\n\nBest regards,\nThe CWS Library"
    send_email(to=email, subject=subject, body=body)
    send_email(to="admin_email@gmail.com", subject=subject, body=body)

    # schedule next overdue reminder
    scheduler.add_job(send_overdue_email, "interval", days=1, args=[name, email, code])