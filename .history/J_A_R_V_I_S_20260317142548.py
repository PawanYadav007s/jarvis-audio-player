import os
import time
from typing import Any, Optional

import yt_dlp
import vlc


# 🔥 Fix VLC path (IMPORTANT)
os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")


def get_audio_url(query: str) -> Optional[str]:
    ydl_opts: Any = {
        "format": "bestaudio",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info: Any = ydl.extract_info(f"ytsearch1:{query}", download=False)

            if info and "entries" in info:
                entries = info["entries"]
                if entries:
                    return entries[0]["url"]
    except Exception as e:
        print("Error fetching song:", e)

    return None


def play_song() -> None:
    player: Optional[vlc.MediaPlayer] = None
    instance = vlc.Instance("--aout=directsound")  # 🔥 FIX AUDIO ERROR

    while True:
        try:
            song = input("\nEnter song name (or 'exit'): ")
        except EOFError:
            print("\nExiting...")
            break

        if song.lower() == "exit":
            print("Goodbye 👋")
            if player:
                player.stop()
            break

        print(f"🔍 Searching & Playing: {song} ...")

        url = get_audio_url(song)

        if not url:
            print("❌ Song not found")
            continue

        # Stop previous song
        if player:
            player.stop()

        try:
            player = instance.media_player_new()
            media = instance.media_new(url)
            player.set_media(media)
            player.play()

            print("▶ Playing... (Press Ctrl+C to change song)")

            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            if player:
                player.stop()
            print("\n⏹ Stopped")

        except Exception as e:
            print("Playback error:", e)


if __name__ == "__main__":
    play_song()