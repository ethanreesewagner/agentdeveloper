import tkinter as tk

class Sketchpad:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Sketchpad")
        self.canvas = tk.Canvas(root, bg="white", width=600, height=400)
        self.canvas.pack()

        self.setup_bindings()

    def setup_bindings(self):
        self.canvas.bind("<B1-Motion>", self.paint)

    def paint(self, event):
        x = event.x
        y = event.y
        r = 3  # radius of the brush
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = Sketchpad(root)
    root.mainloop()