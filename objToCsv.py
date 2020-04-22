import argparse
import os

def isPathOrFile(strPath):
    path = os.path.abspath(strPath)
    if os.path.isdir(path):
        pass # is directory, so it's accepted
    else:
        try:
            open(path, "w").close()
        except Exception as e:
            raise Exception(strPath + " is not a valid path to a file or directory")
    return path

def getCmdLineArgs():
    desc = """
        converts an OBJ file to a CSV file with the headers [x, y, z, r, g, b].

        If the result file is not specified, outputs the csv file in the same directory
        as the source file, with the same name, but with a .csv extension instead of a .obj.

        If the result file is a directory, creates a new file in that directory, named after the source file
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("sourcefile", metavar="sourcefile", type=argparse.FileType("r"), nargs=1, help="the obj file to convert")
    parser.add_argument("resultfile", metavar="resultfile", type=isPathOrFile, nargs="?", help="the csv file to write to")
    parsedArgs = parser.parse_args()

    srcPath = os.path.abspath(parsedArgs.sourcefile[0].name)
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
