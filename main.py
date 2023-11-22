import open3d as o3d
import numpy as np
from pathlib import Path
from time import sleep

def pick_points(pcd):
    print("")
    print("1) Please pick at least three points on the cube and than you origin point using [shift + left click]")
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    print("3) Use shift + '+' or '-' to change the marker size")
    # See here for the other controls: https://github.com/isl-org/Open3D/blob/d7341c4373e50054d9dbe28ed84c09bb153de2f8/src/Visualization/Visualizer/VisualizerWithEditing.cpp#L124

    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    return vis.get_picked_points()


if __name__ == '__main__':
    # Loop over all pointclouds in the folder
    folder = Path('pointclouds')
    output_folder = Path("results")
    output_folder.mkdir(parents=True, exist_ok=True)

    for filename in sorted(folder.rglob("*.ply")):
        pcd = o3d.io.read_point_cloud(str(filename))

        selected_points = pick_points(pcd)
        origin_idx = selected_points[-1]

        # Move zero point to the new origin
        new_origin = pcd.points[origin_idx]
        # Wat to move to 0 so oposite of current position
        pcd_tx = pcd.translate(new_origin * -1)
        output_filename = str(Path.joinpath(output_folder, filename.stem + "_recentered.ply"))
        o3d.io.write_point_cloud(output_filename, pcd_tx)

        # Optional sleep between pointclouds to give the user a second to release the q key.
        sleep(1)
