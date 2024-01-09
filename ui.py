import tkinter as tk
from tkinter import filedialog, messagebox

class InterfaceUtilisateur:
    def __init__(self, root):
        self.root = root
        self.root.title("Select SVG file")
        self.root.geometry("400x200")
        
        self.label = tk.Label(root, text="Click on the button to choose a SVG file")
        self.label.pack(pady=20)
        
        self.bouton_selection = tk.Button(root, text="Select a file", command=self.open_file)
        self.bouton_selection.pack(padx=20, pady=20)

        self.launch_button = tk.Button(root, text="Launch Program", command=self.launch_program)
        self.launch_button.pack(padx=20, pady=15)

        self.file_path = None
        
    def open_file(self):
        initial_directory = "../TpDeSynthese"
        self.file_path = filedialog.askopenfilename(initialdir=initial_directory, filetypes=[("Fichiers SVG", "*.svg")])
        if self.file_path:
            print(f'The SVG file path is:{self.file_path}')
        else:
            messagebox.showwarning("Warning", "You did not select a file")
    def launch_program(self):
        if self.file_path:
            # Place the code here that you want to execute when the launch button is clicked
            self.root.destroy()
            print(f"Launching program with the selected file: {self.file_path}")
        else:
            messagebox.showwarning("Warning", "No file selected to launch")

    def get_file_path(self):
        return self.file_path
