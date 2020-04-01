import os

def clean():
    currDir = os.path.dirname(os.path.abspath(__file__))
    print("Current directory is " + currDir)
    for file in os.listdir(currDir):
        if file.endswith(".log"):
            print("delete " + file)
            os.remove(os.path.join(currDir, file))
    
clean()
