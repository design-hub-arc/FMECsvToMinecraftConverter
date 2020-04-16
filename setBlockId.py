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

class Block:
    def __init__(self, r, g, b, id, data):
        self.r = r
        self.g = g
        self.b = b
        self.id = id
        self.data = data

    def __str__(self):
        return "Block#{0}.{1} ({2}, {3}, {4})".format(self.id, self.data, self.r, self.g, self.b)

def extractBlockHeaders(headerArray):
    required = ["r", "g", "b", "blockID", "blockData"]
    headerToCol = {}
    for header in required:
        if header in headerArray:
            headerToCol[header] = headerArray.index(header)
        else:
            raise Exception("Header array is missing the required header '{0}', instead, it contains the headers [{1}].".format(header, ", ".join(headerArray)));
    return headerToCol

def getBlockTable():
    filePath = "./colorToBlockTable.csv" # may need to make this a cmd line arg if relative paths don't work out
    #blockTable = {}
    file = None
    try:
        file = open(filePath, "r")
        headers = file.readline().strip().split(",")
        headerCols = extractBlockHeaders(headers)
        print(headerCols)
        for line in file:
            line = line.strip().split(",") # the block table file uses proper CSV format, unlike FME
            print(line)
    except Exception as e:
        print("Failed to read " + filePath)
        print(e)

    if file is not None:
        file.close()

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
    #getCmdLineArgs()
    getBlockTable()
