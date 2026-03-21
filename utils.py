import os
from tkinter import *
from tkinter import filedialog
import json
import shutil
from pathlib import Path


file_path = "save.txt"


def delete_children(widget):
    for child in widget.winfo_children():
        child.destroy()

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

def show_music(frame, music_list, func, **kwargs):
    delete_children(frame)
    
    colors = load_theme()
    for music in music_list:
       default_color = colors.get("default_music_color")
       hovered_color = colors.get("hovered_music_color")
       
       button_color = colors.get("dlt_button_color")
       hovered_button_color = colors.get("hovered_dlt_button_color")
       
       row = Frame(frame, bg=default_color, highlightbackground=hovered_color, highlightthickness=0.5)
       row.pack(fill="x", ipadx=10)
       label = Label(row, text=f"{music['name']}", anchor="w", bg=default_color)
       label.pack(side="left", fill="x", expand=True)
       button = Button(row, text="x", 
                       command=lambda m=music, r=row, ml=music_list: func(r, m, ml, **kwargs), 
                       bg=button_color, fg="white", font=("Arial", 10, "bold"), bd=0)
       button.pack(side="right", ipadx=5)
       label.bind("<Enter>", lambda e, r=row, l=label, b=button: (r.configure(bg=hovered_color), l.configure(bg=hovered_color), b.configure(bg=hovered_button_color)))
       label.bind("<Leave>", lambda e, r=row, l=label, b=button: (r.configure(bg=default_color), l.configure(bg=default_color), b.configure(bg=button_color)))
       
       button.bind("<Enter>", lambda e, b=button: (b.configure(bg=hovered_button_color)))
       button.bind("<Leave>", lambda e, b=button: (b.configure(bg=button_color)))
    
    

def delete_song(row, music, music_list, delete_file=False):
    for i, item in enumerate(music_list):
        file = os.path.normpath(item["file"])
        target = os.path.normpath(music["file"])

        if file == target:
            if delete_file:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                        print("song removed successfully")
                    except Exception as e:
                        print("Error deleting:", e)
                else:
                    print("song not found")

            del music_list[i]
            update_iw_music_files(Path(target).parent, music_list)
            break

    row.destroy()
    show_music(row.master, music_list, delete_song, delete_file=delete_file)
        



def add_music(btn, music_list, frame, is_editing=False, directory=""):
    color = load_theme().get("music_btn_color")
    files  = filedialog.askopenfilenames(filetypes=[("OGG files", "*.ogg")])
    btn.configure(bg=color)
    added_music = add_music_to_list(files)
    existing_files = {m["name"] for m in music_list}
    for music in added_music:
        if music["name"] in existing_files:
            continue
        
        if is_editing:
            shutil.copy2(music["file"], directory)
            new_path = os.path.join(directory, music["name"])
            print(new_path)
            music["file"] = new_path
        music_list.append(music)
    show_music(frame, music_list, delete_song, delete_file=is_editing)
    
    if is_editing: update_iw_music_files(directory, music_list)
    
# this function is intended to be used when there are changes in the music list when the user is in the editing tab
def update_iw_music_files(directory, music_list):
    station_name = os.path.basename(directory)
    templates = ""
    with open("iw_music_templates.json", "r") as file:
        templates = json.load(file)
        
    txt_path = os.path.normpath(os.path.join(directory, "iw_music.txt"))
    asset_path = os.path.normpath(os.path.join(directory, "iw_music.asset"))
        
    with open(txt_path, "w") as file:
        text = "music_station = \"iw_test_station\"\n"
        text.replace("test_station", station_name)
        for music in music_list:
            text += templates["txt"].replace("test_song", music["name"])
        file.write(text)
    
    with open(asset_path, "w") as file:
        text = ""
        for music in music_list:
            text += templates["asset"].replace("test_song", music["name"].replace(".ogg", ""))
        file.write(text)