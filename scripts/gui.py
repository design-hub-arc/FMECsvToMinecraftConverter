from tkinter import *
from tkinter import ttk # "Themed widgets". Whatever that means

# Following the example at https://tkdocs.com/tutorial

def launch():
    desc = """
        This is sample text,
        I don't know how it
        will be formatted
    """
    root = Tk() # what does this do? Is it like a JFrame?
    root.title("Minecraft Converter")
    # Create the content pane
    content = ttk.Frame(root, padding="1 1 1 1") # not sure what padding does
    content.grid(column=0, row=0, sticky=(N, W, E, S)) # What does this do? Does it make the content "stick" to 0,0?
    root.columnconfigure(0, weight=1) # fill available space in the window
    root.rowconfigure(0, weight=1)

    # Add info text
    text = ttk.Label(content, text=desc).grid(column=1, row=1, sticky=(N, W))

    # Add input to the GUI
    input = StringVar()
    inputGui = ttk.Entry(content, width=5, textvariable=input)
    inputGui.grid(column=1, row=2, sticky=(N, W))

    # Add button
    button = ttk.Button(content, text="Convert")
    button.grid(column=1, row=3, sticky=(N, W))

    root.mainloop()

if __name__ == "__main__":
    launch()
