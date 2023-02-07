import os
from pytube import YouTube as yt
import tkinter as tk
from tkinter import ttk


def main():
    window = tk.Tk()
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
    window.rowconfigure(0, weight=2)
    window.rowconfigure(1, weight=1)

    # Widget Styles
    style = ttk.Style()
    style.theme_use('clam')

    # Background Image and Widgets
    background_image = tk.PhotoImage(file="Music_Background.jpg")

    background_label = tk.Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1, relx=0, rely=0)

    entry = ttk.Entry(window)
    entry.grid(row=0, column=0, columnspan=2, ipadx=100, ipady=3, sticky=tk.S)

    button = ttk.Button(window, text="Download", command=lambda: [song_downloader(entry), entry.delete(0, tk.END)])
    button.grid(row=1, column=0, columnspan=2, sticky=tk.N, pady=5)

    window.mainloop()


def song_downloader(entry):
    url = entry.get()
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    download_folder = os.path.join(desktop, "Downloaded_Songs")

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    try:
        yt_link = yt(url)

        video_stream = yt_link.streams.filter(only_audio=True).first()
        video_filename = os.path.join(download_folder, video_stream.default_filename)
        video_stream.download(download_folder)

        os.rename(video_filename, video_filename.replace(".mp4", ".mp3"))

        print("The song has been successfully downloaded!")

    except FileExistsError:
        print("Cannot create file, because the same file already exists!")
    except Exception as e:
        if str(e) == 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*':
            print("Sorry, that is an incorrect link")
        else:
            print("Something went wrong!")
            print(f"An error occurred: {e}")
            raise e


if __name__ == '__main__':
    main()
