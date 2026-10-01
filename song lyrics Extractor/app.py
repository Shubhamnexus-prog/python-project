from tkinter import *
from tkinter import messagebox as mb
from tkinter import scrolledtext
import requests


def search_song():

    song_name = song.get().strip()
    artist_name = artist.get().strip()

    if not song_name:
        mb.showwarning(
            "Missing Song",
            "Please enter a song name."
        )
        return

    try:

        params = {
            "track_name": song_name
        }

        if artist_name:
            params["artist_name"] = artist_name

        response = requests.get(
            "https://lrclib.net/api/search",
            params=params,
            headers={
                "User-Agent": "Shubham-Song-Lyrics-Extractor/1.0"
            },
            timeout=10
        )

        response.raise_for_status()

        results = response.json()

        # Clear old results
        results_box.delete(0, END)

        if not results:
            mb.showerror(
                "Not Found",
                "No songs found. Try another song name."
            )
            return

        # Display results
        for item in results:

            title = item.get("trackName", "Unknown Song")
            artist_name_result = item.get(
                "artistName",
                "Unknown Artist"
            )

            results_box.insert(
                END,
                f"{title} - {artist_name_result}"
            )

        # Store API results globally
        global search_results
        search_results = results

    except requests.exceptions.RequestException as e:

        mb.showerror(
            "Network Error",
            f"Unable to connect to lyrics service.\n\n{e}"
        )


def get_selected_lyrics():

    selection = results_box.curselection()

    if not selection:

        mb.showwarning(
            "Select Song",
            "Please select a song from the search results."
        )

        return

    index = selection[0]

    selected_song = search_results[index]

    lyrics = selected_song.get("plainLyrics")

    title = selected_song.get(
        "trackName",
        "Unknown"
    )

    artist_name = selected_song.get(
        "artistName",
        "Unknown"
    )

    if not lyrics:

        mb.showerror(
            "Lyrics Not Available",
            "Lyrics are not available for this song."
        )

        return

    lyrics_box.delete(
        "1.0",
        END
    )

    lyrics_box.insert(
        END,
        lyrics
    )

    song_title.config(
        text=f"🎵 {title} - {artist_name}"
    )


def clear_all():

    song.delete(
        0,
        END
    )

    artist.delete(
        0,
        END
    )

    results_box.delete(
        0,
        END
    )

    lyrics_box.delete(
        "1.0",
        END
    )

    song_title.config(
        text="Lyrics will appear here"
    )


def copy_lyrics():

    lyrics = lyrics_box.get(
        "1.0",
        END
    ).strip()

    if not lyrics:

        mb.showwarning(
            "No Lyrics",
            "There are no lyrics to copy."
        )

        return

    root.clipboard_clear()
    root.clipboard_append(lyrics)

    mb.showinfo(
        "Copied",
        "Lyrics copied to clipboard!"
    )


def download_lyrics():

    lyrics = lyrics_box.get(
        "1.0",
        END
    ).strip()

    if not lyrics:

        mb.showwarning(
            "No Lyrics",
            "There are no lyrics to download."
        )

        return

    filename = song.get().strip()

    if not filename:
        filename = "lyrics"

    try:

        with open(
            f"{filename}.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(lyrics)

        mb.showinfo(
            "Downloaded",
            f"Saved as {filename}.txt"
        )

    except Exception as e:

        mb.showerror(
            "Error",
            str(e)
        )


# --------------------------------
# Main Window
# --------------------------------

root = Tk()

root.title(
    " Song Lyrics Extractor"
)

root.geometry(
    "800x700"
)

root.resizable(
    False,
    False
)

root.config(
    bg="CadetBlue"
)


# --------------------------------
# Title
# --------------------------------

Label(
    root,
    text="🎵 Song Lyrics Extractor",
    font=("Arial", 21, "bold"),
    bg="CadetBlue",
    fg="white"
).pack(pady=15)


# --------------------------------
# Song
# --------------------------------

Label(
    root,
    text="Song Name:",
    font=("Arial", 13, "bold"),
    bg="CadetBlue"
).place(
    x=70,
    y=75
)

song = Entry(
    root,
    width=45,
    font=("Arial", 12)
)

song.place(
    x=200,
    y=75
)


# --------------------------------
# Artist
# --------------------------------

Label(
    root,
    text="Artist Name:",
    font=("Arial", 13, "bold"),
    bg="CadetBlue"
).place(
    x=70,
    y=120
)

artist = Entry(
    root,
    width=45,
    font=("Arial", 12)
)

artist.place(
    x=200,
    y=120
)


# --------------------------------
# Search Button
# --------------------------------

Button(
    root,
    text="🔍 Search Songs",
    font=("Arial", 11, "bold"),
    width=17,
    command=search_song
).place(
    x=200,
    y=160
)


Button(
    root,
    text="🧹 Clear",
    font=("Arial", 11, "bold"),
    width=12,
    command=clear_all
).place(
    x=390,
    y=160
)


# --------------------------------
# Search Results
# --------------------------------

Label(
    root,
    text="Search Results:",
    font=("Arial", 13, "bold"),
    bg="CadetBlue",
    fg="white"
).place(
    x=50,
    y=210
)


results_box = Listbox(
    root,
    width=85,
    height=6,
    font=("Arial", 11)
)

results_box.place(
    x=50,
    y=240
)


Button(
    root,
    text="🎵 Get Lyrics",
    font=("Arial", 11, "bold"),
    width=17,
    command=get_selected_lyrics
).place(
    x=310,
    y=350
)


# --------------------------------
# Lyrics
# --------------------------------

song_title = Label(
    root,
    text="Lyrics will appear here",
    font=("Arial", 14, "bold"),
    bg="CadetBlue",
    fg="white"
)

song_title.place(
    x=50,
    y=400
)


lyrics_box = scrolledtext.ScrolledText(
    root,
    width=85,
    height=11,
    font=("Arial", 11),
    wrap=WORD
)

lyrics_box.place(
    x=50,
    y=430
)


# --------------------------------
# Bottom Buttons
# --------------------------------

Button(
    root,
    text="📋 Copy Lyrics",
    font=("Arial", 11, "bold"),
    width=15,
    command=copy_lyrics
).place(
    x=220,
    y=640
)


Button(
    root,
    text="📥 Download",
    font=("Arial", 11, "bold"),
    width=15,
    command=download_lyrics
).place(
    x=400,
    y=640
)


# Search results storage
search_results = []


root.mainloop()