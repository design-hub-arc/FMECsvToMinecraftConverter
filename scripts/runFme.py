import subprocess # Used to interact with command line

DEFAULT_FME_LOCATION = "C:\\Program Files\\FME\\fme.exe"

def wrapInQuotes(str):
    return "\"{0}\"".format(str)

def runRevitConverter(fmeLocation, workspaceLocation, sourceDataset, outputDir, resultFileName=None):
    if resultFileName is None:
        resultFileName = "ImTheResult"
        
    command = "{0} {1} --SourceDataset_REVITNATIVE_3 {2} --DestDataset_CSV2 {3} --FEATURE_TYPES \"\" --resultFileName {4}"
    command = command.format(
        wrapInQuotes(fmeLocation),
        wrapInQuotes(workspaceLocation),
        wrapInQuotes(sourceDataset),
        wrapInQuotes(outputDir),
        wrapInQuotes(resultFileName)
    )

    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    for line in iter(process.stdout.readline, ""):
        print(line.strip())

    process.stdout.close()
    result = process.wait()
    print("Process returned {0}".format(result))

if __name__ == "__main__":
    runRevitConverter(DEFAULT_FME_LOCATION, "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\revitNativeToCsv.fmw", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\sourceData\\revitData\\SampleWithDoors_Accessories.rvt", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData")
