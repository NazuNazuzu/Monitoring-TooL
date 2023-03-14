import os
import tkinter as tk

from dotenv import load_dotenv


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(
            master,
            borderwidth=5,
            relief='groove')

        e = ENV()
        print(e.name)
        print(e.email)
        print(e.pwd)
        print(e.login_url)
        print(e.home_url)
        print(e.sleep)
        print(e.version)
        print(e.line_token)



class ENV:
    def __init__(self):
        load_dotenv(f'{os.getcwd()}/resources/.env')
        self.name = os.getenv('name')
        self.email = os.getenv('email')
        self.pwd = os.getenv('password')
        self.login_url = os.getenv('login_url')
        self.home_url = os.getenv('home_url')
        self.sleep = os.getenv('sleep')
        self.version = os.getenv('version')
        self.line_token = os.getenv('line_token')


if __name__ == "__main__":
    root = tk.Tk()
    w = 400
    h = 320
    app = Application(master=root)
    app.mainloop()
