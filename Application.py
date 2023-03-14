import os
import tkinter as tk
import tkinter.ttk as ttk

from dotenv import load_dotenv


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(
            master,
            borderwidth=5,
            relief='groove')
        env = ENV()
        self.name = env.name
        self.email = env.email
        self.pwd = env.pwd
        self.login_url = env.login_url
        self.home_url = env.home_url
        self.sleep = env.sleep
        self.version = env.version
        self.line_token = env.line_token

        self.create_widgets()

    def create_widgets(self):
        ## -- Note Frames -- ##
        note = ttk.Notebook(self.master, width=w, height=300)

        self.bottom_frame = ttk.Frame(master=self.master)
        self.bottom_frame.pack(side='bottom', fill='x', expand=False)

        # tab一覧
        main_tab = ttk.Frame(note)
        register_creator_tab = ttk.Frame(note)
        register_time_tab = ttk.Frame(note)

        # Frame pack
        main_tab.pack()
        register_creator_tab.pack()
        register_time_tab.pack()

        # tabに追加
        note.add(main_tab, text='       　　監視　　       ')
        note.add(register_creator_tab, text='     　　管理番号　　     ')
        note.add(register_time_tab, text='     　　メモ　　     ')
        note.pack()


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
