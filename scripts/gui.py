from tkinter import Tk, N, W, E, S, filedialog, StringVar, BooleanVar, INSERT
from tkinter import ttk # "Themed widgets". Whatever that means
import tkinter
import tkinter.scrolledtext

from runFme import convertAsync


# Following the example at https://tkdocs.com/tutorial

def launch():
    desc = """
        This is sample text,
        I don't know how it
        will be formatted
    """

    def out(str):
        outputPane.insert(INSERT, str + "\n")

    def runConversion():
        # needs to be nested to access input
        print("Input is " + input.get())
        print(importColor.get())
        convertAsync(input.get(), shouldColor=importColor.get(), outputListener=out, onDone=lambda:print("done"))


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
    text.grid(column=0, row=0, columnspan=2, sticky=N)

    # Add input to the GUI
    input = StringVar()

    def openChooseFile():
        fname = filedialog.askopenfilename()
        input.set(fname)
    chooseFileButton = ttk.Button(content, text="Choose file to convert", command=openChooseFile)
    chooseFileButton.grid(column=1, row=1, sticky=N)

    #
    importColor = BooleanVar()
    checkbox = ttk.Checkbutton(content, text="Color the Minecraft world", variable=importColor, onvalue=True, offvalue=False)
    checkbox.grid(column=2, row=1, sticky=N)

    # Display selected file
    file = ttk.Label(content, textvariable=input)
    file.grid(column=1, row=2, sticky=N)

    # Add button
    button = ttk.Button(content, text="Convert", command=runConversion)
    button.grid(column=2, row=2, sticky=N)

    # Output
    outputPane = tkinter.scrolledtext.ScrolledText(content)
    outputPane.grid(column=1, row=3, columnspan=2, sticky=N)

    root.mainloop()

if __name__ == "__main__":
    launch()
