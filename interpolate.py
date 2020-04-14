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
    inF = open(inputFilePath, mode="r", encoding="utf-8-sig")
    outF = open(outputFilePath, mode="w")
    containsRGB = True
    error = False
    try:
        firstLine = inF.readline().strip()
        #print(firstLine)
        containsRGB = "r" in firstLine.lower()
    except Exception as e:
        print("Error while reading file: " + str(e))

    if not error:
        # oh wait, I do need to cache lines to compute partial derivatives across multiple axes
        fLines = []
        minX = None
        minY = None
        minZ = None
        for line in inF:
            if "x" in line:
                continue # skip first line if it hasn't been read yet
            line = line.strip().replace(",", " ") # FME output doesn't contain commas, so make sure all data stays that way
            if not containsRGB:
                line = line + " 0 0 0"
            fLines.append(line)
            # next, need to split lines, and update minimums (integers)
            print(line)
        # shift everything to (0,0,0) being the lowest coordinate. Use 2D array for O(1) lookup
        # interpolate, write to output file (don't forget "x y z r g b"!)
    inF.close()
    outF.close()

if __name__ == "__main__":
    args = getCmdLineArgs()
    sfile = args.sourcefile[0]
    spath = os.path.abspath(sfile.name)
    print(spath)
    rfile = args.resultfile[0]
    rpath = os.path.abspath(rfile.name)
    print(rpath)
    interpolate(spath, rpath)
