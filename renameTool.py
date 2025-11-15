import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime
import re 
import Setting 

class FileRenamerApp:
    def __init__(self, master):
        self.master = master
        master.title("ファイル名一括変更ツール")

        initial_path = (
            Setting.DEFAULT_TARGET_FOLDER
            if Setting.DEFAULT_TARGET_FOLDER
            else "フォルダを選択"
        )
        self.target_dir = tk.StringVar(value=initial_path)
        self.dept_code = tk.StringVar(value=Setting.DEPARTMENT_CODES[0])
        self.date_input = tk.StringVar()

        self.setup_folder_selection()
        self.setup_input_form()
        self.setup_execute_button()

    def open_folder_dialog(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_dir.set(folder_selected)

    def setup_folder_selection(self):
        folder_frame = ttk.Frame(self.master, padding="10")
        folder_frame.pack(fill='x')

        ttk.Label(folder_frame, text="対象フォルダ:").pack(side='left', padx=(0, 10))
        ttk.Entry(folder_frame, textvariable=self.target_dir, width=50, state='readonly').pack(side='left', fill='x', expand=True)
        ttk.Button(folder_frame, text="参照", command=self.open_folder_dialog).pack(side='left', padx=(10, 0))

    def setup_input_form(self):
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.pack(fill='x')

        ttk.Label(input_frame, text="部門コード:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        dept_combobox = ttk.Combobox(
            input_frame,
            textvariable=self.dept_code,
            values=Setting.DEPARTMENT_CODES,
            state='readonly'
        )
        dept_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="日付 (YYYYMMDD):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        ttk.Entry(input_frame, textvariable=self.date_input, width=15).grid(row=1, column=1, padx=5, pady=5, sticky='w')

        input_frame.grid_columnconfigure(1, weight=1)

    def execute_renaming(self):
        target_folder = self.target_dir.get()
        dept_code_full = self.dept_code.get()
        date_str = self.date_input.get()
        
        if target_folder == "フォルダを選択してください" or not os.path.isdir(target_folder):
            messagebox.showerror("エラー", "有効な対象フォルダを選択してください。")
            return

        if not (len(date_str) == 8 and date_str.isdigit()):
            messagebox.showerror("エラー", "日付は半角数字8桁 (YYYYMMDD) で入力してください。")
            return
        
        try:
            datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            messagebox.showerror("エラー", "入力された日付は存在しません。正しい日付を入力してください。")
            return

        try:
            prefix = dept_code_full.split(" ")[0]
            
            self.perform_renaming(target_folder, prefix, date_str)
            
            messagebox.showinfo("成功", f"ファイルのリネームを完了しました。\n(プレフィックス: {prefix}_{date_str})")

        except Exception as e:
            messagebox.showerror("致命的なエラー", f"予期せぬエラーが発生しました: {e}")

    def perform_renaming(self, folder, prefix, date_str):
        
        for filename in os.listdir(folder):
            
            if os.path.isdir(os.path.join(folder, filename)):
                continue

            name, ext = os.path.splitext(filename)
            
            new_name = f"{prefix}_{date_str}_{name}{ext}"
            
            if filename == new_name:
                continue

            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            
            os.rename(old_path, new_path)


    def setup_execute_button(self):
        execute_frame = ttk.Frame(self.master, padding="10")
        execute_frame.pack(fill='x')
        
        ttk.Button(execute_frame, text="実行", command=self.execute_renaming).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()