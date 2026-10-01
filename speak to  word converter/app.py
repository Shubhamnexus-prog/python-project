import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import pyttsx3
import nltk
from nltk.corpus import wordnet


try:
    wordnet.synsets("computer")
except LookupError:
    nltk.download("wordnet")

# Text-to-Speech

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 160)


def speak(text):
    """Speak the given text."""

    if not text.strip():
        return

    engine.say(text)
    engine.runAndWait()


# Search Word

def search_word(event=None):

    word = word_entry.get().strip()

    if not word:
        messagebox.showwarning(
            "Enter Word",
            "Please enter a word."
        )
        return

    result_box.delete("1.0", tk.END)

    synsets = wordnet.synsets(word)

    if not synsets:
        result_box.insert(
            tk.END,
            f"❌ Meaning not found for: {word}\n\n"
            "Please check the spelling and try again."
        )

        speak("Meaning not found")
        return

   
    # Title

    result_box.insert(
        tk.END,
        f"📖 WORD: {word.upper()}\n"
    )

    result_box.insert(
        tk.END,
        "=" * 60 + "\n\n"
    )

    # Meanings

    result_box.insert(
        tk.END,
        "📚 MEANINGS\n\n"
    )

    definitions = []

    for index, syn in enumerate(synsets, start=1):

        definition = syn.definition()
        definitions.append(definition)

        result_box.insert(
            tk.END,
            f"{index}. {definition}\n"
        )

    
    # Synonyms

    synonyms = set()

    for syn in synsets:
        for lemma in syn.lemmas():
            synonyms.add(
                lemma.name().replace("_", " ")
            )

    synonyms.discard(word.lower())

    result_box.insert(
        tk.END,
        "\n\n"
        "🔤 SYNONYMS\n\n"
    )

    if synonyms:

        result_box.insert(
            tk.END,
            ", ".join(sorted(synonyms))
        )

    else:

        result_box.insert(
            tk.END,
            "No synonyms found."
        )

    
    # Speak first meaning

    speak_text = (
        f"The meaning of {word} is "
        f"{definitions[0]}"
    )

    speak(speak_text)



# Speak Result

def speak_result():

    content = result_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        messagebox.showwarning(
            "No Result",
            "Please search for a word first."
        )
        return

    speak(content)



# Copy Result

def copy_result():

    content = result_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        messagebox.showwarning(
            "No Result",
            "There is nothing to copy."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(content)
    root.update()

    messagebox.showinfo(
        "Copied",
        "Dictionary result copied successfully."
    )


# Save Result

def save_result():

    content = result_box.get(
        "1.0",
        tk.END
    ).strip()

    if not content:

        messagebox.showwarning(
            "No Result",
            "Please search for a word first."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ],
        title="Save Dictionary Result"
    )

    if file_path:

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        messagebox.showinfo(
            "Saved",
            "Dictionary result saved successfully."
        )



# Clear

def clear_all():

    word_entry.delete(
        0,
        tk.END
    )

    result_box.delete(
        "1.0",
        tk.END
    )

    word_entry.focus()



# Main Window

root = tk.Tk()

root.title(
    "Voice Dictionary"
)

root.geometry(
    "850x650"
)

root.resizable(
    False,
    False
)

root.configure(
    bg="SlateGray1"
)



# Header

title = tk.Label(
    root,
    text="📖 Voice Dictionary",
    font=("Arial", 24, "bold"),
    bg="SlateGray1",
    fg="gray20"
)

title.pack(
    pady=(20, 5)
)


subtitle = tk.Label(
    root,
    text="Search a word and get its meaning, synonyms and voice pronunciation",
    font=("Arial", 11),
    bg="SlateGray1",
    fg="gray30"
)

subtitle.pack(
    pady=(0, 20)
)


# Search Frame

search_frame = tk.Frame(
    root,
    bg="SlateGray1"
)

search_frame.pack()


word_label = tk.Label(
    search_frame,
    text="Enter Word:",
    font=("Arial", 13, "bold"),
    bg="SlateGray1"
)

word_label.grid(
    row=0,
    column=0,
    padx=10
)


word_entry = tk.Entry(
    search_frame,
    width=40,
    font=("Arial", 14)
)

word_entry.grid(
    row=0,
    column=1,
    padx=10
)


search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Arial", 11, "bold"),
    width=12,
    command=search_word
)

search_button.grid(
    row=0,
    column=2,
    padx=5
)


clear_button = tk.Button(
    search_frame,
    text="🧹 Clear",
    font=("Arial", 11, "bold"),
    width=10,
    command=clear_all
)

clear_button.grid(
    row=0,
    column=3,
    padx=5
)


# Result Label


result_label = tk.Label(
    root,
    text="Dictionary Result",
    font=("Arial", 15, "bold"),
    bg="SlateGray1",
    fg="gray20"
)

result_label.pack(
    anchor="w",
    padx=45,
    pady=(25, 5)
)



# Result Box

result_box = ScrolledText(
    root,
    width=88,
    height=20,
    font=("Consolas", 11),
    wrap=tk.WORD
)

result_box.pack(
    padx=40
)



# Buttons

button_frame = tk.Frame(
    root,
    bg="SlateGray1"
)

button_frame.pack(
    pady=15
)


speak_button = tk.Button(
    button_frame,
    text="🔊 Speak",
    font=("Arial", 11, "bold"),
    width=13,
    command=speak_result
)

speak_button.grid(
    row=0,
    column=0,
    padx=5
)


copy_button = tk.Button(
    button_frame,
    text="📋 Copy",
    font=("Arial", 11, "bold"),
    width=13,
    command=copy_result
)

copy_button.grid(
    row=0,
    column=1,
    padx=5
)


save_button = tk.Button(
    button_frame,
    text="💾 Save",
    font=("Arial", 11, "bold"),
    width=13,
    command=save_result
)

save_button.grid(
    row=0,
    column=2,
    padx=5
)


clear_result_button = tk.Button(
    button_frame,
    text="🧹 Clear",
    font=("Arial", 11, "bold"),
    width=13,
    command=clear_all
)

clear_result_button.grid(
    row=0,
    column=3,
    padx=5
)


# Enter Key

word_entry.bind(
    "<Return>",
    search_word
)


# Focus input box
word_entry.focus()



# Run Application

root.mainloop()