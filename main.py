from tkinter import *
from tkinter import messagebox
import json
import random
import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z',
           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def find_password():
    website_input = str(input_website.get()).strip()
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        website = data[website_input]
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File Found.!')
    except KeyError:
        messagebox.showinfo(title=website_input, message='No Data Found.')
    else:
        user = website['email']
        password = website['password']
        messagebox.showinfo(title=website_input, message=f"Email: {user}\nPassword: {password}")
        pyperclip.copy(password)


def generate_pw():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letter + password_symbols + password_numbers

    random.shuffle(password_list)
    password = "".join(password_list)

    input_password.delete(0, END)
    input_password.insert(0, password)
    pyperclip.copy(password)


def save():
    website = str(input_website.get()).strip()
    email = str(input_email.get()).strip()
    password = str(input_password.get()).strip()

    new_data = {
        website: {
            'email': email,
            'password': password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title='Oops', message="Please don't leave any empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'There are details entered: \nEmail:{email}'
                                                              f'\nPassword: {password} \nIs it ok to save?')
        if is_ok:
            try:
                with open('data.json', 'r') as f:
                    # Reading old data
                    data = json.load(f)
                    # Updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                data = new_data
            finally:
                with open('data.json', 'w') as f:
                    # Saving updated data
                    json.dump(data, f, indent=4)
                input_website.delete(0, END)
                input_password.delete(0, END)
                input_website.focus()


# -----------------------------------------------
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Label --------------
label_website = Label(text='Website:')
label_website.grid(column=0, row=1)
label_email = Label(text='Email/Username:')
label_email.grid(column=0, row=2)
label_password = Label(text='Password:')
label_password.grid(column=0, row=3)

# input --------------
input_website = Entry(width=18)
input_website.grid(column=1, row=1, sticky=W+E+N+S, padx=10, pady=1)
input_website.focus()
input_email = Entry(width=35)
input_email.grid(column=1, row=2, columnspan=2, sticky=W+E+N+S, padx=10, pady=3)
input_email.insert(0, '1234567@gmail.com')
input_password = Entry(width=18)
input_password.grid(column=1, row=3, sticky=W+E+N+S, padx=10, pady=1)

# Button --------------
button_Search = Button(text='Search', width=16, command=find_password)
button_Search.grid(column=2, row=1)
button_generate = Button(text='Generate Password', width=16, command=generate_pw)
button_generate.grid(column=2, row=3)
button_add = Button(text='Add', width=38, command=save)
button_add.grid(column=1, row=4, columnspan=2, pady=2)

window.mainloop()
