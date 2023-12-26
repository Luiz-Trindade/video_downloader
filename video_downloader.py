# Simple YouTube Video Downloader written in Python.
# Created By: Luiz Gabriel Magalhães Trindade.
# Distributed Under The GPL3 License.
# GPL3 License: https://www.gnu.org/licenses/gpl-3.0.en.html#license-text

from customtkinter import *
#from pytube import YouTube
#from plyer import notification
import yt_dlp
from PySimpleGUI import popup_quick_message as alert

def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("500x300")
    set_default_color_theme("green")

    def Download():
        '''try:
            video_url = video_link.get()
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()
            video.download("Downloads")
            notification.notify(
                title="Video Downloader", 
                message="vídeo baixado com sucesso!",
                timeout=5
            )
        except:
            notification.notify(
                title="Video Downloader", 
                message="Erro ao fazer o download do vídeo!",
                timeout=5
            )''' 

        try:
            video_url = video_link.get()
            options = {
                "format":"bestvideo+bestaudio/best",
                "outtmpl":"%(title)s.%(ext)s",
                "merge_output_format":"mp4"
            }
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([video_url])
            alert("Vídeo baixado com sucesso!", font=("Arial", 30, "bold"))
        except Exception as error:
            alert(f"{error}", font=("Arial", 30, "bold"))
            #print(f"{error}")

    video_link = CTkEntry(master=app, font=("Arial", 20), width=400, height=50)
    video_link.pack(pady=50, padx=50)

    download_button = CTkButton(master=app, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download)
    download_button.pack(pady=40, padx=50)

    app.mainloop()

Main()
