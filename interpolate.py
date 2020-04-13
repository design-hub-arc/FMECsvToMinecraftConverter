import argparse

def getCmdLineArgs():
    parser = argparse.ArgumentParser(description="Interpolates z coordinates in a csv file", usage="%(prog)s [filename]")
    parser.add_argument("filename", metavar="filename", type=argparse.FileType("r"), nargs=1, help="the csv file to interpolate")
    args = parser.parse_args()
    return args
    
if __name__ == "__main__":
    print(getCmdLineArgs().filename)
