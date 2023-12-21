# Simple YouTube Video Downloader written in Python.
# Created By: Luiz Gabriel Magalhães Trindade.
# Distributed Under The GPL3 License.
# GPL3 License: https://www.gnu.org/licenses/gpl-3.0.en.html#license-text

from customtkinter import *
from pytube import YouTube
from plyer import notification

def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("500x300")
    set_default_color_theme("green")

    def Download():
        try:
            video_url = video_link.get()
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()
            video.download("Downloads")
            notification.notify("Video Downloader", "vídeo baixado com sucesso!")
        except:
            notification.notify("Video Downloader", "Erro ao fazer o download do vídeo!") 

    video_link = CTkEntry(master=app, font=("Arial", 20), width=400, height=50)
    video_link.pack(pady=50, padx=50)

    download_button = CTkButton(master=app, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download)
    download_button.pack(pady=40, padx=50)

    app.mainloop()

Main()
