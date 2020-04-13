import argparse

def getCmdLineArgs():
    parser = argparse.ArgumentParser(description="Interpolates z coordinates in a csv file", usage="%(prog)s [filename]")
    parser.add_argument("filename", metavar="filename", type=argparse.FileType("r"), nargs=1, help="the csv file to interpolate")
    args = parser.parse_args()
    return args

def printFile(file):
    for line in file:
        print(line)
    
if __name__ == "__main__":
    file = getCmdLineArgs().filename[0]
    print(file.name)
    printFile(file)
