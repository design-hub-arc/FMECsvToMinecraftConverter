from tkinter import Tk, N, W, E, S, filedialog, StringVar, BooleanVar
from tkinter import ttk # "Themed widgets". Whatever that means
import tkinter
import threading
from runFme import convert


# Following the example at https://tkdocs.com/tutorial

def launch():
    desc = """
        This is sample text,
        I don't know how it
        will be formatted
    """

    def runConversion():
        # needs to be nested to access input
        print("Input is " + input.get())
        print(importColor.get())
        threading.Thread(target= lambda: convert(input.get(), "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData", shouldColor=importColor.get())).start()


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
    input = StringVar()

    def openChooseFile():
        fname = filedialog.askopenfilename()
        input.set(fname)
    chooseFileButton = ttk.Button(content, text="Choose file to convert", command=openChooseFile)
    chooseFileButton.grid(column=1, row=2, sticky=N)

    #
    importColor = BooleanVar()
    checkbox = ttk.Checkbutton(content, text="Color the Minecraft world", variable=importColor, onvalue=True, offvalue=False)
    checkbox.grid(column=2, row=2, sticky=N)

    # Display selected file
    file = ttk.Label(content, textvariable=input)
    file.grid(column=1, row=3, sticky=N)

    # Add button
    button = ttk.Button(content, text="Convert", command=runConversion)
    button.grid(column=2, row=3, sticky=N)

    # Output
    output = StringVar()
    outputPane = ttk.Label(content, textvariable=output)
    outputPane.grid(column=1, row=4, sticky=N)

    root.mainloop()

if __name__ == "__main__":
    launch()
