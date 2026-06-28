# ==========================================
# Подробно прокомментированная версия
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess
import sys

# Основной класс приложения.
# Отвечает за интерфейс и запуск генератора BAT-файлов.
class PrankCreatorApp:
    def __init__(self, root):
        # Конструктор. Создает главное окно и инициализирует интерфейс.
        self.root = root
        self.root.title("Pranker-bat")
        self.root.geometry("850x650")
        self.root.configure(bg='#1e1e1e')
        
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass 
        
        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys.executable).parent
        else:
            self.base_path = Path(__file__).parent

        self.set_dark_theme()
        
        self.canvas = tk.Canvas(self.root, bg='#1e1e1e', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.create_widgets()

    def set_dark_theme(self):
        # Настройка темной темы оформления.
        style = ttk.Style()
        style.theme_use('clam')
        bg_color = '#1e1e1e'
        secondary_bg = '#2d2d2d'
        accent_color = '#00ff88'
        entry_bg = '#363636'

        style.configure('.', background=bg_color, foreground='white')
        style.configure('TFrame', background=bg_color)
        style.configure('TLabelframe', background=secondary_bg, foreground=accent_color)
        style.configure('TLabelframe.Label', background=secondary_bg, foreground=accent_color, font=('Arial', 10, 'bold'))
        style.configure('TButton', background='#404040', foreground='white', borderwidth=1)
        style.map('TButton', background=[('active', '#505050')])
        style.configure('TEntry', fieldbackground=entry_bg, foreground='white', insertcolor='white', bordercolor=secondary_bg)
        style.configure('TSpinbox', fieldbackground=entry_bg, foreground='white', insertcolor='white', arrowcolor=accent_color, bordercolor=secondary_bg)
        style.map('TSpinbox', fieldbackground=[('readonly', entry_bg)])
        style.configure('TRadiobutton', background=bg_color, foreground='white')
        style.map('TRadiobutton', background=[('selected', bg_color)], foreground=[('selected', accent_color)])

    def create_widgets(self):
        # Создание всех элементов графического интерфейса.
        tk.Label(self.scrollable_frame, text="Pranker-bat", font=('Arial', 24, 'bold'),
                 fg='#00ff88', bg='#1e1e1e').pack(pady=20, fill=tk.X)
        
        type_frame = ttk.LabelFrame(self.scrollable_frame, text="Тип пранка", padding=15)
        type_frame.pack(fill=tk.X, padx=30, pady=10)
        
        self.prank_var = tk.StringVar(value="shutdown")
        ttk.Radiobutton(type_frame, text="Система", variable=self.prank_var, 
                       value="shutdown", command=self.update_ui).pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(type_frame, text="YouTube", variable=self.prank_var, 
                       value="youtube", command=self.update_ui).pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(type_frame, text="Закрытие программ", variable=self.prank_var, 
                       value="close_apps", command=self.update_ui).pack(side=tk.LEFT, padx=15)

        self.settings_frame = ttk.LabelFrame(self.scrollable_frame, text="Параметры", padding=15)
        self.settings_frame.pack(fill=tk.X, padx=30, pady=10)
        
        delay_f = ttk.Frame(self.settings_frame)
        delay_f.pack(fill=tk.X, pady=5)
        ttk.Label(delay_f, text="Задержка (сек):", width=15).pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value="5")
        ttk.Spinbox(delay_f, from_=0, to=999, textvariable=self.delay_var, width=10).pack(side=tk.LEFT)

        self.dynamic_f = ttk.Frame(self.settings_frame)
        self.dynamic_f.pack(fill=tk.X, pady=5)

        save_frame = ttk.LabelFrame(self.scrollable_frame, text="Сохранение", padding=15)
        save_frame.pack(fill=tk.X, padx=30, pady=10)
        
        name_f = ttk.Frame(save_frame)
        name_f.pack(fill=tk.X, pady=5)
        ttk.Label(name_f, text="Имя файла:", width=15).pack(side=tk.LEFT)
        self.filename_entry = ttk.Entry(name_f)
        self.filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        path_f = ttk.Frame(save_frame)
        path_f.pack(fill=tk.X, pady=5)
        ttk.Label(path_f, text="Папка:", width=15).pack(side=tk.LEFT)
        self.path_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        ttk.Entry(path_f, textvariable=self.path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        ttk.Button(path_f, text="Обзор", command=self.browse_path).pack(side=tk.RIGHT)
        
        self.create_btn = ttk.Button(self.scrollable_frame, text="СОЗДАТЬ ПРАНК", 
                                    command=self.create_prank, width=40)
        self.create_btn.pack(pady=30)
        
        self.status_var = tk.StringVar(value="Готов")
        ttk.Label(self.scrollable_frame, textvariable=self.status_var, foreground='#00ff88').pack()
        
        self.update_ui()

    def update_ui(self):
        # Обновление интерфейса при смене типа пранка.
        for w in self.dynamic_f.winfo_children(): w.destroy()
        p_type = self.prank_var.get()
        
        if p_type == "shutdown":
            self.shutdown_type = tk.StringVar(value="shutdown")
            ttk.Label(self.dynamic_f, text="Действие:", width=15).pack(side=tk.LEFT)
            ttk.Radiobutton(self.dynamic_f, text="Выключить", variable=self.shutdown_type, value="shutdown").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(self.dynamic_f, text="Рестарт", variable=self.shutdown_type, value="restart").pack(side=tk.LEFT, padx=5)
            ttk.Radiobutton(self.dynamic_f, text="Сон", variable=self.shutdown_type, value="sleep").pack(side=tk.LEFT, padx=5)
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, "system_update.bat")
        elif p_type == "youtube":
            ttk.Label(self.dynamic_f, text="URL:", width=15).pack(side=tk.LEFT)
            self.youtube_url = tk.StringVar(value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            ttk.Entry(self.dynamic_f, textvariable=self.youtube_url).pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, "surprise.bat")
        elif p_type == "close_apps":
            ttk.Label(self.dynamic_f, text="Режим: Закрытие всех запущенных программ", foreground='#00ff88').pack(side=tk.LEFT)
            self.filename_entry.delete(0, tk.END)
            self.filename_entry.insert(0, "close_apps.bat")

    def browse_path(self):
        # Открывает диалог выбора папки.
        p = filedialog.askdirectory()
        if p: self.path_var.set(p)

    def create_prank(self):
        # Собирает параметры и запускает prank_creator.exe.
        try:
            cpp_exe = self.base_path / "prank_creator.exe"
            if not cpp_exe.exists():
                messagebox.showerror("Ошибка", "prank_creator.exe не найден!")
                return

            p_type = self.prank_var.get()
            cmd = [str(cpp_exe), p_type, self.delay_var.get(), self.filename_entry.get(), self.path_var.get()]
            
            if p_type == "shutdown":
                cmd.append(self.shutdown_type.get())
            elif p_type == "youtube":
                cmd.extend([self.youtube_url.get(), "1"])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Успех", "Пранк успешно создан!")
            else:
                messagebox.showerror("Ошибка", result.stderr)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PrankCreatorApp(root)
    root.mainloop()