# .env reading
from dotenv import load_dotenv
import os # also for some mail stuff
# window/gui stuff:
import tkinter as tk
import tkinter.filedialog as fd
import customtkinter as ctk
import sv_ttk  # color theme (doesn't change mutch, but it's a bit better than the default)
# email stuff:
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import unicodedata

# variables stored in input fields
files = []
destination_user = ""

# Set up environment variables
load_dotenv()
mail_user = os.getenv("MAIL_USER")
mail_password = os.getenv("MAIL_APP_PASSWORD")
mail_host = os.getenv("MAIL_HOST")

default_destination_user = os.getenv("DEFAULT_DESTINATION_USER")
if default_destination_user == None:
    default_destination_user = ""

if mail_user == None or mail_password == None or mail_host == None:
    tk.messagebox.showerror("Environment variables missing", "Please set the MAIL_USER, MAIL_APP_PASSWORD, and MAIL_HOST environment variables.")
    exit()

# Set up tkinter window
app = ctk.CTk()
app.title("Kindle Sender")
app.geometry("300x400")
app.resizable(False, False)
app.iconbitmap("resources/book.ico")

# Set up server
try:
    server = smtplib.SMTP_SSL(mail_host, 465)
    if server.ehlo()[0] != 250:
        server.quit()
        tk.messagebox.showerror("Server connection failed", "Server connection failed. Please check your internet connection.")
        exit()
except Exception as e:
    tk.messagebox.showerror("Server connection failed", "Server connection failed. Reason: " + str(e))
    exit()

try:
    server.login(mail_user, mail_password)
except Exception as e:
    server.quit()
    tk.messagebox.showerror("Login failed", "Login failed. Reason: " + str(e))
    exit()

# 3x4 grid
app.rowconfigure(0, weight=0)
app.rowconfigure(1, weight=3)
app.rowconfigure(2, weight=0)
app.rowconfigure(3, weight=0)
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.columnconfigure(2, weight=1)

# Set up widgets
fileListLabel = ctk.CTkLabel(app, text="Files to send:")
fileListLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)

browseButton = ctk.CTkButton(app, text="Browse")
browseButton.grid(row=0, column=2, padx=10, pady=10)

flieList = tk.Listbox(app, selectmode="multiple")
flieList.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

sendToLabel = ctk.CTkLabel(app, text="Send to:")
sendToLabel.grid(row=2, column=0, sticky="w", padx=10, pady=10)

sendToInput = ctk.CTkEntry(app)
sendToInput.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
sendToInput.insert(0, default_destination_user)

sendButton = ctk.CTkButton(app, text="Send")
sendButton.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

# Set up event handlers

# browse button: opens file dialog for multiple files, then adds them to the file list variable and the listbox
def browse():
    global files
    files = list(fd.askopenfilenames())
    flieList.delete(0, tk.END)
    for file in files:
        flieList.insert(tk.END, file.split("/")[-1])

browseButton.configure(command=browse)

# send button: moves string from input field to variable, verifies that it's a valid email, then sends the files
def send():
    global destination_user
    global files
    
    destination_user = sendToInput.get()
    if "@" not in destination_user:
        tk.messagebox.showerror("Invalid email", "Please enter a valid email address.")
        return
    if len(files) == 0:
        tk.messagebox.showerror("No files", "Please select files to send.")
        return
    
    # convert name to ascii
    def sanitaze_name(name):
        return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = mail_user
    msg['To'] = destination_user
    msg['Subject'] = 'Kindle file transfer'
    
    # Attach and send files

    # kindle supported formats
    supported_extensions = [".pdf", ".doc", ".docx", ".htm", ".html", ".rtf", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".epub"]

    file_count = 0
    for file in files:
        if not any(file.endswith(ext) for ext in supported_extensions):
            continue
        file_count += 1

        # attach file

        book = open(file, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((book).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= ' + sanitaze_name(file.split("/")[-1]))
        msg.attach(part)

        book.close()

    if file_count == 0:
        tk.messagebox.showerror("No valid files", "No valid files to send.")
        return
    
    # Send file in mail
    try:
        server.sendmail(mail_user, destination_user, msg.as_string())
        tk.messagebox.showinfo("Success", "Files sent successfully.")

        # clear input fields and listbox
        sendToInput.delete(0, tk.END)
        flieList.delete(0, tk.END)
        files = []

    except Exception as e:
        tk.messagebox.showerror("Error", "An error occurred: " + str(e))

sendButton.configure(command=send)

# listbox: click on element twice to remove it from the list variable and the listbox
def removeFile(event):
    global files
    selected = flieList.curselection()
    for index in selected:
        files.pop(index)
    flieList.delete(0, tk.END)
    for file in files:
        flieList.insert(tk.END, file.split("/")[-1])

flieList.bind("<Double-Button-1>", removeFile)

sv_ttk.set_theme("dark")

# run the app
app.mainloop()
