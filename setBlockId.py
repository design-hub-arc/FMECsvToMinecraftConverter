import argparse

'''
Takes an input file in CVS [x, y, z, r, g, b] format,
and outputs a new file with the the columns [blockID, blockData]
appended to the end, containing the id and data of the block in
colorToBlockTable.csv that most closely matches the r, g, b value
of that point.

FME probably has some way of doing this,
but I'd have to do some research into it.
'''

def getCmdLineArgs():
    desc = """
        Sets the blockID and blockData of each point in a point cloud.
    """
    parser = argparse.ArgumentParser(description=desc, usage="%(prog)s [sourcefile] [resultfile]")
    parser.add_argument("sourcefile", metavar="sourcefile", type=argparse.FileType("r"), nargs=1, help="the csv file to calculate block attributes for")
    parser.add_argument("resultfile", metavar="resultfile", type=argparse.FileType("w"), nargs=1, help="the csv file to write the new data to")
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    getCmdLineArgs()
