#!/usr/bin/env python
# coding: utf-8

# In[3]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

def get_average_color(frame):
    # Calculate average color of the frame
    average_color = np.mean(frame, axis=(0, 1))
    return average_color.astype(int)

def render_color_line(average_colors, output_path):
    # Plot the line with colors stacked vertically
    plt.figure(figsize=(15, 30))  # Making the figure taller and half as wide
    for i, color in enumerate(average_colors):
        plt.fill_betweenx([i, i+1], 0, 1, color=np.flip(color)/255, linewidth=15)  # Stacked vertically with wider lines
    plt.gca().invert_yaxis()  # Invert y-axis to stack from top to bottom
    plt.axis('off')
    
    # Save the figure as a PNG file
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.show()  # Display the figure
    plt.close()  # Close the figure to avoid displaying it

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Open a file dialog box for selecting any file
file_path = filedialog.askopenfilename(title="Select a File")

# Check if a file was selected
if not file_path:
    print("No file selected. Exiting.")
    exit()

# Extract filename from file path
file_name = os.path.splitext(os.path.basename(file_path))[0]

# Output folder path
output_folder = os.path.dirname(file_path)

# Open the video or image file
if file_path.lower().endswith(('.mp4', '.mov', '.avi')):
    is_video = True
    cap = cv2.VideoCapture(file_path)
else:
    is_video = False
    image = cv2.imread(file_path)
    if image is None:
        print("Error: Unable to read the image file.")
        exit()

average_colors = []

# Prompt user to specify the frame sampling rate
if is_video:
    frame_sampling_rate = simpledialog.askinteger("Frame Sampling Rate", "Enter the frame sampling rate (e.g., 1 for every frame, 30 for every 30th frame):", initialvalue=1)
    if frame_sampling_rate is None or frame_sampling_rate <= 0:
        print("Invalid frame sampling rate. Exiting.")
        exit()
else:
    frame_sampling_rate = 1  # Default: process every frame for images, recommended 2 - 3ish

# Loop through the video frames
if is_video:
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_sampling_rate == 0:
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get average color of the frame
            average_color = get_average_color(frame)
            average_colors.append(average_color)
        
        frame_count += 1

    # Release the video capture object
    cap.release()
else:
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get average color of the image
    average_color = get_average_color(image)
    average_colors.append(average_color)

# Output path for the PNG file
output_path = os.path.join(output_folder, f'{file_name}-colorAVG.png')

# Render the line with colors stacked vertically and save it as a PNG file
render_color_line(average_colors, output_path)

