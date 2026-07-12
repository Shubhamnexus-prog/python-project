import qrcode
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- Window ---------------- #
root = Tk()
root.title("QR Code Generator")
root.geometry("500x600")
root.configure(bg="#1E293B")
root.resizable(False, False)

# ---------------- Generate Function ---------------- #
def generate_qr():
    data = text_entry.get()

    if data == "":
        messagebox.showerror("Error", "Please enter text or URL!")
        return

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("QRCode.png")

    img = img.resize((250, 250))
    photo = ImageTk.PhotoImage(img)

    qr_label.config(image=photo)
    qr_label.image = photo

    messagebox.showinfo("Success", "QR Code Saved as QRCode.png")

# ---------------- Heading ---------------- #
Label(
    root,
    text="QR CODE GENERATOR",
    font=("Arial", 20, "bold"),
    bg="#1E293B",
    fg="white"
).pack(pady=20)

# ---------------- Entry ---------------- #
Label(
    root,
    text="Enter Text or URL",
    font=("Arial", 12),
    bg="#1E293B",
    fg="white"
).pack()

text_entry = Entry(
    root,
    width=40,
    font=("Arial", 13)
)

text_entry.pack(pady=10)

# ---------------- Button ---------------- #
Button(
    root,
    text="Generate QR Code",
    command=generate_qr,
    bg="#22C55E",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
).pack(pady=10)

# ---------------- QR Display ---------------- #
qr_label = Label(root, bg="#1E293B")
qr_label.pack(pady=20)

# ---------------- Footer ---------------- #
Label(
    root,
    text="Made with Python ❤️",
    bg="#1E293B",
    fg="#94A3B8",
    font=("Arial", 10)
).pack(side=BOTTOM, pady=10)

root.mainloop()