# app.py
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
from attendance import process_attendance  # Import the function from attendance.py

# Function to process the CSV file
def process_csv(file_path):
    try:
        return process_attendance(file_path)  # Call the imported function
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")
        return None

def save_processed_csv(df):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", "File saved successfully!")

def upload_and_process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        processed_df = process_csv(file_path)
        if processed_df is not None:
            save_processed_csv(processed_df)

# Initialize Tkinter
root = tk.Tk()
root.title("Attendance Processor")

# Load the background image (same code as before)
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, 'images', 'z1.jpg')

# Load the background image
bg_image = Image.open(image_path)
bg_image = bg_image.resize((400, 200), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas to hold the background image
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack(fill="both", expand=True)

# Set the image on the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a button and add it on top of the image
process_button = tk.Button(root, text="Process CSV", command=upload_and_process_csv, font=("Arial", 12), bg="blue", fg="white")
canvas.create_window(200, 100, window=process_button)  # Positioning at the center

# Run the application
root.geometry("400x200")
root.mainloop()
