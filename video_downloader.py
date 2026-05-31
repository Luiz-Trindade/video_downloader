#!/usr/bin/env python3
# -*- coding: utf-8 -*-

gpl3_text = '''
    Simple YouTube Video Downloader Written In Python!

    Copyright (C) 2024-present  Luiz Gabriel Magalhães Trindade.

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
from tkinter import filedialog
from PIL import Image
import pygame as pg
import multiprocessing
import os
import sys

# Inicializa o mixer do pygame (apenas uma vez)
pg.mixer.init()

# ---------- Funções de download (nível do módulo) ----------
def download_single(url, output_path):
    """Baixa um único vídeo (formato mp4)"""
    try:
        options = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
            "noplaylist": True,
        }
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        return True, None
    except Exception as e:
        return False, str(e)

def download_audio_single(url, output_path):
    """Baixa apenas o áudio em MP3"""
    try:
        options = {
            "format": "bestaudio/best",
            "extractaudio": True,
            "audioformat": "mp3",
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
            "noplaylist": True,
        }
        with YoutubeDL(options) as ydl:
            ydl.download([url])
        return True, None
    except Exception as e:
        return False, str(e)

def is_playlist(url):
    """Verifica se a URL corresponde a uma playlist (YouTube)"""
    try:
        with YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('_type') == 'playlist'
    except Exception:
        return False

def get_playlist_entries(url):
    """Retorna lista de URLs dos vídeos de uma playlist"""
    with YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        if info.get('_type') == 'playlist':
            entries = info.get('entries', [])
            return [entry['url'] for entry in entries if entry]
    return []

def download_playlist_parallel(urls, output_path, mode='video'):
    """Baixa múltiplos URLs em paralelo usando multiprocessing"""
    if mode == 'video':
        download_func = download_single
    else:
        download_func = download_audio_single

    # Número de processos = número de CPUs (ou 1 se não for possível)
    num_processes = max(1, multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_processes) as pool:
        # starmap passa cada tupla (url, output_path) para download_func
        results = pool.starmap(download_func, [(url, output_path) for url in urls])

    success_count = sum(1 for success, _ in results if success)
    errors = [err for _, err in results if err]
    return success_count, len(urls), errors

# ---------- Função principal ----------
def Main():
    app = CTk()
    app.title("Video Downloader 🎥")
    app.geometry("650x550")
    set_default_color_theme("green")
    set_widget_scaling(1.2)

    # Carrega o ícone usando CTkImage (corrige warning de HighDPI)
    try:
        pil_image = Image.open("_internal/icons/icon.png")
        icon_image = CTkImage(light_image=pil_image, dark_image=pil_image, size=(64, 64))
    except Exception:
        icon_image = None

    try:
        icon_tk = PhotoImage(file="_internal/icons/icon.png")
        app.iconphoto(False, icon_tk)
    except:
        pass

    tabview = CTkTabview(master=app)
    tabview.pack(pady=30, padx=10)
    tab1 = tabview.add("Video🎥")
    tab2 = tabview.add("Audio🎵")
    tab3 = tabview.add("About")

    alert_sound_path = "_internal/sound/alert_sound.mp3"
    sound_available = os.path.exists(alert_sound_path)
    if sound_available:
        pg.mixer.music.load(alert_sound_path)

    def Alert(msg):
        if sound_available:
            pg.mixer.music.play()
        alert = CTkToplevel(master=app)
        alert.title("Notification🔔")
        alert.geometry("550x150")
        CTkLabel(master=alert, text=msg, font=("Arial", 30, "bold")).pack(pady=50, padx=10)

    def Download_Video():
        url = video_link.get().strip()
        if not url:
            Alert("Por favor, insira um link.")
            return

        output_path = filedialog.askdirectory(title="Selecione a pasta de destino")
        if not output_path:
            return

        # Verifica se é playlist
        if is_playlist(url):
            entries = get_playlist_entries(url)
            if entries:
                success, total, errors = download_playlist_parallel(entries, output_path, mode='video')
                msg = f"Playlist: {success} de {total} vídeos baixados com sucesso."
                if errors:
                    msg += f"\nErros: {', '.join(errors[:3])}"
                Alert(msg)
                return
            else:
                Alert("Não foi possível interpretar como playlist. Tentando como vídeo único...")
        # Fallback: vídeo único
        success, error = download_single(url, output_path)
        if success:
            Alert("Vídeo baixado com sucesso!")
        else:
            Alert(f"Falha ao baixar vídeo: {error}")

    def Download_Audio():
        url = audio_link.get().strip()
        if not url:
            Alert("Por favor, insira um link.")
            return

        output_path = filedialog.askdirectory(title="Selecione a pasta de destino")
        if not output_path:
            return

        if is_playlist(url):
            entries = get_playlist_entries(url)
            if entries:
                success, total, errors = download_playlist_parallel(entries, output_path, mode='audio')
                msg = f"Playlist: {success} de {total} áudios baixados."
                if errors:
                    msg += f"\nErros: {', '.join(errors[:3])}"
                Alert(msg)
                return
            else:
                Alert("Não foi possível interpretar como playlist. Tentando áudio único...")

        success, error = download_audio_single(url, output_path)
        if success:
            Alert("Áudio baixado com sucesso!")
        else:
            Alert(f"Falha ao baixar áudio: {error}")

    # Interface
    if icon_image:
        CTkLabel(master=tab1, image=icon_image, text="").pack()
    video_link = CTkEntry(master=tab1, placeholder_text="Video Link", font=("Arial", 20),
                          width=400, height=50, justify="center")
    video_link.pack(pady=20, padx=10)
    CTkButton(master=tab1, font=("Arial", 35, "bold"), text="Download ⬇️",
              hover_color="orange", command=Download_Video).pack(pady=30, padx=10)

    if icon_image:
        CTkLabel(master=tab2, image=icon_image, text="").pack()
    audio_link = CTkEntry(master=tab2, placeholder_text="Audio Link", font=("Arial", 20),
                          width=400, height=50, justify="center")
    audio_link.pack(pady=20, padx=10)
    CTkButton(master=tab2, font=("Arial", 35, "bold"), text="Download ⬇️",
              hover_color="orange", command=Download_Audio).pack(pady=30, padx=10)

    if icon_image:
        CTkLabel(master=tab3, image=icon_image, text="").pack()
    CTkLabel(master=tab3, text=gpl3_text, font=("Arial", 14, "bold"), justify="left").pack()

    app.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necessário para Windows
    Main()
