import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For images

# Create main window
root = tk.Tk()
root.title("AUTISM CUM DYSLEXIA LEARNING COMPANION")
root.geometry("600x600")

# Load Background Image
bg_image = Image.open("bg.jpg").resize((600, 600))
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label for Background
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Function for Autism Support System
def open_autism_system():
    print("Autism Support System - To be implemented")

# Function for Dyslexia Support System
def open_dyslexia_system():
    print("Dyslexia Support System - To be implemented")

# Title Label
title_label = tk.Label(root, text="AUTISM CUM DYSLEXIA LEARNING COMPANION", 
                       font=("Arial", 16, "bold"), fg="white", bg="black", padx=10, pady=10)
title_label.pack(pady=20)

# Frame for Buttons
btn_frame = tk.Frame(root, bg="#ffffff")
btn_frame.pack(expand=True, fill="both", padx=25, pady=20)

# Autism Button
btn_autism = tk.Button(btn_frame, text="🧩 Autism Support System", 
                       font=("Arial", 14, "bold"), fg="white", bg="green", height=3, width=20, 
                       command=open_autism_system)
btn_autism.pack(fill="both", expand=True, pady=10)

# Dyslexia Button
btn_dyslexia = tk.Button(btn_frame, text="🔡 Dyslexia Support System", 
                         font=("Arial", 14, "bold"), fg="white", bg="blue", height=3, width=20, 
                         command=open_dyslexia_system)
btn_dyslexia.pack(fill="both", expand=True, pady=10)

# Run GUI
root.mainloop()
