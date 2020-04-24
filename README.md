# Feature Manipulation Engine Minecraft Converter

A conversion program used to import 3D coordinate files into Minecraft.

## Project Purpose

Three dimensional coordinate files are used frequently in the American River College Design Hub, be it for 3D modeling software such as Blender, Computer Aided Design software like AutoCAD, or various drone projects. These applications are incredibly useful for designing 3D objects, but require specialized training or licenses to use. To rectify this issue, this program can convert files to a format anyone can use: Minecraft. Minecraft allows for easy, if not precise, manipulation of 3D spaces in a way many are familiar with.

## Getting Started

Several components of this project require Python 3, which you can download [here](https://www.python.org/downloads/).

In order to run the FME converter workspaces, you will need FME Desktop installed. You can start a free trial of FME Desktop [here](https://www.safe.com/fme/fme-desktop/), but it will require purchasing a license to continue using the application after the free trial expires. Contact a Design Hub supervisor for more details.

In addition, you will need Minecraft Java Edition installed. You can download the Minecraft trial [here](https://www.minecraft.net/en-us/download/), after doing so, you will need to purchase access to the full game (I don't have the URL for this).

## Converting OBJ files to CSV

1. Open a command prompt, and navigate to the project root directory.
2. Run the following command to convert the OBJ file to a csv file:
`python objToCsv.py /path/to/filename.obj`
which will output the converted file to your current directory as `filename_obj.csv`.

## Converting RVT files to CSV

Open `revitNativeToCsv.fme` in FME Desktop, and run the workspace with the Revit file you wish to convert. Given an input file of `filename.rvt`, the converter will output `filename_rvt.csv`.

## Converting CSV files to Minecraft

Choose 1:
(a): Open `Converter.fmw` in FME Desktop, and run it with a CSV file with the headers x, y, z, r, g, b (no space between headers!).
or (b): run `convert.bat` from the command prompt as shown:
`convert.bat /path/to/csvFile.csv`

## User Parameters
When running the program, the user will be asked for a series of parameters.
* Destination Minecraft Folder: the "saves" folder under the user's minecraft folder. Be sure to change this value when you first download the program from GitHub.
* World name: the name of the minecraft world to output data to. Note that FME will create the world if it does not yet exist, or overwrite the world if it does.
* Point cloud file: the CSV file to convert. Currently, the program does not require headers, it only requires that the file follow the guidelines stated above.
* World size: The width and depth to scale points to. Essentially, if you were to set 64 as the world size, imagine a 64 by 64 block box around all the x-y points in the data set, where  the smallest x and y coordinates mark one corner of the box, and the largest mark the diagonal opposite corner.
* Height scale: The maximum height to scale z-coordinates to after shifting, in blocks. The lowest point in the point cloud will be scaled and shifted to have a z-coordinate of 0, while the highest point will be scaled and shifted to have a z-coordinate of this height scale value, with all points in between being adjusted accordingly.
* "Should the height axis scale with the other axes?": Since z-coordinates are restricted in their values, but x- and y-coordinates are not, vastly spread out z-coordinates will require a small scaling factor, which will also force x- and y-coordinates to a small scaling factor to maintain scale. Selecting "no" for this parameter will cause the z-axis to scale independent of the x- and y-axes, whereas selecting "yes" will force all three axes to maintain the same scaling factor.
* Point reduction factor: Used to calculate the maximum number of points to include in the point cloud after thinning, with larger point reduction factors yielding fewer maximum points. For example, given a world size of 64x64x64, and a point reduction factor of 100, the point cloud will be thinned to at most (643)/100=2621points.


## Contributing

Since this project is the property of the American River College Design Hub, it is not open to contributions by developers outside the company. If you are an intern or employee of the Design Hub, and are interested in working on the project, please contact Matt Crow (w# is 1599227), and he can get you set up.

## Project Contributors

* **Matt Crow** - *Initial work* - [IronHeart7334](https://github.com/IronHeart7334)

See also the list of [contributors](https://github.com/design-hub-arc/ARCDHWebAutomator/contributors) who participated in this project.
