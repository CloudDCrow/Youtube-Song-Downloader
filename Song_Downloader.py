import os
import sys
from pytube import YouTube as yt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def main():
    create_window()


def create_window():
    window = tk.Tk()
    icon = Image.open(resource_path("Images/Icon.png"))
    window.iconphoto(True, ImageTk.PhotoImage(icon))
    window.title("Youtube To MP3 Downloader")

    # Window Sizes
    window_width = 600
    window_height = 300
    max_window_width = 1000
    max_window_height = 750
    min_window_width = 350
    min_window_height = 200

    window.geometry(str(window_width) + "x" + str(window_height))
    window.maxsize(max_window_width, max_window_height)
    window.minsize(min_window_width, min_window_height)

    # Grid configs
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=0)
    window.rowconfigure(0, weight=2)
    window.rowconfigure(1, weight=0)
    window.rowconfigure(2, weight=1)

    # Widget Styles
    style = ttk.Style()
    style.theme_use('clam')

    # Background Image and Widgets
    background_image = Image.open(resource_path("Images/Music_Background.jpg"))
    background_image = ImageTk.PhotoImage(background_image)

    background_label = tk.Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1, relx=0, rely=0)

    entry = ttk.Entry(window)
    entry.grid(row=0, column=0, columnspan=2, ipadx=100, ipady=3, sticky=tk.S)

    label = tk.Label(window, text="Insert Youtube Link")
    label.grid(row=2, column=0, columnspan=2, sticky=tk.N, pady=10)

    button = ttk.Button(window, text="Download", command=lambda: [song_downloader(entry, label),
                                                                  entry.delete(0, tk.END)])
    button.grid(row=1, column=0, columnspan=2, sticky=tk.N, pady=5)

    window.bind("<Return>", lambda event: button.invoke())
    window.mainloop()


def song_downloader(entry, label):
    url = entry.get()
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    download_folder = os.path.join(desktop, "Downloaded_Songs")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    try:
        yt_link = yt(url)
        video_stream = yt_link.streams.filter(only_audio=True).first()
        video_filename = os.path.join(download_folder, video_stream.default_filename)

        # Checks if the file already exists, otherwise it would download it again as a mp4 file
        if os.path.exists(video_filename.replace(".mp4", ".mp3")):
            raise FileExistsError("File already exists.")

        video_stream.download(download_folder)
        os.rename(video_filename, video_filename.replace(".mp4", ".mp3"))

        label.config(text="The Song Has Been Successfully Downloaded!")

    except FileExistsError:
        label.config(text="This Song Already Exists In The File")
    except Exception as e:
        if str(e) == 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*':
            label.config(text="Invalid Link")
        else:
            label.config(text="An Unexpected Error Occurred")
            print(f"An error occurred: {e}")
            raise e


# This Code is only for creating the exe file, can be ignored
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        path = getattr(sys, '_MEIPASS', os.getcwd())
    except AttributeError:
        path = os.path.abspath(".")

    return os.path.join(path, relative_path)


if __name__ == '__main__':
    main()