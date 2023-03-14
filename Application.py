import os
import time
import random
import psutil
import threading
import tkinter as tk
import tkinter.ttk as ttk

from selenium import webdriver
from dotenv import load_dotenv
from tkinter import messagebox
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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

        self.started = threading.Event()
        self.alive = True

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

        ## -- main label Frames -- ##

        self.labelFrame_btn_driver = ttk.LabelFrame(main_tab, text='アカウントへのログイン')
        self.labelFrame_btn_driver.pack(fill='x', expand=False, pady=5, padx=10, ipady=2)

        self.labelFrame_pulldown_GERIRA = ttk.LabelFrame(main_tab, text='更新秒数設定(秒)')
        self.labelFrame_pulldown_GERIRA.pack(fill='x', expand=False, pady=5, padx=10, ipady=2)

        self.labelFrame_btn_monitoring = ttk.LabelFrame(main_tab, text='監視の開始停止')
        self.labelFrame_btn_monitoring.pack(fill='x', expand=False, pady=5, padx=10, ipady=5, )


        # Driver Button
        self.btnDriverStart = ttk.Button(self.labelFrame_btn_driver, text='ログイン', command=self._start_thread_driver)

        # Start Button
        self.btnStartMonitoring = ttk.Button(self.labelFrame_btn_monitoring, text='監視開始', state='disabled',
                                             command=self._start_func)
        # Stop Button
        self.btnStopMonitoring = ttk.Button(self.labelFrame_btn_monitoring, text='監視停止', state='disabled',
                                            command=self._stop_func)

        combo_v = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        self.variable_sleep = tk.StringVar()
        self.combobox_sleep = ttk.Combobox(self.labelFrame_pulldown_GERIRA, state="disabled", values=combo_v,
                                        textvariable=self.variable_sleep)

        self.footer_text = ttk.Label(master=self.bottom_frame,
                                     text=f'現在の更新秒数：{self.sleep}sec' + '       ' + f'v{self.version}')

        self.btnDriverStart.pack()
        self.btnStartMonitoring.pack(side='left', padx=10, expand=True)
        self.btnStopMonitoring.pack(side='left', padx=10, expand=True)
        self.combobox_sleep.pack()
        self.footer_text.pack(side='right')

    def _driver_start(self):
        self.btnDriverStart['state'] = 'disabled'
        self.btnDriverStart['text'] = 'ログイン中…'
        start = time.time()

        # UA
        user_agent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        ]

        UA = user_agent[random.randrange(0, len(user_agent), 1)]

        # ドライバーのオプション設定用
        option = Options()
        option.add_argument('--lang=ja')
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument('--log-level=3')
        option.add_argument('--user-agent=' + UA)
        option.add_argument('--disable-extensions')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--use-fake-ui-for-media-stream')
        option.add_argument('--use-fake-device-for-media-stream')
        option.add_argument('--blink-settings=imagesEnabled=false')
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.page_load_strategy = 'eager'

        try:
            service = fs.Service(executable_path=ChromeDriverManager().install())
            service.creation_flags = CREATE_NO_WINDOW
        except Exception as e:

            tk.messagebox.showerror('Error', f'既存のChrome_Driverのバージョンが合っていない又はChrome_Driverがありません。\n {e}')
            self._kill_threads()

        else:

            self.driver = webdriver.Chrome(service=service,
                                           options=option)

        self.wait = WebDriverWait(driver=self.driver, timeout=120)

        # エラーがおきる可能性があるためTRY
        try:
            print(f'[LOG]{self.login_url}' + 'に接続...')
            self.driver.get(self.login_url)

        # エラーが起きた時の処理
        except Exception as e:
            print(e)
            print('[ERROR]Driverの起動に失敗しました。')
            self._kill_threads()

        else:
            stop = time.time()
            result = stop - start
            print(f'[LOG]アプリケーション起動までの時間：{result}s')

            start = time.time()
            self._login()
            stop = time.time()

            result = stop - start
            print(f'[LOG]ログインまでの時間：{result}s')

    def _start_func(self):

        # ページ表示画面の
        if self.driver.current_url != self.home_url:
            print('ホームページではないためページ遷移します。')
            self.driver.get(self.home_url)

        # 開始停止ボタンの有効無効
        self.btnStartMonitoring['state'] = 'disabled'
        self.btnStopMonitoring['state'] = 'normal'

        # waitを開始する
        self.started.set()
        print('処理を開始しました。')

    def _login(self):

        self._get_element_email()
        self._get_element_pwd()
        self._get_element_btn_login()

        # ログインに失敗したら
        if self.driver.current_url == self.login_url:
            messagebox.showerror('ログインエラー', 'ログインに失敗しました。\nメールアドレスかパスワードが間違っています。')
            self._kill_threads()

        self.driver.get('https://only-five.jp/')

        self.btnStartMonitoring['state'] = 'normal'
        self.btnDriverStart['text'] = 'ログイン済'
        self.combobox_sleep['state'] = 'readonly'
        tk.messagebox.showinfo('notice', 'ログインが完了しました。')

    def _stop_func(self):

        self.started.clear()
        print('処理が停止しました。')

        # 開始停止ボタンの有効無効
        self.btnStopMonitoring['state'] = 'disabled'
        self.btnStartMonitoring['state'] = 'normal'

    def _start_thread_driver(self):
        self.btnDriverStart['state'] = 'disabled'
        self.ThreadDriver = threading.Thread(target=self._driver_start)
        self.ThreadDriver.start()

    def _start_thread_monitoring(self):
        self.ThreadMonitoring = threading.Thread(target=self._monitoring)
        self.ThreadMonitoring.start()

    def _kill_threads(self):

        self.started.set()
        self.alive = False
        self.master.quit()

        # driver変数があったら
        if self.driver != '':
            self.driver.quit()

            # get webdriver process
            proc = self.driver.service.process

            pid = int(proc.pid)
            print("----------------------")
            print("プロセスID:" + str(pid))

            # kill process
            p = psutil.Process(pid)
            p.kill()

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
