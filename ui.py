from tkinter import *
from tkinter import messagebox
import requests
import datetime
from random import *
import json

THEME = "white"
FONT_GREY = "grey35"
FONT_COLOR = "black"

PIXELA_USER_ENDPOINT = "https://pixe.la/v1/users"


class HTInterface:

    def __init__(self):

        # WINDOW
        self.window = Tk()
        self.window.title("H-T")
        self.window.iconbitmap("habit_tracker.ico")
        self.window.config(pady=20, padx=20, bg=THEME)
        self.window.resizable(width=False, height=False)

        # LOGO
        self.logo_1 = Label(text="H-T", font=("Ariel", 24, "bold"), foreground=FONT_GREY, bg=THEME)
        self.logo_1.grid(column=0, row=0, columnspan=4, sticky="EW")
        self.logo_2 = Label(text="Habit Tracker", font=("Ariel", 12, "italic"), foreground=FONT_GREY, bg=THEME)
        self.logo_2.grid(column=0, row=1, columnspan=4, sticky="EW", pady=(0, 20))

        # TEXT & INPUT & BUTTON
        self.create_username_label = Label(text="Username: ", bg=THEME, foreground=FONT_COLOR)
        self.create_username_label.grid(column=0, row=2, sticky="E")

        self.create_username_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.create_username_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.create_username_input.grid(column=1, row=2, columnspan=4, sticky="EW")

        self.create_username_button = Button(text="Create User", border=0, highlightthickness=0, width=40,
                                             command=self.create_user)
        self.create_username_button.grid(column=1, row=3, columnspan=4, sticky="EW", pady=(5, 5))

        self.create_graph_id_label = Label(text="Id: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_id_label.grid(column=0, row=4, sticky="E")

        self.create_graph_id_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_id_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.create_graph_id_input.grid(column=1, row=4, padx=(0, 5), sticky="EW")

        self.create_graph_name_label = Label(text="Name: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_name_label.grid(column=2, row=4, sticky="E")

        self.create_graph_name_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_name_input.insert(END, "testgraph")
        self.create_graph_name_input.grid(column=3, row=4, sticky="EW")

        self.create_graph_unit_label = Label(text="Unit: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_unit_label.grid(column=0, row=5, sticky="E")

        self.create_graph_unit_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_unit_input.insert(END, "hours, kilogram, calory, commit")
        self.create_graph_unit_input.grid(column=1, row=5, padx=(0, 5), sticky="EW")

        self.create_graph_type_label = Label(text="Type: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_type_label.grid(column=2, row=5, sticky="E")

        self.create_graph_type_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_type_input.insert(END, "float, int")
        self.create_graph_type_input.grid(column=3, row=5, sticky="EW")

        self.create_graph_button = Button(text="Create Graph", border=0, highlightthickness=0, width=40, command=self.create_graph)
        self.create_graph_button.grid(column=1, row=6, columnspan=4, sticky="EW", pady=(5, 20))

        self.username_label = Label(text="Username: ", bg=THEME, foreground=FONT_COLOR)
        self.username_label.grid(column=0, row=7, sticky="E")

        self.username_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.username_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.username_input.grid(column=1, row=7, columnspan=4, sticky="EW")

        self.quantity_label = Label(text="Quantity: ", bg=THEME, foreground=FONT_COLOR)
        self.quantity_label.grid(column=0, row=8, sticky="E")

        self.quantity_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.quantity_input.insert(END, "")
        self.quantity_input.grid(column=1, row=8, columnspan=4, sticky="EW")

        self.username_button = Button(text="Add Pixel", border=0, highlightthickness=0, width=40, command=self.add_pixel)
        self.username_button.grid(column=1, row=9, columnspan=4, sticky="EW", pady=(5, 0))

        self.existed_username = ""
        self.quantity = ""

        self.new_token = ""
        self.new_username = ""
        self.graph_id = ""
        self.graph_name = ""
        self.graph_unit = ""
        self.graph_type = ""

        self.user_already_exist = ""

        self.token_generator()

        self.window.mainloop()

    def create_user(self):
        self.new_username = self.create_username_input.get()

        pixela_user_params = {
            "token": self.new_token,
            "username": self.new_username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }

        if len(self.new_username) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        else:
            response_create_user = requests.post(PIXELA_USER_ENDPOINT, json=pixela_user_params)
            user_status = response_create_user.json()
            if user_status["message"] == "This user already exist.":
                messagebox.showinfo(title="Oops", message="This user already exist.")

                self.user_already_exist = user_status["message"]
            elif user_status["message"] == "Invalid username. The input rule of username is `[a-z][a-z0-9-]{1,32}`.":
                messagebox.showerror(title="Invalid username",
                                     message="The input rule of username is `[a-z][a-z0-9-]{1,32}`.")

                self.new_username = ""
            else:
                print(f"New User:{self.new_username}")
                messagebox.showinfo(title="Success", message="User Added.")

    def create_graph(self):
        self.graph_id = self.create_graph_id_input.get()
        self.graph_name = self.create_graph_name_input.get()
        self.graph_unit = self.create_graph_unit_input.get()
        self.graph_type = self.create_graph_type_input.get()

        pixela_graph_endpoint = f"{PIXELA_USER_ENDPOINT}/{self.new_username}/graphs"

        pixela_graph_headers = {
            "X-USER-TOKEN": self.new_token,
        }

        pixela_graph_param = {
            "id": self.graph_id,
            "name": self.graph_name,
            "unit": self.graph_unit,
            "type": self.graph_type,
            "color": "momiji"
        }

        new_data = {
            self.new_username: {
                "X-USER-TOKEN": self.new_token,
                "graphid": self.graph_id,
                "unit": self.graph_unit,
                "type": self.graph_type
            }
        }

        if self.user_already_exist == "This user already exist.":
            messagebox.showinfo(title="Oops", message="This user already exist.")
        elif len(self.new_username) == 0:
            messagebox.showerror(title="Oops", message="Make sure that you create a user!")
        elif len(self.graph_id) == 0 or len(self.graph_name) == 0 or len(self.graph_unit) == 0 or len(self.graph_type) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        else:
            response_create_graph = requests.post(pixela_graph_endpoint, headers=pixela_graph_headers,
                                                  json=pixela_graph_param)
            graph_status = response_create_graph.json()

            # if graph_status["message"] == "This graphID already exist.":
            #     messagebox.showinfo(title="Oops", message="This graphID already exist.")
            if graph_status["message"] == "Invalid graphID. The input rule of graphID is `[a-z][a-z0-9-]{1,16}`.":
                messagebox.showerror(title="Invalid graphID",
                                     message="The input rule of graphID is `[a-z][a-z0-9-]{1,16}`.")

                self.graph_id = ""

            elif graph_status["message"] == "The type you specify must be one of the following: int / float":
                messagebox.showerror(title="Invalid Type",
                                 message="The type you specify must be one of the following: int / float")
            else:
                try:
                    # Append new data in json file
                    with open("data/database.json", "r") as data:
                        # Reading the old data
                        data_file = json.load(data)
                except FileNotFoundError:
                    with open("data/database.json", "w") as data:
                        # Saving updated data
                        json.dump(new_data, data, indent=4)
                else:
                    # Updating old data to new data
                    data_file.update(new_data)
                    with open("data/database.json", "w") as data:
                        # Saving updated data
                        json.dump(data_file, data, indent=4)
                finally:
                    messagebox.showinfo(
                        title="Success",
                        message=f"Your Graph: \nhttps://pixe.la/v1/users/{self.new_username}/graphs/{self.graph_id}.html.")

                    self.new_username = ""
                    self.token_generator()

    def token_generator(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # List Comprehension
        token_letters = [choice(letters) for item in range(randint(8, 16))]
        token_numbers = [choice(numbers) for item in range(randint(8, 16))]

        # Combined all list into single list
        token_list = token_letters + token_numbers

        shuffle(token_list)

        self.new_token = "".join(token_list)

    def add_pixel(self):
        self.existed_username = self.username_input.get()
        self.quantity = self.quantity_input.get()

        if len(self.existed_username) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        else:
            try:
                with open("data/database.json", "r") as data:
                    # Reading the old data
                    data_file = json.load(data)
            except FileNotFoundError:
                messagebox.showerror(title="File Not Found", message="Please make sure that you created new user.")
            else:
                try:
                    data_file[self.existed_username]
                except KeyError:
                    messagebox.showerror(title="No Data Found", message="Please make sure this user already created.")
                else:
                    if len(self.quantity) == 0:
                        messagebox.showerror(title="Oops",
                                             message="Please don't leave any fields empty!")
                    else:
                        try:
                            if data_file[self.existed_username]["type"] == "float":
                                val = float(self.quantity)
                            else:
                                val = int(self.quantity)
                        except ValueError:
                            messagebox.showerror(title="Value Error",
                                                 message=f"Make sure you type is {data_file[self.existed_username]['type']}.")
                        else:
                            exist_pixela_graph_token = {
                                "X-USER-TOKEN": data_file[self.existed_username]["X-USER-TOKEN"]
                            }

                            exist_pixela_graph_endpoint = f"{PIXELA_USER_ENDPOINT}/{self.existed_username}/graphs/{data_file[self.existed_username]['graphid']}"

                            today = datetime.datetime.now().strftime("%Y%m%d")

                            exist_pixela_graph_config = {
                                "date": today,
                                "quantity": self.quantity
                            }

                            response_pixel_post = requests.post(exist_pixela_graph_endpoint,
                                                                headers=exist_pixela_graph_token,
                                                                json=exist_pixela_graph_config)
                            messagebox.showinfo(
                                title="Success",
                                message=f"{self.quantity} {data_file[self.existed_username]['unit']} Added.")
