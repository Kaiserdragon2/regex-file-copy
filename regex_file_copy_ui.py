import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

# Function to copy directories with or without filtering files based on regex
def copy_directory_structure(src, dest, regex_pattern, invert_filtering):
    for root, dirs, files in os.walk(src):
        # Create the destination directory structure
        rel_path = os.path.relpath(root, src)
        dest_dir = os.path.join(dest, rel_path)

        # Filter files based on the regex pattern and invert filtering if needed
        filtered_files = [file for file in files if (re.match(regex_pattern, file) and not invert_filtering) or (not re.match(regex_pattern, file) and invert_filtering)]

        # Copy the files to the destination directory
        for file in filtered_files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            # Create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            shutil.copy2(src_file, dest_file)

def browse_source_directory():
    global source_dir
    source_dir = filedialog.askdirectory()
    source_dir_entry.delete(0, tk.END)
    source_dir_entry.insert(0, source_dir)

def browse_destination_directory():
    global destination_dir
    destination_dir = filedialog.askdirectory()
    destination_dir_entry.delete(0, tk.END)
    destination_dir_entry.insert(0, destination_dir)

# Function to update the explanation label text
def update_explanation():
    invert_filtering = invert_filtering_var.get()
    explanation_label.config(text=f"Filtering {'out' if invert_filtering else 'in'} files matching the pattern.")

# Create a tkinter window with a larger size and some basic styling
window = tk.Tk()
window.title("Folder Structure Copy")
window.geometry("400x400")  # Set window size

# Create a frame to contain UI elements for better organization
frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

# Source directory input
source_label = tk.Label(frame, text="Source Directory:")
source_label.grid(row=0, column=0, sticky="w")
source_dir_entry = tk.Entry(frame, width=30)
source_dir_entry.grid(row=0, column=1)
source_browse_button = tk.Button(frame, text="Browse", command=browse_source_directory)
source_browse_button.grid(row=0, column=2)

# Destination directory input
destination_label = tk.Label(frame, text="Destination Directory:")
destination_label.grid(row=1, column=0, sticky="w")
destination_dir_entry = tk.Entry(frame, width=30)
destination_dir_entry.grid(row=1, column=1)
destination_browse_button = tk.Button(frame, text="Browse", command=browse_destination_directory)
destination_browse_button.grid(row=1, column=2)

# Regex pattern input
regex_label = tk.Label(frame, text="Regex Pattern:")
regex_label.grid(row=2, column=0, sticky="w")
regex_pattern_entry = tk.Entry(frame, width=30)
regex_pattern_entry.grid(row=2, column=1)

# Checkbox to invert filtering
invert_filtering_var = tk.BooleanVar()
invert_filtering_var.set(False)
invert_filtering_checkbox = tk.Checkbutton(frame, text="Invert Filtering", variable=invert_filtering_var, command=update_explanation)
invert_filtering_checkbox.grid(row=3, column=0, columnspan=3, pady=(10, 0), sticky="w")

# Explanation label
explanation_label = tk.Label(frame, text="", fg="blue")
explanation_label.grid(row=4, column=0, columnspan=3, pady=(5, 0))

# Copy button
def start_copy():
    global source_dir, destination_dir, regex_pattern, invert_filtering
    source_dir = source_dir_entry.get()
    destination_dir = destination_dir_entry.get()
    regex_pattern = regex_pattern_entry.get()
    invert_filtering = invert_filtering_var.get()

    # Clear the result label text before copying
    result_label.config(text="")

    copy_directory_structure(source_dir, destination_dir, regex_pattern, invert_filtering)

    # Set the result label text after the copy operation
    result_label.config(text="Folder structure copied with filtering.")

copy_button = tk.Button(frame, text="Start Copy", command=start_copy)
copy_button.grid(row=5, column=0, columnspan=3, pady=(20, 0))

# Result label
result_label = tk.Label(frame, text="", fg="green")
result_label.grid(row=6, column=0, columnspan=3)

update_explanation()  # Initialize explanation label text

window.mainloop()
