import argparse
import os

"""
objToCsv.py is used to extract coordinated data from an OBJ file,
and output a CSV file containing the headers [x, y, z, r, g, b].

Currently, this does not extract color information from the OBJ file,
instead, it count the r, g, b values of every point it extracts as being
white (255, 255, 255).
Future versions will need to reference an MTL file to extract color,
but as for now, we are not interested in including color.
"""


"""
Verifies that the given path
leads to an existing OBJ file.
"""
def validateIsObj(strPath):
    strPath = os.path.abspath(strPath)
    if os.path.isdir(strPath):
        raise Exception("Input must be a file, not a directory")
    if not os.path.isfile(strPath):
        raise Exception("Input must be an existing file")
    if strPath.split(".")[-1] != "obj":
        raise Exception("Input file must be in .obj format")
    return strPath

"""
Verifies that the given path
leads to an existing directory.
"""
def validateIsDir(strPath):
    strPath = os.path.abspath(strPath)
    if not os.path.isdir(strPath):
        raise Exception("Input must be a directory")
    return strPath

"""
Extracts arguments from the command line.
Returns a dictionary containing 2 keys:
["sourceFilePath"] : (string) the absolute path to an existing obj file.
["resultFilePath"] : (string) the absolute path to the directory where the resulting CSV file should be written.

the sourceFilePath is required in the command line, but the resultFilePath is optional.
The resultFilePath returned is based on what the user enters for the second argument:
(a) python objToCsv.py /path/to/source/filename.obj:
    will set the resultFilePath to "./filename.csv".
(b) python objToCsv.py /path/to/source/filename.obj /path/to/directory
    will set the resultFilePath to "/path/to/directory/filename.csv"
"""
def getCmdLineArgs():
    desc = """
        converts an OBJ file to a CSV file with the headers [x, y, z, r, g, b].

        If the result file is not specified, outputs the csv file in the directory
        this script is run from, with the same name as the source file, but with a "_obj.csv" appended to the end instead of ".obj".

        If the result file is a directory, creates a new file in that directory, named after the source file
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("sourcefile", metavar="sourcefile", type=validateIsObj, nargs=1, help="the obj file to convert")
    parser.add_argument("resultdir", metavar="resultdir", type=validateIsDir, nargs="?", help="the directory to write the resulting csv file to")
    parsedArgs = parser.parse_args()

    srcPath = os.path.abspath(parsedArgs.sourcefile[0])
    csvFileName = os.path.basename(srcPath).replace(".obj", "_obj.csv")
    if parsedArgs.resultdir is None:
        resultPath = os.path.abspath(csvFileName)
        print(resultPath)
    else:
        resultPath = os.path.join(os.path.abspath(parsedArgs.resultdir), csvFileName)

    args = {
        "sourceFilePath" : srcPath,
        "resultFilePath" : resultPath
    }
    return args

"""
Converts the contents of the file at srcPath
to a csv file at resultPath.

Currently, this just extracts vertices from the OBJ file.
Future versions may add support for color.
"""
def convert(srcPath, resultPath):
    lineCount = 0
    with open(srcPath, "r") as inf:
        with open(resultPath, "w") as outf:
            outf.write("x,y,z,r,g,b\n") # FME can't handle ', ' between each header (...)
            for line in inf:
                lineCount += 1
                if lineCount % 1000 == 0:
                    print("Read " + str(lineCount) + " lines")
                if line[0] == "v":
                    split = line.strip().split(" ")
                    if len(split) >= 4:
                        x, y, z = split[1:4]
                        outf.write(str(x) + "," + str(y) + "," + str(z) + ",255,255,255\n") # no color yet
    print("Done writing to " + resultPath)

if __name__ == "__main__":
    args = getCmdLineArgs()
    convert(args["sourceFilePath"], args["resultFilePath"])
