import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd

# Function to process the CSV file (same as before)
def process_csv(file_path):
    df = pd.read_csv(file_path)
    columns_to_drop = ['Department', 'No.', 'Location ID', 'ID Number', 'VerifyCode', 'CardNo']
    df = df.drop(columns=columns_to_drop)
    df['Date'] = pd.to_datetime(df['Date/Time']).dt.date
    df['Time'] = pd.to_datetime(df['Date/Time']).dt.time
    df = df.drop(columns=['Date/Time'])
    time_in_out = df.groupby(['Name', 'Date'])['Time'].agg(['min', 'max'])
    time_in_out = time_in_out.rename(columns={'min': 'Time In', 'max': 'Time Out'}).reset_index()
    unique_names = df['Name'].unique()
    date_range = pd.date_range(start=df['Date'].min(), end=df['Date'].max())
    all_attendance = [{'Name': name, 'Date': date.date()} for name in unique_names for date in date_range]
    attendance_df = pd.DataFrame(all_attendance)
    attendance_df = pd.merge(attendance_df, time_in_out, on=['Name', 'Date'], how='left')
    attendance_df['Attendance'] = attendance_df['Time In'].notnull().map({True: 'Present', False: 'Absent'})
    return attendance_df

def save_processed_csv(df):
    save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if save_path:
        df.to_csv(save_path, index=False)
        messagebox.showinfo("Success", "File saved successfully!")

def upload_and_process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            processed_df = process_csv(file_path)
            save_processed_csv(processed_df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process the file: {e}")

# Initialize Tkinter
root = tk.Tk()
root.title("Attendance Processor")

# Load the background image
image_path = 'C:\\Users\\user\\Desktop\\attendance\\z1.jpg'  # Your uploaded image path
bg_image = Image.open(image_path)
bg_image = bg_image.resize((400, 200), Image.ANTIALIAS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas to hold the background image
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack(fill="both", expand=True)

# Set the image on the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a button and add it on top of the image
process_button = tk.Button(root, text="Process CSV", command=upload_and_process_csv, font=("Arial", 12), bg="blue", fg="white")

# Place the button using canvas window to allow it on top of the image
canvas.create_window(200, 100, window=process_button)  # Positioning at the center

# Run the application
root.geometry("400x200")
root.mainloop()
