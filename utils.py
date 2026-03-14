import os
from tkinter import *
from tkinter import filedialog
import json

file_path = "save.txt"

def btn_cursor(widget):
    widget.bind("<Enter>", lambda e: widget.config(cursor="hand2"))
    widget.bind("<Leave>", lambda e: widget.config(cursor=""))

def load_theme():
    theme = {}
    with open("theme.json", "r") as file:
        theme = json.load(file)
    return theme

def change_directory(entry, default_directory=os.getcwd()):
    if not (default_directory and os.path.exists(default_directory)):
        default_directory = os.getcwd()
        
    directory = filedialog.askdirectory(initialdir=default_directory)
    entry.delete(0, END)
    entry.insert(0, directory)
    with open(file_path, "w") as file:
        file.write(directory)
        

def load_selected_directory(entry):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            saved_directory = file.read().strip()
            entry.delete(0, END)
            entry.insert(0, saved_directory)
            
def select_file(entry, filetypes=[("All files", "*.*")]):
    file = filedialog.askopenfilename(filetypes=filetypes)
    entry.delete(0, END)
    entry.insert(0, file)


def add_music_to_list(music_tuple):
    result = []
    for file in music_tuple:
        result.append(
            {
                "file": file,
                "name": os.path.basename(file)
            }
        )
        
    return result


def clear_music_interface(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_music(frame, music_list):
    clear_music_interface(frame)
    
    for music in music_list:
       colors = load_theme()
       default_color = colors.get("default_music_color")
       hovered_color = colors.get("hovered_music_color")
       
       button_color = colors.get("dlt_button_color")
       hovered_button_color = colors.get("hovered_dlt_button_color")
       
       row = Frame(frame, bg=default_color, highlightbackground=hovered_color, highlightthickness=0.5)
       row.pack(fill="x", ipadx=10)
       label = Label(row, text=f"{music["name"]}", anchor="w", bg=default_color)
       label.pack(side="left", fill="x", expand=True)
       button = Button(row, text="x", 
                       command=lambda m=music, r=row, ml=music_list: delete_song(r, m, music_list), 
                       bg=button_color, fg="white", font=("Arial", 10, "bold"), bd=0)
       button.pack(side="right", ipadx=5)
       label.bind("<Enter>", lambda e, r=row, l=label, b=button: (r.configure(bg=hovered_color), l.configure(bg=hovered_color), b.configure(bg=hovered_button_color)))
       label.bind("<Leave>", lambda e, r=row, l=label, b=button: (r.configure(bg=default_color), l.configure(bg=default_color), b.configure(bg=button_color)))
       
       button.bind("<Enter>", lambda e, b=button: (b.configure(bg=hovered_button_color)))
       button.bind("<Leave>", lambda e, b=button: (b.configure(bg=button_color)))
    
    

def delete_song(row, music, music_list):
    for i in range(len(music_list)):
        if music_list[i]["file"] == music["file"]:
            music_list.remove(music_list[i])
            break
    row.destroy()
    show_music(row.master, music_list)
    


def add_music(btn, music_list, frame):
        color = load_theme().get("music_btn_color")
        files  = filedialog.askopenfilenames(filetypes=[("OGG files", "*.ogg")])
        btn.configure(bg=color)
        added_music = add_music_to_list(files)
        for music in added_music:
            music_list.append(music)
        show_music(frame, music_list)
        