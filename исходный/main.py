import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess
import sys
import os
import shutil

class PrankCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 PrankMaster Pro")
        self.root.geometry("700x500")
        self.root.configure(bg='#1e1e1e')
        
        # Определяем путь к программе
        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys.executable).parent
        else:
            self.base_path = Path(__file__).parent
        
        self.set_dark_theme()
        self.create_widgets()
    
    def set_dark_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('.', background='#1e1e1e', foreground='white')
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='white')
        style.configure('TLabelframe', background='#2d2d2d', foreground='white')
        style.configure('TLabelframe.Label', background='#2d2d2d', foreground='#00ff88')
        style.configure('TButton', background='#363636', foreground='white')
        style.configure('TRadiobutton', background='#1e1e1e', foreground='white')
        style.configure('TEntry', fieldbackground='#363636', foreground='white')
        style.configure('TSpinbox', fieldbackground='#363636', foreground='white')
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, 
                              text="🎭 PrankMaster Pro", 
                              font=('Arial', 20, 'bold'),
                              fg='#00ff88',
                              bg='#1e1e1e')
        title_label.pack(pady=10)
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Выбор типа пранка
        prank_frame = ttk.LabelFrame(main_frame, text="🔧 Выберите тип пранка", padding=15)
        prank_frame.pack(fill=tk.X, pady=10)
        
        self.prank_var = tk.StringVar(value="shutdown")
        
        ttk.Radiobutton(prank_frame, text="🔴 Выключение/Перезагрузка/Спящий режим", 
                       variable=self.prank_var, value="shutdown").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(prank_frame, text="🎥 Видео пранк (YouTube)", 
                       variable=self.prank_var, value="youtube").pack(anchor=tk.W, pady=5)
        ttk.Radiobutton(prank_frame, text="💀 Fake BSOD (Синий экран)", 
                       variable=self.prank_var, value="fake_bsod").pack(anchor=tk.W, pady=5)
        
        # Настройки пранка
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Настройки пранка", padding=10)
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Задержка
        delay_frame = ttk.Frame(settings_frame)
        delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delay_frame, text="Задержка (сек):").pack(side=tk.LEFT)
        self.delay_var = tk.StringVar(value="5")
        ttk.Spinbox(delay_frame, from_=1, to=60, textvariable=self.delay_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Настройки выключения
        self.shutdown_frame = ttk.Frame(settings_frame)
        self.shutdown_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.shutdown_frame, text="Действие:").pack(side=tk.LEFT)
        self.shutdown_type = tk.StringVar(value="shutdown")
        
        ttk.Radiobutton(self.shutdown_frame, text="Выключение", 
                       variable=self.shutdown_type, value="shutdown").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.shutdown_frame, text="Перезагрузка", 
                       variable=self.shutdown_type, value="restart").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.shutdown_frame, text="Спящий режим", 
                       variable=self.shutdown_type, value="sleep").pack(side=tk.LEFT, padx=5)
        
        # Настройки YouTube
        self.youtube_frame = ttk.Frame(settings_frame)
        
        ttk.Label(self.youtube_frame, text="YouTube ссылка:").pack(side=tk.LEFT)
        self.youtube_url = tk.StringVar(value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        ttk.Entry(self.youtube_frame, textvariable=self.youtube_url, width=40).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.youtube_frame, text="Количество:").pack(side=tk.LEFT, padx=(10,0))
        self.youtube_count = tk.StringVar(value="3")
        ttk.Spinbox(self.youtube_frame, from_=1, to=10, textvariable=self.youtube_count, width=5).pack(side=tk.LEFT, padx=5)
        
        # Fake BSOD настройки (пустой фрейм)
        self.fake_bsod_frame = ttk.Frame(settings_frame)
        
        # Сохранение файла
        output_frame = ttk.LabelFrame(main_frame, text="📁 Сохранить файл", padding=10)
        output_frame.pack(fill=tk.X, pady=10)
        
        # Имя файла
        filename_frame = ttk.Frame(output_frame)
        filename_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filename_frame, text="Имя файла:").pack(side=tk.LEFT)
        self.filename_var = tk.StringVar(value="prank.bat")
        ttk.Entry(filename_frame, textvariable=self.filename_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # Папка для сохранения
        path_frame = ttk.Frame(output_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="Папка:").pack(side=tk.LEFT)
        self.path_var = tk.StringVar(value=str(Path.home() / "Desktop"))
        path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=30)
        path_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(path_frame, text="Обзор", command=self.browse_path).pack(side=tk.LEFT)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🎭 Создать пранк", command=self.create_prank, width=20).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="ℹ️ О программе", command=self.show_info, width=15).pack(side=tk.LEFT, padx=10)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов к созданию пранков...")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground='#00ff88')
        status_label.pack(pady=10)
        
        self.update_settings_display()
        self.prank_var.trace('w', lambda *args: self.update_settings_display())
    
    def update_settings_display(self):
        # Скрываем все фреймы настроек
        self.shutdown_frame.pack_forget()
        self.youtube_frame.pack_forget()
        self.fake_bsod_frame.pack_forget()
        
        # Показываем нужный фрейм
        if self.prank_var.get() == "shutdown":
            self.shutdown_frame.pack(fill=tk.X, pady=5)
            self.filename_var.set("shutdown.bat")
        elif self.prank_var.get() == "youtube":
            self.youtube_frame.pack(fill=tk.X, pady=5)
            self.filename_var.set("youtube.bat")
        else:  # fake_bsod
            self.fake_bsod_frame.pack(fill=tk.X, pady=5)
            self.filename_var.set("fake_bsod.bat")
    
    def browse_path(self):
        path = filedialog.askdirectory(title="Выберите папку для сохранения")
        if path:
            self.path_var.set(path)
    
    def show_info(self):
        info = """🎭 PrankMaster Pro 

Программа для создания безобидных BAT-пранков.

Возможности:
• Выключение/перезагрузка компьютера
• Открытие YouTube видео
• Fake BSOD (синий экран)

Используйте ответственно!
Только с согласия друзей."""
        messagebox.showinfo("О программе", info)
    
    def create_prank(self):
        try:
            # Получаем параметры из GUI
            prank_type = self.prank_var.get()
            delay = self.delay_var.get()
            filename = self.filename_var.get()
            save_path = self.path_var.get()
            
            # Проверяем C++ программу (рядом с програмой)
            cpp_program = self.base_path / "prank_creator.exe"
            if not cpp_program.exists():
                messagebox.showerror("Ошибка", f"C++ программа не найдена!\n{cpp_program}")
                return
            
            # Проверяем Fake BSOD (рядом с програмой)
            fake_bsod_exe = self.base_path / "FakeBsod.exe"
            if prank_type == "fake_bsod" and not fake_bsod_exe.exists():
                messagebox.showerror("Ошибка", f"FakeBsod.exe не найден!\n{fake_bsod_exe}")
                return
            
            # Формируем команду для C++ программы
            cmd = [str(cpp_program), prank_type, delay, filename, save_path]
            
            if prank_type == "shutdown":
                cmd.append(self.shutdown_type.get())
            elif prank_type == "youtube":
                cmd.extend([self.youtube_url.get(), self.youtube_count.get()])
            # Для fake_bsod дополнительных параметров не нужно
            
            # Запускаем C++ программу
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Если это Fake BSOD - копируем FakeBsod.exe в папку с BAT файлом
                if prank_type == "fake_bsod":
                    target_fake_bsod = Path(save_path) / "FakeBsod.exe"
                    try:
                        shutil.copy2(fake_bsod_exe, target_fake_bsod)
                        self.status_var.set("Пранк успешно создан! ✅ (FakeBsod.exe скопирован)")
                    except Exception as copy_error:
                        self.status_var.set("Ошибка копирования FakeBsod.exe! ❌")
                        messagebox.showerror("Ошибка", f"Не удалось скопировать FakeBsod.exe: {copy_error}")
                        return
                else:
                    self.status_var.set("Пранк успешно создан! ✅")
                
                full_path = Path(save_path) / filename
                messagebox.showinfo("Успех", f"Файл создан:\n{full_path}")
            else:
                self.status_var.set("Ошибка создания пранка! ❌")
                messagebox.showerror("Ошибка", f"C++ программа вернула ошибку:\n{result.stderr}")
                
        except Exception as e:
            self.status_var.set("Ошибка! ❌")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrankCreator(root)
    root.mainloop()