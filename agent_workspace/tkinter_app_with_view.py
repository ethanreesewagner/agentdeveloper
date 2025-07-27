import tkinter as tk
from tkinter import Canvas, Listbox, Scrollbar, END
import random
import string
from PIL import Image, ImageDraw, ImageTk
import requests
from io import BytesIO

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
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    headers = {'Content-Type': 'application/octet-stream'}
    try:
        response = requests.post('http://127.0.0.1:5000/upload', data=img_bytes.getvalue(), headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error uploading image: {e}")

# Function to load image list from server
def load_images_from_server():
    try:
        response = requests.get('http://127.0.0.1:5000/images')
        image_list = response.json().get('images', [])
        return image_list
    except Exception as e:
        print(f"Error retrieving images: {e}")
        return []

# Function to view image from server
def view_image(image_name):
    try:
        image_url = f'http://127.0.0.1:5000/images/{image_name}'
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        img_tk = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        # Save img_tk reference to keep it displayed
        canvas.image = img_tk
    except Exception as e:
        print(f"Error viewing image: {e}")

# Create the main window
root = tk.Tk()
root.title("Random Image Generator and Viewer")

# Create a canvas to display images
canvas = Canvas(root, width=200, height=200)
canvas.grid(row=0, column=0, rowspan=2)

# Create a listbox to display image list
listbox = Listbox(root, width=50)
listbox.grid(row=0, column=1, sticky='ns')

scrollbar = Scrollbar(root)
scrollbar.grid(row=0, column=2, sticky='ns')
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

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
button_generate = tk.Button(root, text="Generate Image", command=display_new_image)
button_generate.grid(row=1, column=1)

# Function to load images from server and display in listbox
def refresh_image_list():
    listbox.delete(0, END)  # Clear the listbox
    images = load_images_from_server()
    for image_name in images:
        listbox.insert(END, image_name)

# Button to refresh image list from server
button_refresh = tk.Button(root, text="Refresh Image List", command=refresh_image_list)
button_refresh.grid(row=2, column=1)

# Bind the listbox selection to display the selected image
def on_image_select(event):
    if listbox.curselection():
        selected_index = listbox.curselection()[0]
        image_name = listbox.get(selected_index)
        view_image(image_name)

listbox.bind('<<ListboxSelect>>', on_image_select)

# Start by refreshing the image list
refresh_image_list()

# Start the Tkinter event loop
root.mainloop()
