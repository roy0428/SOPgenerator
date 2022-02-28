import pyrealsense2 as rs
import numpy as np
import cv2
import os
import os.path as osp
import time
import argparse

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('bag_path', type=str, help='path to a bag files or .bag')
    parser.add_argument('-o', '--output_dir', help='path to save extracted data', default=None)
    parser.add_argument('-s', '--save_ply', default=False, action='store_true', help='input sth. to save .ply')
    args = parser.parse_args()
    
    if args.output_dir is None:
        # args.output_dir = os.path.basename(args.bag_path)[:-4]
        args.output_dir = args.bag_path[:-4]
    os.makedirs(args.output_dir, exist_ok=True)
        
    for name in ['color', 'depth', 'lapped', 'verts', 'coord', 'timestamp']:
        os.makedirs(osp.join(args.output_dir, name), exist_ok=True)
    if args.save_ply:
        os.makedirs(osp.join(args.output_dir, 'point'), exist_ok=True)
    
    return args    

def write_ts(output_dir, filename, frame_ts):
    np.save(osp.join(output_dir, 'timestamp', filename + '.npy'), frame_ts)

def write_color(output_dir, filename, color_image):
    cv2.imwrite(osp.join(output_dir, 'color', filename + '.png'), color_image)

def write_depth(output_dir, filename, depth_colormap):
    cv2.imwrite(osp.join(output_dir, 'depth', filename + '.png'), depth_colormap)
    
def write_lapped(output_dir, filename, color_image, depth_colormap):
    weighted = cv2.addWeighted(color_image, 0.5, depth_colormap, 0.5, 0)
    cv2.imwrite(osp.join(output_dir, 'lapped', filename + '.png'), weighted)
    
def write_3D(output_dir, filename, aligned_color_frame, aligned_depth_frame, save_ply = False):
    pc = rs.pointcloud()
    pc.map_to(aligned_color_frame)
    points = pc.calculate(aligned_depth_frame)
    
    # Save point cloud
    if save_ply:
        points.export_to_ply(osp.join(output_dir, 'point', filename + '.ply'), aligned_color_frame)

    # Save 3D coordinates
    v, t = points.get_vertices(), points.get_texture_coordinates()
    verts = np.asanyarray(v).view(np.float32).reshape(aligned_depth_frame.height, aligned_depth_frame.width, 3) # xyz in grid format
    texcoords = np.asanyarray(t).view(np.float32).reshape(aligned_depth_frame.height, aligned_depth_frame.width, 2) # uv in grid format
    np.save(osp.join(output_dir, 'verts', filename + '.npy'), verts)
    np.save(osp.join(output_dir, 'coord', filename + '.npy'), texcoords)

def write_IMU(output_dir, filename, f_gyro, f_accel):
    # Save gyroscope data
    mf_gyro = f_gyro.as_motion_frame()
    pf_gyro = mf_gyro.get_profile()
    data_gyro = mf_gyro.get_motion_data()
    np_gyro = np.array([data_gyro.x, data_gyro.y, data_gyro.z])
    np.save(osp.join(output_dir, 'gyro', filename + '.npy'), np_gyro)
    
    # Save accelerometer data
    mf_accel = f_accel.as_motion_frame()
    pf_accel = mf_accel.get_profile()
    data_accel = mf_accel.get_motion_data()
    np_accel = np.array([data_accel.x, data_accel.y, data_accel.z])
    np.save(osp.join(output_dir, 'accel', filename + '.npy'), np_accel)

def extract(bag_path, output_dir, save_ply):
    # Configure depth, color and IMU streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device_from_file(bag_path, repeat_playback = False)
    config.enable_stream(rs.stream.depth)
    config.enable_stream(rs.stream.color)

    # Start streaming
    profile = pipeline.start(config)
    profile.get_device().as_playback().set_real_time(False)

    # We'll use the colorizer to generate colormap for depth image
    colorizer = rs.colorizer()

    # Create an align object, we plan to align color frames to depth frames
    align = rs.align(rs.stream.color)
    
    while True:
        try:
            time_count = time.time()

            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            aligned_color_frame = aligned_frames.get_color_frame()
            aligned_depth_frame = aligned_frames.get_depth_frame()

            # Validate that all frames are valid
            if not (aligned_color_frame and aligned_depth_frame):
                continue

            # Convert frameset to images
            color_image = cv2.cvtColor(np.asanyarray(aligned_color_frame.get_data()), cv2.COLOR_BGR2RGB)
            depth_colormap = cv2.cvtColor(np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data()), cv2.COLOR_BGR2RGB)

            # Write files
            frame_ts = frames.get_timestamp()
            frame_number = str(frames.get_frame_number()).zfill(5)
            filename = osp.basename(output_dir) + '_' + frame_number
            write_ts(output_dir, filename, frame_ts)
            write_color(output_dir, filename, color_image)
            write_depth(output_dir, filename, depth_colormap)
            write_lapped(output_dir, filename, color_image, depth_colormap)
            write_3D(output_dir, filename, aligned_color_frame, aligned_depth_frame, save_ply = save_ply)
            print('Filename:', filename, ', Elapsed time:', time.time() - time_count)
        except:
            break
    # Stop streaming
    pipeline.stop()

if __name__ == '__main__':
    args = parse()
    if osp.splitext(args.bag_path)[1] == '.bag':
        print('Extracting:', osp.basename(args.bag_path))
        extract(args.bag_path, args.output_dir, args.save_ply)

