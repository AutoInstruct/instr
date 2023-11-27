import cv2
import cv2.aruco as aruco
import numpy as np

class ArucoMarkerTracker:
    def __init__(self):
        # Initialize ArUco dictionary and parameters
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_100)
        self.aruco_params = aruco.DetectorParameters_create()
        self.marker_length = 0.1  # Set the length of the marker side in meters
        self.cube_height = 0.1  # Set the height of the cube above the marker's plane in meters
        self.cube_base_size = 0.05  # Set the size of the cube's base in meters

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

                # Calculate the position of the cube base on the marker's plane
                cube_base = tvec[0] - np.array([self.cube_base_size / 2, self.cube_base_size / 2, 0])

                # Calculate the position of the cube top above the marker's plane
                cube_top = tvec[0] - np.array([self.cube_base_size / 2, self.cube_base_size / 2, self.cube_height])

                # Project the cube base and top onto the image
                cube_base_projected, _ = cv2.projectPoints(np.float32([cube_base]), rvec, tvec, camera_matrix, distortion_coefficients)
                cube_top_projected, _ = cv2.projectPoints(np.float32([cube_top]), rvec, tvec, camera_matrix, distortion_coefficients)

                # Draw lines to represent the cube
                frame = self.draw_cube(frame, cube_base_projected, cube_top_projected)

        return frame

    def draw_cube(self, frame, cube_base, cube_top):
        cube_base = cube_base[0].ravel().astype(int)
        cube_top = cube_top[0].ravel().astype(int)

        # Draw lines from cube top to base
        frame = cv2.line(frame, (cube_base[0], cube_top[1]), tuple(cube_top), (0, 255, 0), 3)  # Green line on the side
        frame = cv2.line(frame, (cube_top[0], cube_base[1]), tuple(cube_top), (0, 255, 0), 3)  # Green line on the side

        # Draw vertical lines connecting the top and base
        frame = cv2.line(frame, tuple(cube_base), (cube_base[0], cube_top[1]), (0, 255, 0), 3)  # Green line on the bottom
        frame = cv2.line(frame, tuple(cube_top), (cube_top[0], cube_base[1]), (0, 255, 0), 3)  # Green line on the top

        return frame

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
            frame = self.detect_markers(frame)

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


