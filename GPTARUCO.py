import cv2
import cv2.aruco as aruco
import numpy as np

class ArucoMarkerTracker:
    def __init__(self):
        # Initialize ArUco dictionary and parameters
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        self.aruco_params = aruco.DetectorParameters_create()
        self.marker_length = 0.5  # Set the length of the marker side in meters

    def detect_markers(self, frame):
        # Detect ArUco markers in the frame
        corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            # Draw the detected markers on the frame
            aruco.drawDetectedMarkers(frame, corners, ids)

            # Iterate over the detected markers
            for i in range(len(ids)):
                # Estimate the pose of the marker
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners[i], self.marker_length, camera_matrix, distortion_coefficients)
                # Declare the cube in space
                # Define variables for cube dimensions and position
                
                base_length = 0.15  # Length of the cube base
                base_width = 0.15   # Width of the cube base
                height = 0.2       # Height of the cube
                center_x = 0.0      # X-coordinate of the center of the base
                center_y = 1      # Y-coordinate of the center of the base

                # Calculate the coordinates of the cube vertices
                vertices = np.float32([
                    [center_x - base_length / 2, center_y - base_width / 2, 0],                 
                    [center_x - base_length / 2, center_y + base_width / 2, 0],                
                    [center_x + base_length / 2, center_y + base_width / 2, 0],               
                    [center_x + base_length / 2, center_y - base_width / 2, 0],                
                    [center_x - base_length / 2, center_y - base_width / 2, height],     
                    [center_x - base_length / 2, center_y + base_width / 2, height],      
                    [center_x + base_length / 2, center_y + base_width / 2, height],      
                    [center_x + base_length / 2, center_y - base_width / 2, height],
                ])
                
                # Project the cube points onto the image
                cube_points, _ = cv2.projectPoints(vertices, rvec, tvec, camera_matrix, distortion_coefficients)

                # Draw lines to represent the cube
                frame = self.draw_cube(frame, cube_points)

    def draw_cube(self, frame, cube_points):
        for i in range(4):
            p1 = tuple(cube_points[i].ravel().astype(int))
            p2 = tuple(cube_points[(i + 1) % 4].ravel().astype(int))
            if self.are_points_valid(p1, p2):
                frame = cv2.line(frame, p1, p2, (0, 255, 0), 1)  # Green lines on the top of the cube

            p1 = tuple(cube_points[i].ravel().astype(int))
            p2 = tuple(cube_points[i + 4].ravel().astype(int))
            if self.are_points_valid(p1, p2):
                frame = cv2.line(frame, p1, p2, (0, 255, 0), 1)  # Green lines from top to bottom

            p1 = tuple(cube_points[i + 4].ravel().astype(int))
            p2 = tuple(cube_points[(i + 1) % 4 + 4].ravel().astype(int))
            if self.are_points_valid(p1, p2):
                frame = cv2.line(frame, p1, p2, (0, 255, 0), 1)  # Green lines on the bottom of the cube

        return frame

    def are_points_valid(self, *points):
        return all(np.isfinite(coord) for point in points for coord in point)
    
    
    def run(self):
        # Open a video capture
        cap = cv2.VideoCapture(0)  # Use 0 for the default camera, or specify a video file path

        while True:
            # Read a frame from the video capture
            ret, frame = cap.read()

            if not ret:
                print("Failed to capture frame.")
                break

            # Detect ArUco markers and draw augmented reality cube
            self.detect_markers(frame)

            # Display the resulting frame
            cv2.imshow('Aruco Marker Tracking', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture and close all windows
        cap.release()
        cv2.destroyAllWindows()


# Set your camera matrix and distortion coefficients

with np.load('C:/Users/Christian/Desktop/MECCATRONICA/Tesi/codetests/Pose_Aruco/CamParams.npz') as X:
    camera_matrix, distortion_coefficients, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]


# Create an instance of the ArucoMarkerTracker class and run the script
aruco_tracker = ArucoMarkerTracker()
aruco_tracker.run()

