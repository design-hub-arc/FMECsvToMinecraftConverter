import math

'''
This file is used by FME to find which
blockID and blockData to assign to each
point in a point cloud, based on their
RGB values.
'''

# change this line if you move the colorToBlockTable.csv file
BLOCK_TABLE_PATH = "./colorToBlockTable.csv"

class Block:
    def __init__(self, r, g, b, id, data):
        self.r = r
        self.g = g
        self.b = b
        self.id = id
        self.data = data

    def __str__(self):
        return "Block #{0}/{1} ({2}, {3}, {4})".format(self.id, self.data, self.r, self.g, self.b)

def extractBlockHeaders(headerArray):
    required = ["r", "g", "b", "blockID", "blockData"]
    headerToCol = {}
    for header in required:
        if header in headerArray:
            headerToCol[header] = headerArray.index(header)
        else:
            raise Exception("Header array is missing the required header '{0}', instead, it contains the headers [{1}].".format(header, ", ".join(headerArray)));
    return headerToCol

def getBlockList():
    filePath = BLOCK_TABLE_PATH
    blockList = []
    file = None
    try:
        file = open(filePath, "r")
        headers = file.readline().strip().split(",")
        headerCols = extractBlockHeaders(headers)
        for line in file:
            line = line.strip().split(",") # the block table file uses proper CSV format, unlike FME
            blockList.append(Block(
                int(line[headerCols["r"]]),
                int(line[headerCols["g"]]),
                int(line[headerCols["b"]]),
                int(line[headerCols["blockID"]]),
                int(line[headerCols["blockData"]])
            ))
    except Exception as e:
        print("Failed to read " + filePath)
        print(e)

    if file is not None:
        file.close()

    return blockList

class Cache:
    def __init__(self):
        self.blockList = getBlockList()
        self.cachedMatches = {}

    def tryCast(self, i):
        try:
            i = int(i)
        except:
            print("Failed to cast {0} to an integer. Defaulting to 255".format(i))
            i = 255
        return i

    def getBlock(self, r, g, b):
        tuple = (r, g, b)
        ret = None
        if tuple in self.cachedMatches.keys():
            ret = self.cachedMatches[tuple]
        else:
            casted = (self.tryCast(tuple[0]), self.tryCast(tuple[1]), self.tryCast(tuple[2]))
            shortestDist = None
            for block in self.blockList:
                distance = dist(casted, (block.r, block.g, block.b))
                if shortestDist is None or distance < shortestDist:
                    shortestDist = distance
                    ret = block
            self.cachedMatches[tuple] = ret
            print("cached " + str(tuple))
        return ret

def dist(point1, point2):
    return math.sqrt(
        math.pow(point1[0] - point2[0], 2)
        + math.pow(point1[1] - point2[1], 2)
        + math.pow(point1[2] - point2[2], 2)
    )

def closestBlockColor(rgb, blockList):
    shortestDist = None
    closestBlock = None
    for block in blockList:
        distance = dist(rgb, (block.r, block.g, block.b))
        if shortestDist is None or distance < shortestDist:
            shortestDist = distance
            closestBlock = block
    return closestBlock
