from tkinter import *
from tkinter import ttk # "Themed widgets". Whatever that means
import tkinter
import tkinter.scrolledtext
import tkinter.filedialog

from runFme import convertAsync


# Following the example at https://tkdocs.com/tutorial

def launch():
    desc = """
        Choose a file to convert to Minecraft.
        Currently supported formats are:
        (*) RVT
        (*) OBJ (warning! Very slow!)
        (*) CSV (with columns [x, y, z, r, g, b] or [x, y, z], but you can exclude the header row if you want)
    """

    def out(str):
        outputPane.config(state=NORMAL)
        outputPane.insert(INSERT, str + "\n")
        outputPane.see(INSERT)
        outputPane.config(state=DISABLED)

    def done():
        chooseFileButton.config(state=NORMAL)
        checkbox.config(state=NORMAL)
        convertButton.config(state=NORMAL)
        out("Done converting file")

    def runConversion():
        # needs to be nested to access input
        chooseFileButton.config(state=DISABLED)
        checkbox.config(state=DISABLED)
        convertButton.config(state=DISABLED)
        convertAsync(
            input.get(),
            shouldColor=importColor.get(),
            outputListener=out,
            onDone=done
        )


    root = Tk() # what does this do? Is it like a JFrame?
    root.title("Minecraft Converter")
    # Create the content pane
    #                   root is the parent
    content = ttk.Frame(root)
    content.grid(column=0, row=0)# What does this do? Does it make the content "stick" to 0,0?
    root.columnconfigure(0, weight=1) # fill available space in the window
    root.rowconfigure(0, weight=1)

    # Add info text
    descLabel = ttk.Label(content, text=desc)
    descLabel.grid(column=0, row=0, columnspan=2)

    # Add input to the GUI
    input = StringVar()
    def openChooseFile():
        fname = tkinter.filedialog.askopenfilename()
        input.set(fname)
    chooseFileButton = ttk.Button(content, text="Choose file to convert", command=openChooseFile)
    chooseFileButton.grid(column=1, row=1)

    importColor = BooleanVar()
    checkbox = ttk.Checkbutton(content, text="Color the Minecraft world", variable=importColor, onvalue=True, offvalue=False)
    checkbox.grid(column=2, row=1)

    # Display selected file
    file = ttk.Label(content, textvariable=input)
    file.grid(column=1, row=2)

    # Add button
    convertButton = ttk.Button(content, text="Convert", command=runConversion)
    convertButton.grid(column=2, row=2)

    # Output
    outputPane = tkinter.scrolledtext.ScrolledText(content)
    outputPane.grid(column=1, row=3, columnspan=2)
    outputPane.config(state=DISABLED)

    root.mainloop()

if __name__ == "__main__":
    launch()
