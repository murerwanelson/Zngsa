import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
from attendance import process_attendance  # Import the updated function from attendance.py

# Get the base directory where app.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Function to save processed attendance CSV
def save_processed_csv(df):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", "File saved successfully!")

# Function to upload and process the CSV file
def upload_and_process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            # Call the updated process_attendance function
            processed_df = process_attendance(file_path)
            # Save the processed DataFrame
            save_processed_csv(processed_df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the file: {e}")

# Initialize Tkinter window
root = tk.Tk()
root.title("Attendance Processor")

# Check if running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the background image
image_path = os.path.join(base_dir, 'images', 'z1.jpg')
bg_image = Image.open(image_path)
bg_image = bg_image.resize((400, 200), Image.Resampling.LANCZOS)  # Resize the image
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas to hold the background image
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a button to upload and process the CSV
process_button = tk.Button(root, text="Process CSV", command=upload_and_process_csv, font=("Arial", 12), bg="blue", fg="white")
canvas.create_window(200, 100, window=process_button)  # Position the button at the center

# Set window geometry
root.geometry("400x200")

# Run the Tkinter event loop
root.mainloop()
