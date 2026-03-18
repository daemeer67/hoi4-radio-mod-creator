from tkinter import *
from utils import *
from modules import *
from tkinter import messagebox

def edit(main_frame, directory):
    root = main_frame.master
    
    if directory.strip() == "":
        messagebox.showerror("Warning", "Directory cannot be empty.")
        return
    if not os.path.exists(directory):
        messagebox.showerror("Error", "Directory does not exist.")
        return
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "The selected path is not a directory.")
        return
    
    
    return