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
Checks to see if a string represents
a valid path on the user's computer.
This path is considered valid if it is one of three things:
(a) a directory that exists
(b) a file that exists
or (c) a file that can be created

If the path meets none of these conditions, throws an exception,
otherwise, returns the absolute version of the path
"""
def validatePath(strPath):
    path = os.path.abspath(strPath)
    if os.path.isdir(path):
        pass # is directory, so it's accepted
    elif os.path.isfile(path):
        pass # exists, so it's accepted
    else:
        # see if we can create it as a file
        try:
            open(path, "w").close()
        except Exception as e:
            raise Exception(strPath + " is not a valid path to a file or directory")
    return path

"""
Extracts arguments from the command line.
Returns a dictionary containing 2 keys:
["sourceFilePath"] : (string) the absolute path to an existing obj file.
["resultFilePath"] : (string) the absolute path to where the resulting CSV file should be written.

the sourceFilePath is required in the command line, but the resultFilePath is optional.
The resultFilePath returned is based on what the user enters for the second argument:
(a) python objToCsv.py /path/to/source/filename.obj:
    will set the resultFilePath to "/path/to/source/filename.csv".
(b) python objToCsv.py /path/to/source/filename.obj /path/to/resultfile.csv
    will set the resultFilePath to "/path/to/resultfile.csv"
(c) python objToCsv.py /path/to/source/filename.obj /path/to/directory
    will set the resultFilePath to "/path/to/directory/filename.csv"
"""
def getCmdLineArgs():
    desc = """
        converts an OBJ file to a CSV file with the headers [x, y, z, r, g, b].

        If the result file is not specified, outputs the csv file in the same directory
        as the source file, with the same name, but with a .csv extension instead of a .obj.

        If the result file is a directory, creates a new file in that directory, named after the source file
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("sourcefile", metavar="sourcefile", type=validateIsObj, nargs=1, help="the obj file to convert")
    parser.add_argument("resultfile", metavar="resultfile", type=validatePath, nargs="?", help="the csv file to write to")
    parsedArgs = parser.parse_args()

    srcPath = os.path.abspath(parsedArgs.sourcefile[0])
    if parsedArgs.resultfile is None:
        resultPath = srcPath.replace(".obj", ".csv")
    else:
        resultPath = os.path.abspath(parsedArgs.resultfile)
        if os.path.isdir(resultPath):
            fname = os.path.basename(srcPath)
            resultPath = os.path.join(resultPath, fname.replace(".obj", ".csv"))

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
