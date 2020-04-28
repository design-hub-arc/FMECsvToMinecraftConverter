import subprocess # Used to interact with command line
import os

DEFAULT_FME_LOCATION = "C:\\Program Files\\FME\\fme.exe"
WORKSPACE_RELATIVE_PATH = ".\\" # located in the same directory

def wrapInQuotes(str):
    return "\"{0}\"".format(str)

def runCommand(command, outputListener=print):
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
    print("Process returned {0}".format(result))

def runRevitConverter(sourceDataset, outputDir, resultFileName=None):
    if resultFileName is None:
        resultFileName = os.path.basename(sourceDataset).replace(".rvt", "_rvt")
    workspaceLocation = os.path.abspath(os.path.join(WORKSPACE_RELATIVE_PATH, "revitNativeToCsv.fmw"))
    command = "{0} {1} --SourceDataset_REVITNATIVE_3 {2} --DestDataset_CSV2 {3} --FEATURE_TYPES \"\" --resultFileName {4}"
    command = command.format(
        wrapInQuotes(DEFAULT_FME_LOCATION),
        wrapInQuotes(workspaceLocation),
        wrapInQuotes(sourceDataset),
        wrapInQuotes(outputDir),
        wrapInQuotes(resultFileName)
    )
    print("Running command " + command)
    runCommand(command)
    return os.path.join(os.path.abspath(outputDir), resultFileName + ".csv")

def runCsvConverter(sourceDataset, shouldColor=False):
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
    print("Running command " + command)
    runCommand(command)

def convert(sourceDataset, outputDir, shouldColor=False, resultFileName=None):
    extention = os.path.splitext(os.path.basename(sourceDataset))[1]
    output = None
    if extention == ".rvt":
        output = runRevitConverter(sourceDataset, outputDir, resultFileName)
    else:
        raise ValueError("Don't have a converter for file type \"{0}\"".format(extention))

    print("Wrote to {0}".format(output))

    runCsvConverter(output, shouldColor)
