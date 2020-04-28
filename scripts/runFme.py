import subprocess # Used to interact with command line
"""
This is the command to run the revit converter. Still need to implement
"C:\\Program Files\\FME\\fme.exe" "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\revitNativeToCsv.fmw"
              --SourceDataset_REVITNATIVE_3 "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\sourceData\\revitData\\SampleWithDoors_Accessories.rvt"
              --FEATURE_TYPES ""
              --DestDataset_CSV2 "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData"
"""

def wrapInQuotes(str):
    return "\"{0}\"".format(str)

def runRevitConverter(fmeLocation, workspaceLocation, sourceDataset, outputDir):
    command = "{0} {1} --SourceDataset_REVITNATIVE_3 {2} --DestDataset_CSV2 {3} --FEATURE_TYPES \"\""
    command = command.format(
        wrapInQuotes(fmeLocation),
        wrapInQuotes(workspaceLocation),
        wrapInQuotes(sourceDataset),
        wrapInQuotes(outputDir)
    )

    # https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    for line in iter(process.stdout.readline, ""):
        print(line.trim())

    process.stdout.close()
    result = process.wait()
    print(result)

if __name__ == "__main__":
    runRevitConverter("C:\\Program Files\\FME\\fme.exe", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\revitNativeToCsv.fmw", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\sourceData\\revitData\\SampleWithDoors_Accessories.rvt", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData")
