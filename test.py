import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()
label = ttk.Label(text="Python rocks!")
label = tk.Label(text="Python rocks!")
button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
button.pack()
label.pack()

window.mainloop()