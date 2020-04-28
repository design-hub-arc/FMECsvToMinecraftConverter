import subprocess # Used to interact with command line
"""
This is the command to run the revit converter. Still need to implement
"C:\\Program Files\\FME\\fme.exe" "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\revitNativeToCsv.fmw"
              --SourceDataset_REVITNATIVE_3 "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\sourceData\\revitData\\SampleWithDoors_Accessories.rvt"
              --FEATURE_TYPES ""
              --DestDataset_CSV2 "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData"
"""

def runRevitConverter(fmeLocation, workspaceLocation, sourceDataset, outputDir):
    """
    result = subprocess.run(
        '"{0}"'.format(fmeLocation),
        '"{0}"'.format(workspaceLocation),
        "--SourceDataset_REVITNATIVE_3",
        '"{0}"'.format(sourceDataset),
        "--DestDataset_CSV2",
        '"{0}"'.format(outputDir),
        "--FEATURE_TYPES",
        "",
        capture_output=True,
        shell=True
    )"""
    result = subprocess.run("echo {0}".format(fmeLocation), capture_output=True, shell=True)
    print(result)

if __name__ == "__main__":
    runRevitConverter("C:\\Program Files\\FME\\fme.exe", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\revitNativeToCsv.fmw", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\sourceData\\revitData\\SampleWithDoors_Accessories.rvt", "C:\\Users\\Matt\\Documents\\FME Projects\\Converter\\convertedData")
