from tkinter import *
import random
import string
import pyperclip

# ---------------- Window ---------------- #
root = Tk()
root.geometry("450x450")
root.title("Password Generator")
root.resizable(False, False)

# Background color
root.configure(bg="#1E1E2E")

# ---------------- Title ---------------- #
Label(
    root,
    text="🔐 PASSWORD GENERATOR",
    font=("Arial", 18, "bold"),
    fg="white",
    bg="#1E1E2E"
).pack(pady=15)

Label(
    root,
    text="Made with Python",
    font=("Arial", 11),
    fg="#A6ADC8",
    bg="#1E1E2E"
).pack(side=BOTTOM, pady=10)

# ---------------- Password Length ---------------- #
Label(
    root,
    text="Password Length",
    font=("Arial", 12, "bold"),
    fg="white",
    bg="#1E1E2E"
).pack(pady=10)

pass_len = IntVar(value=12)

Spinbox(
    root,
    from_=8,
    to_=32,
    textvariable=pass_len,
    width=10,
    font=("Arial", 12),
    bg="white",
    fg="black"
).pack()

pass_str = StringVar()

# ---------------- Generator ---------------- #
def Generator():
    password = []

    chars = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        string.punctuation
    )

    if pass_len.get() >= 4:
        password.append(random.choice(string.ascii_uppercase))
        password.append(random.choice(string.ascii_lowercase))
        password.append(random.choice(string.digits))
        password.append(random.choice(string.punctuation))

        for _ in range(pass_len.get() - 4):
            password.append(random.choice(chars))

        random.shuffle(password)

    else:
        for _ in range(pass_len.get()):
            password.append(random.choice(chars))

    pass_str.set("".join(password))

# ---------------- Copy ---------------- #
def Copy_password():
    pyperclip.copy(pass_str.get())

# ---------------- Buttons ---------------- #
Button(
    root,
    text="Generate Password",
    command=Generator,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    activebackground="#45A049",
    activeforeground="white",
    padx=10,
    pady=5
).pack(pady=15)

Entry(
    root,
    textvariable=pass_str,
    font=("Consolas", 14),
    justify="center",
    width=30,
    bg="white",
    fg="#1E1E2E"
).pack(pady=10)

Button(
    root,
    text="Copy to Clipboard",
    command=Copy_password,
    font=("Arial", 12, "bold"),
    bg="#2196F3",
    fg="white",
    activebackground="#1976D2",
    activeforeground="white",
    padx=10,
    pady=5
).pack(pady=10)

root.mainloop()
