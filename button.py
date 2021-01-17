import tkinter as tk
from tkinter import *
from tkinter import messagebox

def write_slogan():
    print("Content of Button 1")

def write_slogan2():
   print("Content of Button 2")

root = tk.Tk()
root.title('Ung dung 1')
frame = tk.Frame(root)
frame.pack()

button1 = tk.Button(frame, text="Button 1", fg="blue", command=write_slogan())
button1.pack(side=tk.LEFT)
button2 = tk.Button(frame, text="Button 2", fg="green", command=write_slogan2())
button2.pack(side=tk.LEFT)
button3 = tk.Button(frame, text="Button 3 QUIT", fg="red", command=quit)
button3.pack(side=tk.LEFT)

root.mainloop()