import tkinter as tk
from tkinter import messagebox
import requests
import threading

class Sketchpad(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Sketchpad')
        self.geometry('400x400')

        self.canvas = tk.Canvas(self, bg='white', width=400, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.old_x = None
        self.old_y = None
        self.line_width = 5
        self.draw_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.auto_save_interval = 5000  # in milliseconds
        self.load_sketch()  # Load any existing sketch on start
        self.auto_save()

    def paint(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.line_width, fill=self.draw_color,
                capstyle=tk.ROUND, smooth=tk.TRUE)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x = None
        self.old_y = None

    def save_sketch(self):
        try:
            # Get the canvas content
            self.update_idletasks()
            self.canvas.postscript(file='temp_sketch.ps', colormode='color')

            # Read the postscript file and send it to the server
            with open('temp_sketch.ps', 'r') as f:
                image_data = f.read()

            response = requests.post(
                'http://127.0.0.1:5000/save_sketch',
                json={'image_data': image_data, 'image_name': 'sketch.ps'})

            if response.status_code == 200:
                print('Sketch saved successfully')
            else:
                print('Failed to save sketch')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def load_sketch(self):
        try:
            # Request the existing sketch from the server
            response = requests.get('http://127.0.0.1:5000/load_sketch')

            if response.status_code == 200:
                print('Sketch loaded successfully')
                ps_data = response.json().get('image_data', '')
                if ps_data:
                    # Load the postscript data into the canvas
                    self.canvas.delete("all")  # Clear existing drawings
                    self.canvas.create_image((0, 0), image=tk.PhotoImage(data=ps_data), anchor=tk.NW)
            else:
                print('No existing sketch to load')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def auto_save(self):
        self.save_sketch()
        self.after(self.auto_save_interval, self.auto_save)

if __name__ == '__main__':
    app = Sketchpad()
    app.mainloop()
