import subprocess # Used to interact with command line
import os
import threading

DEFAULT_FME_LOCATION = "C:\\Program Files\\FME\\fme.exe"
WORKSPACE_RELATIVE_PATH = ".\\" # located in the same directory
OUTPUT_DIRECTORY_RELATIVE_PATH = ".\\convertedData"

"""
Puts quote marks around a string.
Used to ensure console commands
don't contain extraneous spaces.
"""
def wrapInQuotes(string: str):
    if not(string.startswith('""') and string.endswith('""')):
        string = "\"{0}\"".format(string)
    return string

"""
runs the given command in the console,
writing output to the given outputListener.

outputListener should accept a single argument,
and will receive each line of output the command
produces in the console.
"""
def runCommand(command: str, outputListener=print):
    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )

    for line in iter(process.stdout.readline, ""):
        outputListener(line.strip())
    process.stdout.close()

    result = process.wait()
    outputListener("Process returned {0}".format(result))

def runRevitConverter(sourceDataset, resultFileName=None, outputListener=print):
    if resultFileName is None:
        resultFileName = os.path.basename(sourceDataset).replace(".rvt", "_rvt")
    workspaceLocation = os.path.abspath(os.path.join(WORKSPACE_RELATIVE_PATH, "revitNativeToCsv.fmw"))
    outputDir = os.path.abspath(OUTPUT_DIRECTORY_RELATIVE_PATH)
    command = "{0} {1} --SourceDataset_REVITNATIVE_3 {2} --DestDataset_CSV2 {3} --FEATURE_TYPES \"\" --resultFileName {4}"
    command = command.format(
        wrapInQuotes(DEFAULT_FME_LOCATION),
        wrapInQuotes(workspaceLocation),
        wrapInQuotes(sourceDataset),
        wrapInQuotes(outputDir),
        wrapInQuotes(resultFileName)
    )
    outputListener("Running command " + command)
    runCommand(command, outputListener)
    return os.path.join(os.path.abspath(outputDir), resultFileName + ".csv")

def runCsvConverter(sourceDataset, shouldColor=False, outputListener=print):
    workspaceLocation = os.path.abspath(os.path.join(WORKSPACE_RELATIVE_PATH, "Converter.fmw"))
    outputDir = "%HOMEDRIVE%%HOMEPATH%\\AppData\\Roaming\\.minecraft\\saves"
    command = "{0} {1} --SourceDataset_CSV2 {2} --DestDataset_MINECRAFT {3} --shouldColor {4} --FEATURE_TYPES \"\""
    command = command.format(
        wrapInQuotes(DEFAULT_FME_LOCATION),
        wrapInQuotes(workspaceLocation),
        wrapInQuotes(sourceDataset),
        wrapInQuotes(outputDir),
        wrapInQuotes("yes" if shouldColor else "no")
    )
    outputListener("Running command " + command)
    runCommand(command, outputListener)

def convert(sourceDataset, shouldColor=False, resultFileName=None, outputListener=print):
    extention = os.path.splitext(os.path.basename(sourceDataset))[1]
    output = None
    if extention == ".rvt":
        output = runRevitConverter(sourceDataset, resultFileName, outputListener)
    else:
        raise ValueError("Don't have a converter for file type \"{0}\"".format(extention))

    outputListener("Wrote to {0}".format(output))

    runCsvConverter(output, shouldColor, outputListener)

"""
Runs the conversion process on the given sourceDataset in a seperate thread.

sourceDataset should be a path to an existing file.

If shouldColor is set to true, color data from the given file will be converted to block data in the created
Minecraft world. If set to false, the resulting world will be colored white.

ResultFileName is what the program will name the intermediate csv file created from the source dataset.
This defaults to the name of the orginal file, but with the '.' in its file extention replaced with an '_'.

OutputListener is a function accepting a single string argument,
and will receive the console output from the conversion process.

OnDone should be a function, which will run after converting the file.
It should accept no arguments

This method returns the Thread running the converter.
"""
def convertAsync(sourceDataset: str, shouldColor=False, resultFileName=None, outputListener=print, onDone=None)->threading.Thread:
    def f():
        convert(sourceDataset, shouldColor, resultFileName, outputListener)
        if onDone is not None:
            onDone()
    thread = threading.Thread(target=lambda: f())
    thread.start()

    return thread
