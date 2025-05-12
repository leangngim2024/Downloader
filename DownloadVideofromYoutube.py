import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import ttkbootstrap as ttk

# Function to validate the URL
def validation(url):
    if "youtu.be" in url or "youtube.com" in url:
        return url
    else:
        return None

# Function to download the video
def download_video(valid_url, download_type, location):
    if download_type == "mp3":
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': f'{location}/%(title)s.%(ext)s',
        }
    elif download_type == "mp4":
        ydl_opts = {
            'format': 'bestvideo',
            'outtmpl': f'{location}/%(title)s.%(ext)s',
        }
    else:
        messagebox.showerror("Error", "Please select either 'mp3' or 'mp4'.")
        return

    # Download using YoutubeDL
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([valid_url])
            messagebox.showinfo("Success", "Download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
def create_gui():
    # Create the main window
    root = ttk.Window(themename='sandstone')
    root.title("YouTube Downloader")
    

    # URL input
    ttk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
    url_entry = ttk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=10)

    # Radio buttons for format selection (MP3 or MP4)
    format_choice = ttk.StringVar(value="mp3")  # Default selection
    ttk.Radiobutton(root, text="MP3", variable=format_choice, value="mp3").grid(row=1, column=0, padx=10, pady=5)
    ttk.Radiobutton(root, text="MP4", variable=format_choice, value="mp4").grid(row=1, column=1, padx=10, pady=5)

    # Button to select download location
    location_label = ttk.Label(root, text="No folder selected")
    location_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def select_location():
        location = filedialog.askdirectory()
        if location:
            location_label.config(text=location)

    ttk.Button(root, text="Select Download Folder", command=select_location).grid(row=2, column=2, padx=10, pady=10)

    # Start download button
    def start_download():
        url = url_entry.get()
        valid = validation(url)
        download_type = format_choice.get()
        location = location_label.cget("text")

        if not valid:
            messagebox.showerror("Error", "Please enter a valid YouTube URL!")
        elif location == "No folder selected":
            messagebox.showerror("Error", "Please select a download folder!")
        else:
            download_video(valid, download_type, location)

    ttk.Button(root, text="Download", command=start_download).grid(row=3, column=0, columnspan=3, padx=10, pady=20)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
