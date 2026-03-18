from tkinter import *
from utils import *
from modules import *

def edit_menu(main_frame):
    delete_children(main_frame)
    
    selected_directory = False
    
    create_label(main_frame, "Mod directory:", 0)
    mod_directory_entry = Entry(main_frame)
    mod_directory_entry.grid(row=0, column=1, sticky="we", pady=5, ipady=3, ipadx=3)
    Button(main_frame, text="...", 
        command=lambda: change_directory(mod_directory_entry, 
        default_directory=os.path.expanduser("~\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod"))).grid(row=0, column=2, padx=5)
    Button(main_frame, text="Load Mod", command=lambda: load_mod(main_frame, mod_directory_entry.get())).grid(row=0, column=3, pady=5)
    
    music_interface = create_music_interface(main_frame, [], can_edit=selected_directory)
    
    selected_directory = True