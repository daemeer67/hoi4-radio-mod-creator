from tkinter import *
from tkinter import ttk
from utils import *
from create import create


def create_menu(root, music_list):
    
    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0, sticky="nsew")
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)  
    
    # Radio Station Name
    Label(main_frame, text="Radio Station Name:").grid(row=1, column=0, sticky="e", pady=5)
    radio_station_name_entry = Entry(main_frame)
    radio_station_name_entry.grid(row=1, column=1, columnspan=2, sticky="we", ipady=3, ipadx=3)
    
    # HOI4 mod directory
    Label(main_frame, text="HOI4 mod directory:").grid(row=2, column=0, sticky="e")
    hoi4_mod_directory = Entry(main_frame)
    hoi4_mod_directory.grid(row=2, column=1, sticky="we", ipady=3, ipadx=3, pady=5)
    Button(main_frame, text="...", 
           command=lambda: change_directory(hoi4_mod_directory, 
                                            default_directory=os.path.expanduser("~\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod"))).grid(row=2, column=2, padx=5)
    
    load_selected_directory(hoi4_mod_directory)
    
    # Mod Thumbnail
    Label(main_frame, text="Mod Thumbnail:").grid(row=3, column=0, sticky="e", pady=5)
    mod_thumbnail_entry = Entry(main_frame)
    mod_thumbnail_entry.grid(row=3, column=1, sticky="we", pady=5, ipady=3, ipadx=3)
    Button(main_frame, text="...", command=lambda: select_file(mod_thumbnail_entry, 
                                                               filetypes=[("Image files", "*.jpg *.jpeg *.png")])).grid(row=3, column=2, padx=5)
    
    # Radio Station Cover
    Label(main_frame, text="Radio Station Cover:").grid(row=4, column=0, sticky="e", pady=5)
    radio_station_cover_entry = Entry(main_frame)
    radio_station_cover_entry.grid(row=4, column=1, sticky="we", pady=5, ipady=3, ipadx=3)
    Button(main_frame, text="...", command=lambda: select_file(radio_station_cover_entry, 
                                                               filetypes=[("Image files", "*.dds")])).grid(row=4, column=2, padx=5)
    
    # Music Files
    music_frame = Frame(main_frame)
    music_frame.grid(row=6, column=1, columnspan=2, sticky="nsew", pady=10)
    music_frame.columnconfigure(0, weight=1)
    music_frame.rowconfigure(0, weight=1)
    
    music_btn_color = "#4CAF50"
    hovered_music_btn_color = "#45a049"
    
    
   
    insert_music_btn = Button(music_frame, command=lambda: add_music(insert_music_btn, 
                                                                     music_list, scrollable_frame), text="Add music (.ogg)", font=("Arial", 12, "bold"), bg=music_btn_color, fg="white", bd=0, padx=5, pady=5, activebackground=hovered_music_btn_color, activeforeground="white")
    insert_music_btn.grid(row=0, column=0, sticky="nsew")
    insert_music_btn.bind("<Enter>", lambda e: insert_music_btn.configure(bg=hovered_music_btn_color))
    insert_music_btn.bind("<Leave>", lambda e: insert_music_btn.configure(bg=music_btn_color))
    
    canvas = Canvas(music_frame, bg="#d6d6d6")
    scrollbar = Scrollbar(music_frame, orient=VERTICAL, command=canvas.yview)
    
    canvas.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    
    scrollable_frame = Frame(canvas, bg="gray")
    
    
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    def on_frame_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    scrollable_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    Button(main_frame, text="Create Mod", command=lambda: create(root,
                                                                 music_list, 
                                                                 radio_station_name_entry.get(), 
                                                                 hoi4_mod_directory.get(),
                                                                 thumbnail_path=mod_thumbnail_entry.get(),
                                                                 radio_station_cover_path=radio_station_cover_entry.get()
                                                                 )).grid(row=7, column=1, pady=15)
    
    
    root.mainloop()