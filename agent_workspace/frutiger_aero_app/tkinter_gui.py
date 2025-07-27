import tkinter as tk
from tkinter import messagebox
import requests

class FrutigerAeroApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Frutiger Aero Styled App')
        self.root.geometry('400x300')
        self.server_url = 'http://127.0.0.1:5000'

        self.label = tk.Label(root, text='Item:', font=('Helvetica', 14), bg='#d4e5f2', bd=5, relief='ridge')
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=10)

        self.create_button = tk.Button(root, text='Create', command=self.create_item, bg='#4ea1d3')
        self.create_button.pack(pady=5)

        self.read_button = tk.Button(root, text='Read', command=self.read_items, bg='#4ea1d3')
        self.read_button.pack(pady=5)

        self.update_button = tk.Button(root, text='Update', command=self.update_item, bg='#4ea1d3')
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text='Delete', command=self.delete_item, bg='#4ea1d3')
        self.delete_button.pack(pady=5)

        self.result_label = tk.Label(root, text='', font=('Helvetica', 12))
        self.result_label.pack(pady=10)

    def create_item(self):
        item = self.entry.get()
        if item:
            response = requests.post(f'{self.server_url}/create', json={'item': item})
            messagebox.showinfo('Create', response.json().get('message'))

    def read_items(self):
        response = requests.get(f'{self.server_url}/read')
        items = response.json().get('items', [])
        self.result_label.config(text='Items: ' + ', '.join(items))

    def update_item(self):
        item_id = int(self.entry.get())
        new_item = 'Updated ' + str(item_id)
        response = requests.put(f'{self.server_url}/update/{item_id}', json={'item': new_item})
        messagebox.showinfo('Update', response.json().get('message'))

    def delete_item(self):
        item_id = int(self.entry.get())
        response = requests.delete(f'{self.server_url}/delete/{item_id}')
        messagebox.showinfo('Delete', response.json().get('message'))

if __name__ == '__main__':
    root = tk.Tk()
    app = FrutigerAeroApp(root)
    root.mainloop()