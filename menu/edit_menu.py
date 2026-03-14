from tkinter import *
from tkinter import ttk
from utils import *


def edit_menu(root):
    
    main_frame = ttk.Frame(root)
    main_frame.grid(row=1, column=0, sticky="nsew")
    
    root.columnconfigure(0, weight=1)
    
    main_frame.columnconfigure(1, weight=1)