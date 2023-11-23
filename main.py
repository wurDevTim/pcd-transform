import open3d as o3d
import numpy as np
from pathlib import Path
from time import sleep
from copy import deepcopy
from scipy.spatial.transform import Rotation as R

# -------------------------------
# Simple program intended to correct to photoneo pointclouds
# It start by opening a 3D viewer which allows users to pick 3 points.
# The first 3 should be on the rockwool and are used for the rotational correction.
# This is done with the align_vectors function of scipi, alternatively the normals of the rockwool block can be used.
# The last one is used as new origin for the pointcloud
# Based on: http://www.open3d.org/docs/latest/tutorial/Basic/transformation.html
# --------------------------------


def pick_points(pcd):
    """Üse the interactive vizualisation of open3d to enable users to select points """
    print("")
    print("1) Please pick at least three points on the cube and than you origin point using [shift + left click]")
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    print("3) Use shift + '+' or '-' to change the marker size")
    # For the other controls see: 
    # https://github.com/isl-org/Open3D/blob/d7341c4373e50054d9dbe28ed84c09bb153de2f8/src/Visualization/Visualizer/VisualizerWithEditing.cpp#L124

    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points
    vis.destroy_window()
    print("")
    return vis.get_picked_points()

def vizualize_rotation():
    """"Create a reference frame and rotate/move it like the pointcloud will rotate, for debugging purposes only"""
    inv_rotation, inv_rssd = R.align_vectors(b=target_vectors, a=source_vectors, weights=weights)
    #rot_vec = rotation.as_rotvec()
    ref_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=25, origin=[0, 0, 0])
    ref_frame_rot = deepcopy(ref_frame)
    ref_frame_rot.rotate(inv_rotation.as_matrix(), center=(0, 0, 0))
    o3d.visualization.draw_geometries([ref_frame, ref_frame_rot])


if __name__ == '__main__':
    # Loop over all pointclouds in the folder
    folder = Path('pointclouds')
    output_folder = Path("results")
    output_folder.mkdir(parents=True, exist_ok=True)

    for filename in sorted(folder.rglob("*.ply")):
        pcd = o3d.io.read_point_cloud(str(filename))

        selected_points = pick_points(pcd)
        origin_idx = selected_points[-1]
        plain_points = selected_points[:-1]

        # Rotate the pointcloud
        p0 = pcd.points[plain_points[0]]
        p1 = pcd.points[plain_points[1]]
        p2 = pcd.points[plain_points[2]]
        # compute vectors
        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)

        target_vectors = np.array([[1, 0, 0], [0, 0, 1]])
        source_vectors = np.vstack((v0, v1))
        weights = np.array([0.7, 0.3])
        # Rotation vector b to vector a
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.align_vectors.html#scipy.spatial.transform.Rotation.align_vectors
        #vizualize_rotation()
        rotation, rssd = R.align_vectors(a=target_vectors, b=source_vectors, weights=weights)
        rot_vec = rotation.as_rotvec()
        pcd_r = deepcopy(pcd)
        pcd_r.rotate(rotation.as_matrix(), center=(0, 0, 0))

        # Move zero point to the new origin
        new_origin = pcd_r.points[origin_idx]
        # Wat to move to 0 so oposite of current position
        pcd_tx = pcd_r.translate(new_origin * -1)
        output_filename = str(Path.joinpath(output_folder, filename.stem + "_recentered.ply"))
        o3d.io.write_point_cloud(output_filename, pcd_tx)

        # Optional sleep between pointclouds to give the user a second to release the q key.
        sleep(1)
