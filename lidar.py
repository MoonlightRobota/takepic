import pyrealsense2 as rs
import cv2 as cv
import serial

# Create a context object. This object owns the handles to all connected realsense devices
pipeline = rs.pipeline()
config = rs.config()

# Configure the pipeline to stream the depth sensor's data
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            raise RuntimeError("Could not acquire a depth frame.")

        # Get the depth frame's dimensions
        width = depth_frame.get_width()
        height = depth_frame.get_height()

       # for y in range(0, height, 50):
        for x in range(0, width, 25):
            # Get the distance of the pixel at (x, y) in meters
            distance = depth_frame.get_distance(x, int(height / 2))

            # Convert distance to centimeters
            distance_cm = distance * 100

            # Check if the pixel is within 10 centimeters
            if distance_cm <= 500 and distance_cm > 0:
                print(f"The pixel at ({x}, {int(height/2)}) is {distance_cm} centimeters of the camera.")
                ser.write(f"{distance_cm},{x}\n".encode())
except Exception as e:
    print(e)
finally:
    # Stop streaming
    pipeline.stop()