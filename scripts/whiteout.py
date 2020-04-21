import argparse
import os

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
    with open(srcPath, "r") as source:
        with open(resultPath, "w") as result:
            result.write(source.readline().replace(",", " ")) #add headers
            for line in source:
                #                            need to replace these two individually, otherwise we may get two spaces in a row
                #                            TODO: replace with regex so it splits on any number of spaces
                split = line.strip().replace(", ", " ").replace(",", " ").split(" ") # FME exports CSV with spaces instead of commas sometimes
                print(split)
                split[3] = "255"
                split[4] = "255"
                split[5] = "255"
                newLine = " ".join(split)
                result.write(newLine + "\n")

if __name__ == "__main__":
    args = getCmdLineArgs()
    print(args)
    whiteout(args["sourceFilePath"], args["resultFilePath"])
