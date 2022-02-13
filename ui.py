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
        self.window.config(pady=20, padx=20, bg=THEME)
        self.window.resizable(width=False, height=False)

        # LOGO
        self.logo_1 = Label(text="H-T", font=("Ariel", 24, "bold"), foreground=FONT_GREY, bg=THEME)
        self.logo_1.grid(column=0, row=0, columnspan=4, sticky="EW")
        self.logo_2 = Label(text="Habit Tracker", font=("Ariel", 12, "italic"), foreground=FONT_GREY, bg=THEME)
        self.logo_2.grid(column=0, row=1, columnspan=4, sticky="EW", pady=(0, 20))

        # TEXT & INPUT & BUTTON
        self.create_username_label = Label(text="Create Username: ", bg=THEME, foreground=FONT_COLOR)
        self.create_username_label.grid(column=0, row=2, sticky="E")

        self.create_username_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.create_username_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.create_username_input.grid(column=1, row=2, columnspan=4, sticky="EW")

        self.create_graph_id_label = Label(text="Id: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_id_label.grid(column=0, row=3, sticky="E")

        self.create_graph_id_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_id_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.create_graph_id_input.grid(column=1, row=3, padx=(0, 5), sticky="EW")

        self.create_graph_name_label = Label(text="Name: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_name_label.grid(column=2, row=3, sticky="E")

        self.create_graph_name_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_name_input.insert(END, "testgraph")
        self.create_graph_name_input.grid(column=3, row=3, sticky="EW")

        self.create_graph_unit_label = Label(text="Unit: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_unit_label.grid(column=0, row=4, sticky="E")

        self.create_graph_unit_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_unit_input.insert(END, "hours, kilogram, calory, commit")
        self.create_graph_unit_input.grid(column=1, row=4, padx=(0, 5), sticky="EW")

        self.create_graph_type_label = Label(text="Type: ", bg=THEME, foreground=FONT_COLOR)
        self.create_graph_type_label.grid(column=2, row=4, sticky="E")

        self.create_graph_type_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=20)
        self.create_graph_type_input.insert(END, "float, int")
        self.create_graph_type_input.grid(column=3, row=4, sticky="EW")

        self.create_username_button = Button(text="Create", border=0, highlightthickness=0, width=40, command=self.create_user)
        self.create_username_button.grid(column=1, row=5, columnspan=4, sticky="EW", pady=(5, 20))

        self.username_label = Label(text="Username: ", bg=THEME, foreground=FONT_COLOR)
        self.username_label.grid(column=0, row=6, sticky="E")

        self.username_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.username_input.insert(END, "[a-z][a-z0-9-]{1,32}")
        self.username_input.grid(column=1, row=6, columnspan=4, sticky="EW")

        self.quantity_label = Label(text="Quantity: ", bg=THEME, foreground=FONT_COLOR)
        self.quantity_label.grid(column=0, row=7, sticky="E")

        self.quantity_input = Entry(highlightthickness=0, foreground=FONT_GREY, width=40)
        self.quantity_input.insert(END, "")
        self.quantity_input.grid(column=1, row=7, columnspan=4, sticky="EW")

        self.username_button = Button(text="Add", border=0, highlightthickness=0, width=40)
        self.username_button.grid(column=1, row=8, columnspan=4, sticky="EW", pady=(5, 0))

        self.existed_username = self.username_input.get()
        self.quantity = self.quantity_input.get()

        self.new_token = ""

        self.token_generator()

        self.window.mainloop()

    def create_user(self):

        print(self.new_token)

        new_username = self.create_username_input.get()
        graph_id = self.create_graph_id_input.get()
        graph_name = self.create_graph_name_input.get()
        graph_unit = self.create_graph_unit_input.get()
        graph_type = self.create_graph_type_input.get()

        new_data = {
            new_username: {
                "X-USER-TOKEN": self.new_token,
                "graphid": graph_id
            }
        }

        pixela_user_params = {
            "token": self.new_token,
            "username": new_username,
            "agreeTermsOfService": "yes",
            "notMinor": "yes"
        }

        pixela_graph_endpoint = f"{PIXELA_USER_ENDPOINT}/{new_username}/graphs"

        pixela_graph_headers = {
            "X-USER-TOKEN": self.new_token,
        }

        pixela_graph_param = {
            "id": graph_id,
            "name": graph_name,
            "unit": graph_unit,
            "type": graph_type,
            "color": "momiji"
        }

        if len(new_username) == 0 or len(graph_id) == 0 or len(graph_name) == 0 or len(graph_unit) == 0 or len(graph_type) == 0:
            messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
        else:
            try:
                response_create_user = requests.post(PIXELA_USER_ENDPOINT, json=pixela_user_params)
                user_status = response_create_user.json()
                print(user_status)

                response_create_graph = requests.post(pixela_graph_endpoint, headers=pixela_graph_headers, json=pixela_graph_param)
                graph_status = response_create_graph.json()
                print(graph_status)
            except:
                messagebox.showerror(title="Invalid username", message="The input rule of username is `[a-z][a-z0-9-]{1,32}`.")
            else:
                # if user_status["message"] == "This user already exist.":
                #     messagebox.showinfo(title="Oops", message="This user already exist.")
                if user_status["message"] == "Invalid username. The input rule of username is `[a-z][a-z0-9-]{1,32}`.":
                    messagebox.showerror(title="Invalid username",
                                         message="The input rule of username is `[a-z][a-z0-9-]{1,32}`.")
                # if graph_status["message"] == "This graphID already exist.":
                #     messagebox.showinfo(title="Oops", message="This graphID already exist.")
                elif graph_status["message"] == "Invalid graphID. The input rule of graphID is `[a-z][a-z0-9-]{1,16}`.":
                    messagebox.showerror(title="Invalid graphID",
                                         message="The input rule of graphID is `[a-z][a-z0-9-]{1,16}`.")
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
                        messagebox.showinfo(title="Success", message="Added New Users.")
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