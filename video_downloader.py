# Simple YouTube Video Downloader written in Python.
# Created By: Luiz Gabriel Magalhães Trindade.
# Distributed Under The GPL3 License.
# GPL3 License: https://www.gnu.org/licenses/gpl-3.0.en.html#license-text

from customtkinter import *
from PySimpleGUI import popup_quick_message as alert
from yt_dlp import YoutubeDL
from tkinter import ttk, PhotoImage as PI

def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("600x400")
    set_default_color_theme("green")
    set_widget_scaling(1.2)

    tabview = CTkTabview(master=app)
    tabview.pack(pady=10, padx=10)
    tab1 = tabview.add("Download")
    tab2 = tabview.add("About")

    icon_image = PI(file="icon.png")

    def Download():
        video_url = video_link.get()
        try:
            options = {
                "format":"bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best[ext=mp4]/best"
            }
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(video_url, download=True)
            alert(f"Vídeo baixado com sucesso!", font=("Arial", 30, "bold"))
            
        except Exception as error:
            alert(f"{error}", font=("Arial", 30, "bold"))

    icon1 = CTkLabel(master=tab1, image=icon_image, text=None)
    icon1.pack()

    video_link = CTkEntry(master=tab1, placeholder_text="Video Link" ,font=("Arial", 20), width=400, height=50, justify="center")
    video_link.pack(pady=20, padx=10)

    download_button = CTkButton(master=tab1, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download)
    download_button.pack(pady=30, padx=10)

    icon2 = CTkLabel(master=tab2, image=icon_image, text=None)
    icon2.pack()

    about_text = """
    -'Video Downloader' is a program that is
    written in the python programing language.
    -That program was designed to be simple and 
    functional.

    -Copy and Paste the link and Download the Video!

    -Created By: Luiz Gabriel Magalhães Trindade. 
    (Computer Science Student)
    -Distributed Under The GPL3 License.
    """
    about_label = CTkLabel(master=tab2, text=about_text, font=("Arial", 16.5, "bold"), justify="left")
    about_label.pack()

    app.mainloop()

Main()
