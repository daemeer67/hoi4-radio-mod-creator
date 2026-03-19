from tkinter import *
from utils import *
from create import create
from modules import *

def grid_entry(entry, row, column=1, **kwargs):
    entry.grid(row=row, column=column, sticky="we", ipady=3, ipadx=3, **kwargs)





def create_menu(main_frame, music_list):
    delete_children(main_frame)
    
    colors = load_theme()
    root = main_frame.master
    
    main_frame.grid(row=1, column=0, sticky="nsew")
    
    
    
    main_frame.columnconfigure(1, weight=1)  
    
    # Radio Station Name
    create_label(main_frame, "Radio Station Name:", 1)
    radio_station_name_entry = Entry(main_frame)
    grid_entry(radio_station_name_entry, 1)
    
    # HOI4 mod directory
    create_label(main_frame, "HOI4 mod directory:", 2)
    hoi4_mod_directory = Entry(main_frame)
    grid_entry(hoi4_mod_directory, 2)
    Button(main_frame, text="...", 
           command=lambda: change_directory(hoi4_mod_directory, 
                                            default_directory=os.path.expanduser("~\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod"))).grid(row=2, column=2, padx=5)
    
    load_selected_directory(hoi4_mod_directory)
    
    # Mod Thumbnail
    create_label(main_frame, "Mod Thumbnail:", 3)
    mod_thumbnail_entry = Entry(main_frame)
    grid_entry(mod_thumbnail_entry, 3)
    Button(main_frame, text="...", command=lambda: select_file(mod_thumbnail_entry, 
                                                               filetypes=[("Image files", "*.jpg *.jpeg *.png")])).grid(row=3, column=2, padx=5)
    
    # Radio Station Cover
    create_label(main_frame, "Radio Station Cover:", 4)
    radio_station_cover_entry = Entry(main_frame)
    grid_entry(radio_station_cover_entry, 4)
    Button(main_frame, text="...", command=lambda: select_file(radio_station_cover_entry, 
                                                               filetypes=[("Image files", "*.dds")])).grid(row=4, column=2, padx=5)
    
    # Music Files
    create_music_interface(main_frame, music_list)

    Button(main_frame, text="Create Mod", command=lambda: create(root,
                                        music_list, 
                                        radio_station_name_entry.get(), 
                                        hoi4_mod_directory.get(),
                                        thumbnail_path=mod_thumbnail_entry.get(),
                                        radio_station_cover_path=radio_station_cover_entry.get()
                                        )).grid(row=7, column=1, pady=15)
    