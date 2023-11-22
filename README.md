# Pointcloud tranformation for the stand alone turntable
This program opens the pointcloud in the `/pointclouds` folder one by one in the interactive 3D vieuwer of open3D.
It allows the user to select a point, close the viewer and than move the origin of the pointcloud to the selected point. 

## Open3d interactive viewer
The left mouse button and moving the mouse rotates the pointcloud and the mouse wheel can be used to zoom. 
Points can be selected by pressing `shift + left click`.
To undo the selection use: `shift + right click`.
After selecting, `q` can be used to close the viewer.
For more information see: http://www.open3d.org/docs/release/tutorial/visualization/interactive_visualization.html

## Getting started
Open a commandline in this folder and run the following commands to create a virtual environment and install the requirements.
```
python -m venv venv
venv/scripts/activate
python -m pip install -R requirements
```
