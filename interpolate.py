import argparse
import os

def getCmdLineArgs():
    desc = """
        Interpolates z coordinates in a csv file.
        This takes a series of 3-D points from a CSV file,
        and converts those points to use integer coordinates.
        It then fills any holes in the resulting point cloud,
        creating a 3-D surface with exactly one point at each
        (x, y) coordinate.
    """
    parser = argparse.ArgumentParser(description=desc, usage="%(prog)s [sourcefile] [resultfile]")
    parser.add_argument("sourcefile", metavar="sourcefile", type=argparse.FileType("r"), nargs=1, help="the csv file to interpolate")
    parser.add_argument("resultfile", metavar="resultfile", type=argparse.FileType("w"), nargs=1, help="the csv file write output to")
    args = parser.parse_args()
    return args

def printFile(file):
    for line in file:
        print(line)

def interpolate(inputFilePath, outputFilePath):
    inF = open(inputFilePath, "r")
    outF = open(outputFilePath, "w")
    try:
        firstLine = inF.readline()
        print(firstLine)
    except Error as e:
        print("Error while reading file: " + str(e))
    inF.close()
    outF.close()

if __name__ == "__main__":
    args = getCmdLineArgs()
    sfile = args.sourcefile[0]
    print(os.path.abspath(sfile.name))
    rfile = args.resultfile[0]
    print(os.path.abspath(rfile.name))
