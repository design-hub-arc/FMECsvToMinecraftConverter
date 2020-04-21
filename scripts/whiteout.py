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

if __name__ == "__main__":
    args = getCmdLineArgs()
    print(args)
