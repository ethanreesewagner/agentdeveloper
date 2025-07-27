import tkinter as tk
from tkinter import Canvas
import random
import string
from PIL import Image, ImageDraw, ImageTk
import requests

# Function to generate random geometric image
def generate_random_image():
    width, height = 200, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw random shapes
    for _ in range(random.randint(1, 10)):
        shape_type = random.choice(['line', 'rectangle', 'ellipse', 'text'])
        if shape_type == 'line':
            draw.line([random_point(width, height), random_point(width, height)], 
                      fill=random_color(), width=random.randint(1, 3))
        elif shape_type == 'rectangle':
            draw.rectangle([random_point(width, height), random_point(width, height)], 
                           outline=random_color(), width=random.randint(1, 3))
        elif shape_type == 'ellipse':
            draw.ellipse([random_point(width, height), random_point(width, height)], 
                         outline=random_color(), width=random.randint(1, 3))
        elif shape_type == 'text':
            font_size = random.randint(10, 20)
            draw.text(random_point(width, height), random_character(), fill=random_color())

    return image

# Helper function to get a random point
def random_point(width, height):
    return random.randint(0, width), random.randint(0, height)

# Helper function to get a random color
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Helper function to get a random character
def random_character():
    return random.choice(string.ascii_letters + string.digits)

# Function to save the image to the server
def save_image_to_server(image):
    # Convert image to bytes
    image_bytes = image.tobytes()
    headers = {'Content-Type': 'application/octet-stream'}
    response = requests.post('http://localhost:5000/upload', data=image_bytes, headers=headers)
    return response.json()

# Create the main window
root = tk.Tk()
root.title("Random Image Generator")

# Create a canvas to display images
canvas = Canvas(root, width=200, height=200)
canvas.pack()

# Function to display a new image
def display_new_image():
    img = generate_random_image()
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    # Save img_tk reference to keep it displayed
    canvas.image = img_tk
    # Save the image to the server
    save_image_to_server(img)

# Button to generate a new image
button = tk.Button(root, text="Generate Image", command=display_new_image)
button.pack()

# Start the Tkinter event loop
root.mainloop()
