from tkinter import *
from utils import *
from menu.create_menu import *
import json

colors = load_theme()

def make_a_tab(parent, text):
    return Button(parent, text=text, bg=colors.get("primary_color"), bd=0, padx=20, pady=2, activebackground=colors.get("secondary_color"), activeforeground="black")

def main():
    root = Tk()
    root.title("Hoi4 Radio Creator")
    root.geometry("1200x700")
    
    
    music_list = []
    
    tabs_frame = Frame(root)
    tabs_frame.grid(row=0, column=0, sticky="ew")
    tabs_frame.configure(height=20, bg=colors.get("secondary_color"))
    
    create_tab = make_a_tab(tabs_frame, "Create")
    create_tab.pack(side="left", padx=1)
    
    edit_tab = make_a_tab(tabs_frame, "Edit")
    edit_tab.pack(side="left", padx=1)
    
    btn_cursor(create_tab)
    btn_cursor(edit_tab)
    
    create_menu(root, music_list)


if __name__ == "__main__":
    main()