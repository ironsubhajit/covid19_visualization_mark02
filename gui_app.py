import os
import tkinter as tk
from tkinter import ttk


from back_end.app import save_file, auto_open


# def greet(file_name):
#     myLabel = tk.Label(root, text=f'Hello, {e.get()}')
#     myLabel.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Covid19 App")
    cwd = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(cwd, 'logo_test.ico')
    root.iconbitmap(icon_path)
    root.geometry('500x250')

    # input/entry box
    e = tk.Entry(width=50)
    e.pack()
    #file_name = e.get()

    # get entry input
    #file_path = save_file(file_name)
    
    
    # greet = ttk.Button(root, text="test", command=greet)
    # greet.pack(side='right',fg='green')
    map_view = ttk.Button(root,
                          text="View Map",
                          command=lambda: auto_open(save_file(e.get())))
    map_view.pack()

    root.mainloop()
