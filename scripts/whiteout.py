import argparse
import os
import re

# FME currently handles all of this, so we don't really need this file

def getCmdLineArgs():
    desc = """
        Replaces all color in a CSV [x, y, z, r, g, b] file with white
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("sourcefile", metavar="sourcefile", type=argparse.FileType("r"), nargs=1, help="the csv file to interpolate")
    parser.add_argument("resultfile", metavar="resultfile", type=argparse.FileType("w"), nargs="?", help="the csv file write output to")
    parsedArgs = parser.parse_args()

    srcPath = os.path.abspath(parsedArgs.sourcefile[0].name)
    if parsedArgs.resultfile is None:
        resultPath = srcPath.replace(".csv", "Whiteout.csv")
    else:
        resultPath = os.path.abspath(parsedArgs.resultfile[0].name)

    args = {
        "sourceFilePath" : srcPath,
        "resultFilePath" : resultPath
    }
    return args

def whiteout(srcPath, resultPath):
    with open(srcPath, "r", encoding="utf-8-sig") as source:
        with open(resultPath, "w") as result:
            for line in source:
                #         substitute commas followed by any number of spaces with one space
                line = re.sub(r",[ ]*", " ", line.strip())
                #          split on one or more spaces.
                split = re.split(r" +", line)
                if "x" != split[0].lower():
                    # not on header row, so replace r, g, b
                    for i in range(3, len(split)):
                        split[i] = "255"
                newLine = " ".join(split) + "\n"
                result.write(newLine)

if __name__ == "__main__":
    args = getCmdLineArgs()
    whiteout(args["sourceFilePath"], args["resultFilePath"])
