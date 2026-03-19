from tkinter import *
from utils import *


colors = load_theme()

def create_label(parent, t, r, c=0):
    Label(parent, text=t).grid(row=r, column=c, sticky="e", pady=5)
    
def make_a_tab(parent, text):
    btn = Button(parent, text=text, bg=colors.get("unselected_tab"), bd=0, padx=20, pady=2, 
                 activebackground=colors.get("selected_tab"), 
                 activeforeground="black",
                 width=10)
    btn.pack(side="left", padx=1)
    btn_cursor(btn)
    return btn  

def create_add_music_btn(parent, music_list, scrollable_frame, r=0, c=0, is_editing=False, directory=""):
    insert_music_btn = Button(parent, 
            command=lambda: add_music(insert_music_btn,  music_list, scrollable_frame, is_editing=is_editing, directory=directory), 
            text="Add music (.ogg)", 
            font=("Arial", 12, "bold"),
            bg=colors.get("music_btn_color"), fg="white", bd=0, padx=5, pady=5, 
            activebackground=colors.get("hovered_music_btn_color"), activeforeground="white")
    insert_music_btn.grid(row=r, column=c, sticky="nsew")
    insert_music_btn.bind("<Enter>", lambda e: insert_music_btn.configure(bg=colors.get("hovered_music_btn_color")))
    insert_music_btn.bind("<Leave>", lambda e: insert_music_btn.configure(bg=colors.get("music_btn_color")))
    
    return insert_music_btn

def create_music_interface(main_frame, music_list, can_add=True, is_editing=False, directory=""):
    music_frame = Frame(main_frame)
    music_frame.grid(row=6, column=1, columnspan=2, sticky="nsew", pady=10)
    music_frame.columnconfigure(0, weight=1)
    music_frame.rowconfigure(0, weight=1)
   
    
    canvas = Canvas(music_frame, bg=colors.get("secondary_color"), highlightthickness=0)
    scrollbar = Scrollbar(music_frame, orient=VERTICAL, command=canvas.yview)
    
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")
    
    canvas.configure(yscrollcommand=scrollbar.set)
        
    scrollable_frame = Frame(canvas, bg="gray")
    
    if can_add:
        create_add_music_btn(music_frame, music_list, scrollable_frame, is_editing=is_editing, directory=directory)
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    def on_frame_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    return scrollable_frame


def load_mod(main_frame, directory):
    if not os.path.exists(directory):
        return
    music_list = []
    music_path = os.path.join(directory, "music")
    music_files = os.listdir(music_path)
    for file in music_files:
        if file[-4:] == ".ogg":
            music_list.append({
                "file": os.path.normpath(os.path.join(music_path, file)),
                "name": file
            })
    music_frame = create_music_interface(main_frame, music_list, is_editing=True, directory=music_path)
    show_music(music_frame, music_list, delete_song, delete_file=True)