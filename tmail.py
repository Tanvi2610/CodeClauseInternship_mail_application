from tkinter import *
from tkinter import filedialog
import smtplib
from email.message import EmailMessage

attachments = []

root = Tk()
root.title('Email App')

def attachFile():
    filename = filedialog.askopenfilename(initialdir='C:/', title='Select a file')
    attachments.append(filename)
    notif.config(fg='green', text='Attached ' + str(len(attachments)) + ' files')

def send():
    try:
        msg = EmailMessage()
        userName = temp_username.get()
        password = temp_password.get()
        to = temp_receiver.get()
        subject = temp_subject.get()
        body = temp_body.get()
        msg['subject'] = subject
        msg['from'] = userName
        msg['to'] = to
        msg.set_content(body)

        if attachments:
            filename = attachments[0]
            filetype = filename.split('.')
            filetype = filetype[1]
            if filetype.lower() in ["jpg", "png"]:
                import imghdr
                with open(filename, 'rb') as f:
                    file_data = f.read()
                    image_type = imghdr.what(filename)
                msg.add_attachment(file_data, maintype='image', subtype=image_type, filename=f.name)
            else:
                with open(filename, 'rb') as f:
                    file_data = f.read()
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=f.name)
        
        if not all([userName, password, to, subject, body]):
            notif.config(text='All fields are required', fg="red")
            return
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(userName, password)
        server.send_message(msg)
        server.quit()
        notif.config(text='Email has been sent', fg='green')
    except Exception as e:
        print(f"Error: {e}")
        notif.config(text='Error sending email', fg='red')

def reset():
    userNameEntry.delete(0, 'end')
    passwordEntry.delete(0, 'end')
    receiverEntry.delete(0, 'end')
    subjectEntry.delete(0, 'end')
    bodyEntry.delete(0, 'end')

Label(root, text="Email App", font=('Calibri', 30, "bold"),foreground="#4a4a4a").grid(row=0, sticky=N)
Label(root, text="Use the form below to send an email", font=('Calibri', 20)).grid(row=1, sticky=W, padx=5)

Label(root, text="Email", font=('Calibri', 24)).grid(row=2, sticky=W, padx=5)
Label(root, text="Password", font=('Calibri', 24)).grid(row=3, sticky=W, padx=5,)  # Added padding
Label(root, text="To", font=('Calibri', 24)).grid(row=4, sticky=W, padx=5)
Label(root, text="Subject", font=('Calibri', 24)).grid(row=5, sticky=W, padx=5)
Label(root, text="Body", font=('Calibri', 24)).grid(row=6, sticky=W, padx=5)

notif = Label(root, text="", font=('Calibri', 18))
notif.grid(row=7, sticky=S, padx=5)

temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject = StringVar()
temp_body = StringVar()

userNameEntry = Entry(root, textvariable=temp_username, width=40)
userNameEntry.grid(row=2, column=0, padx=60,ipady=6)
passwordEntry = Entry(root, show="*", textvariable=temp_password, width=40)
passwordEntry.grid(row=3, column=0, padx=10, ipady=6)
receiverEntry = Entry(root, textvariable=temp_receiver, width=40)
receiverEntry.grid(row=4, column=0, padx=10, ipady=6)
subjectEntry = Entry(root, textvariable=temp_subject, width=40)
subjectEntry.grid(row=5, column=0, padx=10, ipady=6)
bodyEntry = Entry(root, textvariable=temp_body, width=40)
bodyEntry.grid(row=6, column=0, padx=10, ipady=6)

Button(root, text="Send", font=('Calibri', 24), command=send, cursor="hand2", activebackground="grey").grid(row=7, sticky=W, pady=15, padx=5)
Button(root, text="Reset", font=('Calibri', 24), command=reset, cursor="hand2", activebackground="grey").grid(row=7, sticky=W, pady=45, padx=90)
Button(root, text="Attachment", font=('Calibri', 24), command=attachFile, cursor="hand2", activebackground="grey").grid(row=7, sticky=W, pady=75, padx=185)

root.mainloop()
