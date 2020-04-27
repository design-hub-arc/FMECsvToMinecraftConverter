from tkinter import *
from tkinter import ttk # "Themed widgets". Whatever that means



# Following the example at https://tkdocs.com/tutorial

def launch():
    desc = """
        This is sample text,
        I don't know how it
        will be formatted
    """

    def convert(*args):
        print(args)
        # needs to be nested to access input
        print("Input is " + input.get())
        print(importColor.get())

    root = Tk() # what does this do? Is it like a JFrame?
    root.title("Minecraft Converter")
    # Create the content pane
    #                   root is the parent
    content = ttk.Frame(root, padding="10 10 10 10")
    content.grid(column=0, row=0, sticky=(N, W, E, S)) # What does this do? Does it make the content "stick" to 0,0?
    root.columnconfigure(0, weight=1) # fill available space in the window
    root.rowconfigure(0, weight=1)

    # Add info text
    text = ttk.Label(content, text=desc)
    text.grid(column=0, row=0, sticky=N)

    # Add input to the GUI
    input = StringVar() #         using textvariable allows this to auto-update when input changes
    inputGui = ttk.Entry(content, textvariable=input)
    inputGui.grid(column=1, row=2, sticky=N)

    #
    importColor = BooleanVar()
    checkbox = ttk.Checkbutton(content, text="Color the Minecraft world", variable=importColor, onvalue=True, offvalue=False)
    checkbox.grid(column=2, row=2, sticky=N)

    # Add button
    button = ttk.Button(content, text="Convert", command=convert)
    button.grid(column=1, row=3, sticky=N)

    # Output
    output = StringVar()
    outputPane = ttk.Label(content, textvariable=output)
    outputPane.grid(column=1, row=4, sticky=N)

    inputGui.focus()
    root.bind("<Return>", convert) # Press enter to convert
    root.mainloop()

if __name__ == "__main__":
    launch()
