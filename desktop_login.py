from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import ast
import sys
from cryptography.fernet import Fernet

def load_key():
    with open("encryption_key.key", "rb") as key_file:
        return key_file.read()

# Load key
encryption_key = load_key()
cipher = Fernet(encryption_key)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def show_login_window():
    is_logged_in = False

    main_login = Tk()
    main_login.title("Login")
    main_login.geometry("900x450+300+200")
    main_login.configure(bg='white')
    main_login.resizable(False, False)
    
    def signin():
        global username
        username = un.get()
        password = pw.get()

        try:
            with open("user_data/user_datasheet.txt", 'r') as file:
                data = file.read()
                users = ast.literal_eval(data)

            if username in users:
                encrypted_password = users[username]
                decrypted_password = decrypt_password(encrypted_password)

                if password == decrypted_password:
                    nonlocal is_logged_in
                    is_logged_in = True
                    main_login.destroy()  # Close the login window
                else:
                    messagebox.showerror("Invalid", "Invalid username or password")
            else:
                messagebox.showerror("Invalid", "Invalid username or password")
        except FileNotFoundError:
            messagebox.showerror("File Error", "User data file not found.")

    def signup_command():

        global signup_win
        signup_win = Toplevel(main_login)

        signup_win.title("Sign Up")
        signup_win.geometry("900x450+300+200")
        signup_win.configure(bg="#fff")
        signup_win.resizable(False, False)

        main_login.withdraw()

        def signup():
            username = un.get()
            password = pw.get()
            confirm_password = cpw.get()

            if password == confirm_password:
                try:
                    with open("user_data/user_datasheet.txt", 'r+') as file:
                        data = file.read()
                        users = ast.literal_eval(data)
                        
                        # Check if username already exists
                        if username in users:
                            messagebox.showerror('Invalid', 'Username already exists. Please choose another one!')
                        else:
                            encrypted_password = encrypt_password(password)
                            users[username] = encrypted_password

                            # Write the updated user data
                            file.truncate(0)
                            file.seek(0)
                            file.write(str(users))

                            messagebox.showinfo("Signup", "Sign Up Successful!")
                            signup_win.destroy()
                            main_login.deiconify()
                except FileNotFoundError:
                    # If the file doesn't exist, create a new one
                    with open("user_data/user_datasheet.txt", 'w') as file:
                        users = {username: encrypt_password(password)}
                        file.write(str(users))
                    messagebox.showinfo("Signup", "Sign Up Successful!")
                    signup_win.destroy()
                    main_login.deiconify()

            else:
                messagebox.showerror('Invalid', 'Passwords Should Match')

        def sign():
            signup_win.destroy()
            main_login.deiconify()
        
        # Handle the closing event of the signup window
        def on_closing_signup():
            signup_win.destroy()
            main_login.destroy()
            sys.exit()

        signup_win.protocol("WM_DELETE_WINDOW", on_closing_signup)

        img = Image.open("assets/login.jpg").resize((398, 332))
        img = ImageTk.PhotoImage(img)
        Label(signup_win, image=img, highlightbackground='#578361', highlightthickness=0, bd=0).place(x=50, y=55)

        Label(signup_win, text='Crop Disease Detection', fg='#003300', bg='white', font=('Microsoft YaHei UI Light', 25, 'bold')).pack(side=TOP, pady=8)

        frame = Frame(signup_win, width=350, height=390, bg='white')
        frame.place(x=480, y=50)

        Label(frame, text='Sign Up', fg = "#4b6d53", bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=115, y=20)

        # User Input Fields (for Username, Password, and Confirm Password)
        def on_enter(e):
            un.delete(0, 'end')

        def on_leave(e):
            input = un.get()
            if input == '':
                un.insert(0, 'Username')

        un = Entry(frame, width=33, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        un.place(x=30, y=70)
        un.insert(0, "Username")
        un.bind('<FocusIn>', on_enter)
        un.bind('<FocusOut>', on_leave)

        Frame(frame, width=315, height=2, bg='#578361').place(x=30, y=95)

        def on_enter(e):
            pw.delete(0, 'end')

        def on_leave(e):
            input = pw.get()
            if input == '':
                pw.insert(0, 'Password')

        pw = Entry(frame, width=33, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        pw.place(x=30, y=140)
        pw.insert(0, "Password")
        pw.bind('<FocusIn>', on_enter)
        pw.bind('<FocusOut>', on_leave)

        Frame(frame, width=315, height=2, bg='#578361').place(x=30, y=165)


        def on_enter(e):
            cpw.delete(0, 'end')

        def on_leave(e):
            input = cpw.get()
            if input == '':
                cpw.insert(0, 'Confirm Password')

        cpw = Entry(frame, width=33, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        cpw.place(x=30, y=210)
        cpw.insert(0, "Confirm Password")
        cpw.bind('<FocusIn>', on_enter)
        cpw.bind('<FocusOut>', on_leave)

        Frame(frame, width=315, height=2, bg='#578361').place(x=30, y=240)

        Button(frame, text='Sign up', bg="#59836f", fg='white', border=0, command=signup, width=30, anchor=CENTER, font=(15)).place(x=30, y=265)
        label = Label(frame, text='I already have an account', fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=50, y=315)

        signin = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg="#59836f", command=sign)
        signin.place(x=230, y=310)

        signup_win.mainloop()

    # This is all for if the user already has an account
    img = Image.open("assets/login.jpg").resize((398, 332))
    img = ImageTk.PhotoImage(img)
    Label(main_login, image=img, highlightbackground='#578361', highlightthickness=0, bd=0).place(x=50, y=55)

    frame = Frame(main_login, width=350, height=390, bg='white')
    frame.place(x=480, y=70)

    Label(main_login, text='Crop Disease Detection', fg='#003300', bg='white', font=('Microsoft YaHei UI Light', 25, 'bold')).pack(side=TOP, pady=8)

    Label(frame, text='Sign In', fg = "#4b6d53", bg='white', font=('Microsoft YaHei UI Light', 23, 'bold')).place(x=115, y=30)

    def on_enter(e):
        un.delete(0, 'end')

    def on_leave(e):
        name = un.get()
        if name == '':
            un.insert(0, 'Username')

    un = Entry(frame, width=33, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    un.place(x=30, y=90)
    un.insert(0, "Username")
    un.bind('<FocusIn>', on_enter)
    un.bind('<FocusOut>', on_leave)


    Frame(frame, width=315, height=2, bg='black').place(x=30, y=120)

    def on_enter(e):
        pw.delete(0, 'end')

    def on_leave(e):
        name = pw.get()
        if name == '':
            pw.insert(0, 'Password')

    pw = Entry(frame, width=33, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
    pw.place(x=30, y=170)
    pw.insert(0, "Password")
    pw.bind('<FocusIn>', on_enter)
    pw.bind('<FocusOut>', on_leave)

    Frame(frame, width=315, height=2, bg='black').place(x=30, y=200)

    Button(frame, text='Sign in', bg="#59836f", fg='white', border=0, command=signin, width=30, anchor=CENTER, font=(15)).place(x=30, y=235)
    label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
    label.place(x=50, y=300)

    signup = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg="#59836f", command=signup_command)
    signup.place(x=230, y=295)
    
    # If user closes window here itself, program will terminate
    def on_closing():
        main_login.destroy()
        sys.exit()

    main_login.protocol("WM_DELETE_WINDOW", on_closing)
    main_login.wait_window()

    return username, is_logged_in
