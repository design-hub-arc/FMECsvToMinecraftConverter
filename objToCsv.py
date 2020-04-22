import argparse
import os

def getCmdLineArgs():
    desc = """
        converts an OBJ file to a CSV file with the headers [x, y, z, r, g, b]
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("sourcefile", metavar="sourcefile", type=argparse.FileType("r"), nargs=1, help="the obj file to convert")
    parser.add_argument("resultfile", metavar="resultfile", type=argparse.FileType("w"), nargs="?", help="the csv file to write to")
    parsedArgs = parser.parse_args()

    srcPath = os.path.abspath(parsedArgs.sourcefile[0].name)
    if parsedArgs.resultfile is None:
        resultPath = srcPath.replace(".obj", ".csv")
    else:
        resultPath = os.path.abspath(parsedArgs.resultfile.name)

    args = {
        "sourceFilePath" : srcPath,
        "resultFilePath" : resultPath
    }
    return args

def convert(srcPath, resultPath):
    lineCount = 0
    with open(srcPath, "r") as inf:
        with open(resultPath, "w") as outf:
            outf.write("x, y, z, r, g, b\n")
            for line in inf:
                lineCount += 1
                if lineCount % 1000 == 0:
                    print("Read " + str(lineCount) + " lines")
                if line[0] == "v":
                    split = line.strip().split(" ")
                    if len(split) >= 4:
                        x, y, z = split[1:4]
                        outf.write(str(x) + ", " + str(y) + ", " + str(z) + ", 255, 255, 255\n") # no color yet
    print("Done writing to " + resultPath)

if __name__ == "__main__":
    args = getCmdLineArgs()
    convert(args["sourceFilePath"], args["resultFilePath"])
