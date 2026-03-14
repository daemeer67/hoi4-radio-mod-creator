from tkinter import *
from utils import *
from create_menu import *

def main():
    root = Tk()
    root.title("Hoi4 Radio Creator")
    root.geometry("1200x700")
    
    music_list = []
    
    create_menu(root, music_list)


if __name__ == "__main__":
    main()