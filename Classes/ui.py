from tkinter import *
from tkinter import messagebox
from Classes.generate_password import *
import pyperclip
from os.path import exists
import csv
import json
import pandas as pd


# CONSTANTS
EMAIL_LIST_FILE = 'data/email_list.csv'
LOGO_PHOTO = "images/lock.png"


class UserInterface:
    def __init__(self, password_generator: GeneratePassword):

        self.pass_gen = password_generator
        self.password = ""

        # Window Instance of Tk
        self.window = Tk()
        self.window.title("Password Generator")
        self.window.config(padx=50, pady=50, bg="white")
        self.window.eval('tk::PlaceWindow . center')

        # Website Label
        self.website_label = Label(text="Website:", bg="White")
        self.website_label.grid(column=0, row=2)

        # Website Textbox Input
        self.website_input = Entry(bg="white", highlightbackground="white")
        self.website_input.grid(column=1, row=2)

        # When window opens, cursor starts out in website textbox
        self.website_input.focus()

        # Email Label
        self.email_username_label = Label(text="Email/Username:", bg="white")
        self.email_username_label.grid(column=0, row=3)

        # Email Textbox Input
        self.email_input = Entry(width=38, highlightbackground="white")
        self.email_input.grid(column=1, row=3, columnspan=2)

        # Password Label
        self.password_label = Label(text="Password:", bg="white")
        self.password_label.grid(column=0, row=5)

        # Password Textbox Input
        self.password_input = Entry(width=21, highlightbackground="white")
        self.password_input.grid(column=1, row=5)

        # Generate Password Button
        self.gen_pswd_btn = Button(text="Generate Password", command=self.password_in_box, highlightbackground="white")
        self.gen_pswd_btn.grid(column=2, row=5)

        # Email Dropdown Box
        self.clicked = StringVar()

        # Search Button
        self.search_btn = Button(text="Search", highlightbackground="white", width=13, command=self.search_data)
        self.search_btn.grid(column=2, row=2)

        # Add Button
        self.add_btn = Button(text="Add", width=36, highlightbackground="white")
        self.add_btn = Button(text="Add", width=36, command=self.add_button_clicked, highlightbackground="white")
        self.add_btn.grid(column=1, row=6, columnspan=2)

        # Lock Logo Photo
        self.canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
        self.lock_img = PhotoImage(file=LOGO_PHOTO)
        # enter x & y coordinates for placement of lock_img
        self.canvas.create_image(100, 100, image=self.lock_img)
        self.canvas.grid(column=0, row=0, rowspan=2, columnspan=3, pady=(0, 50))

        self.password_in_box()

        # If email_list.csv file exists:
        if exists(EMAIL_LIST_FILE):
            # Read csv file
            df = pd.read_csv(EMAIL_LIST_FILE)
            # Iterate through email column in csv file & add each item in column to list, removing any duplicates
            self.email_list_data = [*set(df.email.tolist())]

            self.showing_item = StringVar()
            self.dropdown_list = self.email_list_data

            self.email_dropdown_box = OptionMenu(self.window, self.showing_item, *self.dropdown_list,
                                                 command=self.update_email_input_box_after_dropdown_click)
            self.email_dropdown_box.config(width=34, bg="white")
            self.email_dropdown_box.grid(column=1, row=4, columnspan=3)
            self.email_input.insert(0, self.email_list_data[0])
            self.showing_item.set(self.email_list_data[0])

        # If email_list.csv file does NOT exist
        else:
            headers = ["website", "email", "password"]
            # Create email list file
            with open(EMAIL_LIST_FILE, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(headers)
            self.showing_item = StringVar()
            self.dropdown_list = [" "]

            self.email_dropdown_box = OptionMenu(self.window, self.showing_item, *self.dropdown_list,
                                                 command=self.update_email_input_box_after_dropdown_click)
            self.email_dropdown_box.config(width=25, bg="white")
            self.email_dropdown_box.grid(column=1, row=3, columnspan=2)

        self.window.mainloop()

    def password_in_box(self):
        # Check if password text already in box, if generate password is being clicked again, this means the 
        # user wants a different password generated. this will ensure to not save previous 
        # generated passwords in final password save
        if len(self.password_input.get()) != 0:
            self.password_input.delete(0, END)

        # Generate Password
        self.password = self.pass_gen.gen_password()

        # Puts generated password into entry box
        self.password_input.insert(0, self.password)

        # Copy password to clipboard
        pyperclip.copy(self.password)

    def field_reset(self):
        self.website_input.delete(0, END)
        self.password_input.delete(0, END)

    def add_button_clicked(self):
        # Get & assign variables to website name, username/email, and generated password
        website_name = self.website_input.get().lower()
        email_un_name = self.email_input.get()
        password_text = self.password_input.get()

        # Assign data to list
        new_data = [website_name, email_un_name, password_text]

        if len(website_name) == 0 or len(password_text) == 0:
            messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty!")
            pass

        else:
            # Hitting "ok" or "cancel" returns a boolean
            is_ok = messagebox.askokcancel(title=website_name,
                                   message=f'This is the information entered: \nEmail/Username: {email_un_name} \nPassword: {password_text} \n \nIs it ok to save?')

            # "Ok" returns true, if the user hits ok, write data to file
            if is_ok:
                # Write new_data list to csv file
                with open(EMAIL_LIST_FILE, 'a') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(new_data)

                # Get updated list of emails/usernames to display in dropdown box
                df = pd.read_csv(EMAIL_LIST_FILE)
                # Iterate through email column in csv file & add each item in column to list, removing any duplicates
                self.email_list_data = [*set(df.email.tolist())]

                # Set email dropdown to email input
                self.showing_item.set(email_un_name)
                menu = self.email_dropdown_box['menu']
                menu.delete(0, "end")
                for string in self.email_list_data:
                    menu.add_command(label=string,
                                     command=lambda value=string: self.om_variable.set(value))

                # # Auto-populate & Insert email address list, index, 0 at character 0
                # # self.email_input.insert(0, self.email_list_data[0])
                # # self.clicked.set(self.email_list_data[0])
                self.clicked.set(email_un_name)

                # Delete website input text
                self.website_input.delete(0, END)

            # If it's not okay, then do nothing & let user change info
            else:
                pass

    def update_email_input_box_after_dropdown_click(self, arg):
        # Pass dropdown menu choice as argument & change email input box to this string
        # https://stackoverflow.com/questions/65027966/access-optionmenu-items-tkinter
        self.email_input.delete(0, END)
        self.email_input.insert(0, arg)

    def search_data(self):
        website = self.website_input.get().lower()

        # Search csv file for website column
        # Get updated list of emails/usernames to display in dropdown box
        df = pd.read_csv(EMAIL_LIST_FILE)
        # Iterate through email column in csv file & add each item in column to list, removing any duplicates
        website_list_data = df.website.tolist()
        print(f"This is the website_list_data: {website_list_data}")

        data_holder = []
        # If website is in the email_list.csv file:
        # Get the inputted website string & validate it against the website_list_data
        if website in website_list_data:
            # Get index for all instances of website
            indexes = [i for i, j in enumerate(website_list_data) if j == website]

            # For each index found, append its row items to list
            for index in indexes:
                found_website = df.website[int(index)]
                found_email = df.email[int(index)]
                found_password = df.password[int(index)]
                data_holder.append([found_website, found_email, found_password])
            print(data_holder)

            # If there is more than one match, give a custom message with all matches found
            if len(indexes) > 1:
                concatenator = f'Information for {website.capitalize()} has been found {len(indexes)} times:\n\n'
                # Display all instances found in window
                for item in data_holder:
                    message = f'Email/Username: {item[1]}\nPassword: {item[2]}\n\n'
                    concatenator += message
                messagebox.showinfo(title=website, message=concatenator)

            # If only one match is found, give a custom message with data found
            else:
                # Just display one instance found in the window
                message = f'Information for {website.capitalize()} has been found 1 time\n\nEmail/Username: {data_holder[0][1]}\nPassword: {data_holder[0][2]}\n\n'
                messagebox.showinfo(title=website, message=message)


        # If website is not in the email_list.csv file:
        else:
            messagebox.showinfo(title="Password Not Found",
                                    message=f"Associated Email/Password for {website} not found \n\nOR \n\nyou must first add data to access it!")



        # if not exists(EMAIL_LIST_FILE_PATH):
        #     # Auto-populate & blank email address at character 0
        #     self.email_input.insert(0, "")
        # else:
        #     with open(EMAIL_LIST_FILE, newline='') as f:
        #         reader = csv.reader(f)
        #         self.email_list_data = list(reader)
        #     # Auto-populate & Insert email address list, index, 0 at character 0
        #     self.email_input.insert(0, self.email_list_data[0])
        #
        # if not exists(EMAIL_LIST_FILE_PATH):
        #     self.email_list_data = [" "]
        # else:
        #     with open(EMAIL_LIST_FILE, newline='') as f:
        #         reader = csv.reader(f)
        #         self.email_list_data = list(reader)
        #         self.clicked.set(self.email_list_data[0])

