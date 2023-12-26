# Simple YouTube Video Downloader written in Python.
# Created By: Luiz Gabriel Magalhães Trindade.
# Distributed Under The GPL3 License.
# GPL3 License: https://www.gnu.org/licenses/gpl-3.0.en.html#license-text

from customtkinter import *
from pytube import YouTube
from PySimpleGUI import popup_quick_message as alert
import os

def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("500x325")
    set_default_color_theme("green")

    extension = "mp4"

    '''def SetExtension(): 
        switch_state = switch_var.get()
        if switch_state == "on": extension = "mp3"
        else: extension = "mp4"
        print(extension)'''

    def Download():
        video_url = video_link.get()
        try:
            yt = YouTube(video_url)
            title = yt.title
            #title = title.replace("#", "")
            #print(title)

            video = yt.streams.get_highest_resolution()
            video.download()

            #if extension == "mp3":
            #    os.rename(f"{title.mp4", f"{title}.mp3")
            #else: pass

            alert(f"Vídeo '{title}' com sucesso!", font=("Arial", 30, "bold"))
            
        except Exception as error:
            alert(f"{error}", font=("Arial", 30, "bold"))

    video_link = CTkEntry(master=app, font=("Arial", 20), width=400, height=50)
    video_link.pack(pady=50, padx=50)

    #switch_var = StringVar(value="off")
    #switch = CTkSwitch(master=app, text="Download as MP3 audio", command=SetExtension, variable=switch_var, onvalue="on", offvalue="off", font=("Arial", 20, "bold"))
    #switch.pack(pady=10, padx=10)

    download_button = CTkButton(master=app, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download)
    download_button.pack(pady=40, padx=50)

    app.mainloop()

Main()
