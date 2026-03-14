from tkinter import messagebox
import shutil
import os

def create(root, music_list, original_radio_station_name, output_directory, thumbnail_path="", radio_station_cover_path=""):
    root.config(cursor = "wait")
    root.update()
    
    template_path = "./template"
    
    if original_radio_station_name.strip() == "":
        messagebox.showerror("Warning", "Radio station name cannot be empty.")
        return
    
    radio_station_name = original_radio_station_name.strip().replace(" ", "_").lower()

    new_station_path = os.path.join(output_directory, radio_station_name)

    shutil.copytree(template_path, new_station_path)

    if not os.path.exists(os.path.join(output_directory, radio_station_name)):
        messagebox.showerror("Error", "Failed to create the radio station mod")
        return

    # Interface
    cwm_music = open(os.path.join(new_station_path, "interface", "cwm_music.gui"), "r+")
    cwm_music_content = cwm_music.read()

    cwm_music_content = cwm_music_content.replace("name = \"iw_test_station_faceplate\"", f"name = \"{radio_station_name}_faceplate\"")
    cwm_music_content = cwm_music_content.replace("name = \"iw_test_station_stations_entry\"", f"name = \"{radio_station_name}_stations_entry\"")

    cwm_music.seek(0)
    cwm_music.write(cwm_music_content)
    cwm_music.truncate()
    cwm_music.close()


    # Music (must be .ogg files)
    for music in music_list:
        shutil.copy(music["file"], os.path.join(new_station_path, "music", music["name"]))

    # Modification of iw_music.asset
    iw_music_asset = open(os.path.join(new_station_path, "music", "iw_music.asset"), "w")

    music_asset_text = ""
    asset_template = """
    music = {
    	name = "test_song"
    	file = "test_song.ogg"
    }
    """

    for music in music_list:
        music_asset_text += asset_template.replace("test_song", music["name"].replace(".ogg", ""))

    iw_music_asset.write(music_asset_text)
    iw_music_asset.close()

    # Modification of iw_music.txt
    iw_music_txt = open(os.path.join(new_station_path, "music", "iw_music.txt"), "w", encoding="utf-8")

    music_text = f"music_station = \"{radio_station_name}\"\n"
    music_template = """
    music = {
    	song = "test_song"
    	chance = {
    		factor = 0
    		modifier = {
    			factor = 100
    		}
    	}
    }
    """

    for music in music_list:
        music_text += f"{music_template.replace("test_song", music["name"].replace(".ogg", ""))}\n"

    iw_music_txt.write(music_text)
    iw_music_txt.close()

    # A small change in the descriptor file
    descriptor_file = open(os.path.join(new_station_path, "descriptor.mod"), "r+")
    descriptor_content = descriptor_file.read()
    descriptor_content = descriptor_content.replace("HOI4 Music Station Template", original_radio_station_name)
    descriptor_file.seek(0)
    descriptor_file.write(descriptor_content)
    descriptor_file.truncate()
    descriptor_file.close()

    # Localisation
    localisation_file = open(os.path.join(new_station_path, "localisation", "music_station_l_english.yml"), "r+", encoding="utf-8-sig")
    localisation_text = f"l_english:\n {radio_station_name}_TITLE:0 \"{original_radio_station_name.replace("_"," ")}\"\n"

    # for music in music_list:
    #     localisation_text += f" {music.replace(' ', '_').replace('.ogg', '')}:0 \"{music.replace("_", " ").replace(".ogg", "")}\"\n"

    localisation_file.seek(0)
    localisation_file.truncate()
    localisation_file.write(localisation_text)
    localisation_file.close()

    # Create .mod file for the radio station
    mod_file_path = os.path.join(output_directory, f"{radio_station_name}.mod")

    mod_file_content = f"""version="1.17.4"
    tags={{
    	"Sound"
    }}
    name="{original_radio_station_name}"
    supported_version="1.17.4.1"
    path="C:/Users/user/Documents/Paradox Interactive/Hearts of Iron IV/mod/{radio_station_name}" """

    with open(mod_file_path, "w", encoding="utf-8") as mod_file:
        mod_file.write(mod_file_content)
        mod_file.close()

    # Replace the thumbnail
    if thumbnail_path and os.path.isfile(thumbnail_path):
        shutil.copy(thumbnail_path, os.path.join(new_station_path, "thumbnail.jpg"))
        
    if radio_station_cover_path and os.path.isfile(radio_station_cover_path):
        radio_cover_filename = os.path.basename(radio_station_cover_path)
        shutil.copy(radio_station_cover_path, os.path.join(new_station_path, "gfx", f"{radio_cover_filename}"))
        with open(os.path.join(new_station_path, "interface", "cwm_music.gfx"), "w") as cwm_music_file:
            cwm_music_file.write(
                f"""spriteTypes = {{
    spriteType = {{
		name = "GFX_{radio_cover_filename.split('.')[0]}"
		textureFile = "gfx/{radio_cover_filename}"
		noOfFrames = 2
	}}
}}"""
            )
            cwm_music_file.close()
    
    
    root.config(cursor = "")
    
    messagebox.showinfo("Success", "The radio station has been created successfully!")

