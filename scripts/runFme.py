import subprocess # Used to interact with command line
import os
import threading
from config import FME_PATH, WORKSPACE_RELATIVE_PATH, OUTPUT_DIRECTORY_RELATIVE_PATH, MC_SAVE_DIR


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
    outputListener("Running command " + command)
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

"""
Runs the FME workspace with the given name located in the WORKSPACE_RELATIVE_PATH directory,
passing fmeArgs to the command line.
Output from the command will be passed to outputListener.
"""
def runFme(workspaceName: str, fmeArgs: dict, outputListener=print):
    workspacePath = os.path.abspath(os.path.join(WORKSPACE_RELATIVE_PATH, workspaceName))
    outputDir = os.path.abspath(OUTPUT_DIRECTORY_RELATIVE_PATH)
    command = "{0} {1}".format(wrapInQuotes(FME_PATH), wrapInQuotes(workspacePath))
    fmeArgs["FEATURE_TYPES"] = ""
    for k, v in fmeArgs.items():
        command = command + " --" + k + " " + wrapInQuotes(v)
    runCommand(command, outputListener)

"""
Runs the given sourceDataset through revitNativeToCsv.fmw.

sourceDataset should be the path to a .rvt file.

resultFileName is what to name the csv file produced by fme,
defaulting to the original file name, but with the '.' before its extension replaced with an '_'.
outputListener should accept a single argument,
and will receive each line of output the command
produces in the console.

returns the path to the file produced by fme.
"""
def runRevitConverter(sourceDataset: str, resultFileName=None, outputListener=print)->str:
    if resultFileName is None:
        resultFileName = os.path.basename(sourceDataset).replace(".rvt", "_rvt")
    outputDir = os.path.abspath(OUTPUT_DIRECTORY_RELATIVE_PATH)
    runFme("revitNativeToCsv.fmw", {
        "SourceDataset_REVITNATIVE_3": sourceDataset,
        "DestDataset_CSV2": outputDir,
        "resultFileName": resultFileName
    }, outputListener)
    return os.path.join(os.path.abspath(outputDir), resultFileName + ".csv")


"""
Runs the given sourceDataset through objToCsv.fmw.

sourceDataset should be the path to a .obj file.

resultFileName is what to name the csv file produced by fme,
defaulting to the original file name, but with the '.' before its extension replaced with an '_'.
outputListener should accept a single argument,
and will receive each line of output the command
produces in the console.

returns the path to the file produced by fme.
"""
def runObjConverter(sourceDataset: str, resultFileName=None, outputListener=print)->str:
    if resultFileName is None:
        resultFileName = os.path.basename(sourceDataset).replace(".obj", "_obj")
    outputDir = os.path.abspath(OUTPUT_DIRECTORY_RELATIVE_PATH)
    runFme("objToCsv.fmw", {
        "SourceDataset_OBJ" : sourceDataset,
        "DestDataset_CSV2" : outputDir,
        "resultFileName" : resultFileName
    }, outputListener)
    return os.path.join(os.path.abspath(outputDir), resultFileName + ".csv")

def runXyzConverter(sourceDataset: str, resultFileName=None, outputListener=print)->str:
    if resultFileName is None:
        resultFileName = os.path.basename(sourceDataset).replace(".xyz", "_xyz")
    outputDir = os.path.abspath(OUTPUT_DIRECTORY_RELATIVE_PATH)
    runFme("xyzToCsv.fmw", {
        "SourceDataset_POINTCLOUDXYZ" : sourceDataset,
        "DestDataset_CSV2" : outputDir,
        "resultFileName" : resultFileName
    }, outputListener)
    return os.path.join(os.path.abspath(outputDir), resultFileName + ".csv")


"""
Runs the given sourceDataset through Converter.fmw.

sourceDataset should be the path to the csv file to convert.
If shouldColor is set to true, color data from the given file will be converted to block data in the created
Minecraft world. If set to false, the resulting world will be colored white.
OutputListener is a function accepting a single string argument,
and will receive the console output from the conversion process.
"""
def runCsvConverter(sourceDataset, shouldColor=False, outputListener=print):
    runFme("Converter.fmw", {
        "SourceDataset_CSV2" : sourceDataset,
        "DestDataset_MINECRAFT" : MC_SAVE_DIR,
        "shouldColor" : "yes" if shouldColor else "no"
    }, outputListener)

"""
Converts the given file to Minecraft, running all the necessary conversions.

If shouldColor is set to true, color data from the given file will be converted to block data in the created
Minecraft world. If set to false, the resulting world will be colored white.

ResultFileName is what the program will name the intermediate csv file created from the source dataset.
This defaults to the name of the orginal file, but with the '.' in its file extention replaced with an '_'.

OutputListener is a function accepting a single string argument,
and will receive the console output from the conversion process.
"""
def convert(sourceDataset, shouldColor=False, resultFileName=None, outputListener=print):
    ext = os.path.splitext(os.path.basename(sourceDataset))[1]
    output = None
    if ext == ".rvt":
        output = runRevitConverter(sourceDataset, resultFileName, outputListener)
    elif ext == ".obj":
        output = runObjConverter(sourceDataset, resultFileName, outputListener)
    else:
        raise ValueError("Don't have a converter for file type \"{0}\"".format(ext))

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
