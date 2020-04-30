# Feature Manipulation Engine Minecraft Converter

A conversion program used to import 3D coordinate files into Minecraft.

## Project Purpose

Three dimensional coordinate files are used frequently in the American River College Design Hub, be it for 3D modeling software such as Blender, Computer Aided Design software like AutoCAD, or various drone projects. These applications are incredibly useful for designing 3D objects, but require specialized training or licenses to use. To rectify this issue, this program can convert files to a format anyone can use: Minecraft. Minecraft allows for easy, if not precise, manipulation of 3D spaces in a way many are familiar with.

## Getting Started

Several components of this project require Python 3, which you can download [here](https://www.python.org/downloads/).

In order to run the FME converter workspaces, you will need FME Desktop installed. You can start a free trial of FME Desktop [here](https://www.safe.com/fme/fme-desktop/), but it will require purchasing a license to continue using the application after the free trial expires. Contact a Design Hub supervisor for more details.

In addition, you will need Minecraft Java Edition installed. You can download the Minecraft trial [here](https://www.minecraft.net/en-us/download/), after doing so, you will need to purchase access to the full game (I don't have the URL for this).

## Converting files to Minecraft (the easy way)

1. Double click on `launch.bat`
2. Once Python launches, follow the onscreen prompt.
3. You're done!



## Converting OBJ files to CSV
    There are currently two ways to convert OBJ files to CSV:
(a) Use `objToCsv.fmw`: this will produce a more accurate CSV file,
but it extremely slow, at least on my laptop.
(b) Use the Python script: significantly faster, but it just extracts vertices from the OBJ file, so it's less accurate.
1. Open a command prompt, and navigate to the project root directory.
2. Run the following command to convert the OBJ file to a csv file:
`python objToCsv.py /path/to/filename.obj`
which will output the converted file to your current directory as `filename_obj.csv`.

## Converting RVT files to CSV

Open `revitNativeToCsv.fme` in FME Desktop, and run the workspace with the Revit file you wish to convert.

## User Parameters (revitNativeToCsv.fmw)
* Revit Project Files: the .rvt file to convert.
* Feature Types to Read: Unknown what this does. You should ignore it.
* Destination CSV folder: the directory to write output files to.
* resultFileName: the name to save the resulting csv file as. Given a source file name of filename.rvt, the resultFileName defaults to filename_rvt.

## Converting CSV files to Minecraft

Choose 1:
Open `Converter.fmw` in FME Desktop, and run it with a CSV file with the headers x, y, z, r, g, b (no space between headers!).

## User Parameters (Converter.fmw)
When running `Converter.fmw`, the user will be asked for a series of parameters.
* Destination Minecraft Folder: the "saves" folder under the user's minecraft folder. Be sure to change this value when you first download the program from GitHub.
* Source CSV: the CSV file to convert. It must contain the headers [x, y, z, r, g, b], with no spaces between headers. Coordinates are measured in meters (blocks in Minecraft).
* Feature Types to read: Unknown what this does. You should ignore it.
* Should the world read color from the source file?: If set to yes, for every point in the source CSV file, assigns the block from `colorToBlockTable.csv` with the closest matching color to that point. If set to no, every point is converted to a block of Quartz.



## Contributing

Since this project is the property of the American River College Design Hub, it is not open to contributions by developers outside the company. If you are an intern or employee of the Design Hub, and are interested in working on the project, please contact Matt Crow (w# is 1599227), and he can get you set up.

## Project Contributors

* **Matt Crow** - *Initial work* - [IronHeart7334](https://github.com/IronHeart7334)

See also the list of [contributors](https://github.com/design-hub-arc/ARCDHWebAutomator/contributors) who participated in this project.
