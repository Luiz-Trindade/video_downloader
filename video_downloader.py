gpl3_text='''
    Simple YouTube Video Downloader Written In Python!

    Copyright (C) 2024  Luiz Gabriel Magalhães Trindade.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from customtkinter import *
from yt_dlp import YoutubeDL
from tkinter import ttk, PhotoImage as PI, filedialog
import pygame as pg
pg.init()

def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("650x550")
    set_default_color_theme("green")
    set_widget_scaling(1.2)

    icon_image = PI(file="_internal/icons/icon.png")

    tabview = CTkTabview(master=app)
    tabview.pack(pady=30, padx=10)
    tab1 = tabview.add("Video🎥")
    tab2 = tabview.add("Audio🎵")
    tab3 = tabview.add("About")

    alert_sound = ("_internal/sound/alert_sound.mp3")
    pg.mixer.music.load(alert_sound)
    
    def Alert(msg):
        pg.mixer.music.play()
        Alert = CTkToplevel(master=app)
        Alert.title("Notification🔔")
        Alert.geometry("550x150")
        Alert_Message = CTkLabel(master=Alert, text=msg, font=("Arial", 30, "bold"))
        Alert_Message.pack(pady=50, padx=10)

    def Download_Video():
        video_url = video_link.get()
        output_path = filedialog.askdirectory(title="Select the destination path")
        if output_path:
            try:
                options = {
                    "format":"bestvideo[ext=mp4]+bestaudio[ext=mp4a]/best[ext=mp4]/best",
                    "outtmpl":f"{output_path}/%(title)s.%(ext)s"
                }
                with YoutubeDL(options) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                Alert("Vídeo baixado com sucesso!")
            except Exception as error:
                Alert("Vídeo não baixado!")

    def Download_Audio():
        audio_url = audio_link.get()
        output_path = filedialog.askdirectory(title="Select the destination path")
        if output_path:
            try:
                options = {
                    "format":"bestaudio/best",
                    "extractaudio":True,
                    "audioformat":"mp3",
                    "outtmpl":f"{output_path}/%(title)s.%(ext)s"
                }
                with YoutubeDL(options) as ydl:
                    info = ydl.extract_info(audio_url, download=True)
                    Alert("Audio baixado com sucesso!")
            except Exception as error:
                Alert("Audio não baixado!")

    icon1 = CTkLabel(master=tab1, image=icon_image, text=None)
    icon1.pack()

    video_link = CTkEntry(master=tab1, placeholder_text="Video Link" ,font=("Arial", 20), width=400, height=50, justify="center")
    video_link.pack(pady=20, padx=10)

    download_video_button = CTkButton(master=tab1, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download_Video)
    download_video_button.pack(pady=30, padx=10)


    icon2 = CTkLabel(master=tab2, image=icon_image, text=None)
    icon2.pack()
    
    audio_link = CTkEntry(master=tab2, placeholder_text="Audio Link" ,font=("Arial", 20), width=400, height=50, justify="center")
    audio_link.pack(pady=20, padx=10)
    
    download_audio_button = CTkButton(master=tab2, font=("Arial", 35, "bold"), text="Download ⬇️ ", hover_color="orange", command=Download_Audio)
    download_audio_button.pack(pady=30, padx=10)


    icon3 = CTkLabel(master=tab3, image=icon_image, text=None)
    icon3.pack()

    about_label = CTkLabel(master=tab3, text=gpl3_text, font=("Arial", 14, "bold"), justify="left")
    about_label.pack()

    app.mainloop()

Main()
