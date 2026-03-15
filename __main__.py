from tkinter import *
from utils import *
from menu.create_menu import *
from menu.edit_menu import *

colors = load_theme()

active_tab = "create"

def make_a_tab(parent, text):
    btn = Button(parent, text=text, bg=colors.get("unselected_tab"), bd=0, padx=20, pady=2, activebackground=colors.get("selected_tab"), activeforeground="black")
    btn.pack(side="left", padx=1)
    btn_cursor(btn)
    return btn


def interface_controller(switching_to, func):
    global active_tab
    if switching_to != active_tab:
        func()
        active_tab = switching_to

def main():
    root = Tk()
    root.title("Hoi4 Radio Creator")
    root.geometry("1200x700")
        
    music_list = []
    
    tabs_frame = Frame(root)
    tabs_frame.grid(row=0, column=0, sticky="ew")
    tabs_frame.configure(height=20, bg=colors.get("secondary_color"))
    
    create_tab = make_a_tab(tabs_frame, "Create")
    create_tab.configure(bg=colors.get("selected_tab"))
    
    edit_tab = make_a_tab(tabs_frame, "Edit")
    
    create_tab.configure(command=lambda: (interface_controller("create", lambda: create_menu(main_frame, music_list)),
                                        create_tab.configure(bg=colors.get("selected_tab")), 
                                        edit_tab.configure(bg=colors.get("unselected_tab"))))
    edit_tab.configure(command=lambda: (interface_controller("edit", lambda: edit_menu(main_frame)),
                                        edit_tab.configure(bg=colors.get("selected_tab")), 
                                        create_tab.configure(bg=colors.get("unselected_tab"))))
    
    
    
    main_frame = ttk.Frame(root)
    root.columnconfigure(0, weight=1)
    
    
    create_menu(main_frame, music_list)
    
    root.mainloop()


if __name__ == "__main__":
    main()