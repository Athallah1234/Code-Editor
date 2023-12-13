import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog, filedialog, messagebox
from ttkthemes import ThemedTk
import pdb

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Code Editor")
        self.root.geometry("800x600")

        # Create a text widget
        self.text_editor = ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 12))
        self.text_editor.pack(expand=True, fill='both')

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # View menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Toggle Full Screen", command=self.toggle_fullscreen)
        self.view_menu.add_command(label="Zoom In", command=self.zoom_in)
        self.view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Run menu
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run", command=self.run_code)
        self.run_menu.add_separator()
        self.run_submenu = tk.Menu(self.run_menu, tearoff=0)
        self.run_submenu.add_command(label="Run Selected", command=self.run_selected_code)
        self.run_submenu.add_command(label="Run All", command=self.run_all_code)
        self.run_menu.add_cascade(label="Run Options", menu=self.run_submenu)
        self.run_menu.add_command(label="Debug", command=self.debug_code)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about_dialog)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_editor.get(1.0, tk.END)
                file.write(content)

    def cut(self):
        self.text_editor.event_generate("<<Cut>>")

    def copy(self):
        self.text_editor.event_generate("<<Copy>>")

    def paste(self):
        self.text_editor.event_generate("<<Paste>>")

    def find_text(self):
        target = simpledialog.askstring("Find", "Enter text to find:")
        if target:
            start_pos = self.text_editor.search(target, 1.0, tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(target)}c"
                self.text_editor.tag_add(tk.SEL, start_pos, end_pos)
                self.text_editor.mark_set(tk.INSERT, end_pos)
                self.text_editor.see(tk.INSERT)

    def replace_text(self):
        target = simpledialog.askstring("Replace", "Enter text to replace:")
        if target:
            replacement = simpledialog.askstring("Replace", f"Replace '{target}' with:")
            if replacement:
                start_pos = self.text_editor.search(target, 1.0, tk.END)
                while start_pos:
                    end_pos = f"{start_pos}+{len(target)}c"
                    self.text_editor.delete(start_pos, end_pos)
                    self.text_editor.insert(start_pos, replacement)
                    start_pos = self.text_editor.search(target, end_pos, tk.END)

    def run_code(self):
        code_to_run = self.text_editor.get(1.0, tk.END)
        try:
            exec(code_to_run)
        except Exception as e:
            print(f"Error: {e}")

    def debug_code(self):
        code_to_debug = self.text_editor.get(1.0, tk.END)
        try:
            pdb.run(code_to_debug)
        except Exception as e:
            print(f"Error in debugging: {e}")

    def run_selected_code(self):
        selected_code = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
        try:
            exec(selected_code)
        except Exception as e:
            print(f"Error: {e}")

    def run_all_code(self):
        code_to_run = self.text_editor.get(1.0, tk.END)
        try:
            exec(code_to_run)
        except Exception as e:
            print(f"Error: {e}")

    def show_about_dialog(self):
        about_message = "Modern Code Editor\nVersion 1.0\n\n© 2023 Your Name"
        messagebox.showinfo("About", about_message)

    def toggle_fullscreen(self):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def zoom_in(self):
        current_size = self.text_editor.cget("font").split()[1]
        new_size = int(current_size) + 1
        self.text_editor.configure(font=("Consolas", new_size))

    def zoom_out(self):
        current_size = self.text_editor.cget("font").split()[1]
        new_size = max(8, int(current_size) - 1)
        self.text_editor.configure(font=("Consolas", new_size))

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # You can choose a different theme
    code_editor = CodeEditor(root)
    root.mainloop()

