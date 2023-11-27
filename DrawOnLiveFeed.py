import numpy as np
import cv2 as cv
import glob

# Load previously saved data
with np.load('C:/Users/Christian/Desktop/MECCATRONICA/Tesi/codetests/Pose_Chess/CamParams.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
    
# Define our drawing function
def draw(img, corners, imgpts):
    corner = list(corners[0].ravel())
    corner[0] = int(corner[0])
    corner[1] = int(corner[1])
    corner= tuple(corner)
    imgpt = list(imgpts[0].ravel())
    imgpt[0] = int(imgpt[0])
    imgpt[1] = int(imgpt[1])
    imgpt= tuple(imgpt)
    img = cv.line(img, corner, imgpt, (255,0,0), 5)
    imgpt = list(imgpts[1].ravel())
    imgpt[0] = int(imgpt[0])
    imgpt[1] = int(imgpt[1])
    imgpt= tuple(imgpt)
    img = cv.line(img, corner, imgpt, (0,255,0), 5)
    imgpt = list(imgpts[2].ravel())
    imgpt[0] = int(imgpt[0])
    imgpt[1] = int(imgpt[1])
    imgpt= tuple(imgpt)
    img = cv.line(img, corner, imgpt, (0,0,255), 5)
    return img

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((13*9,3), np.float32)
objp[:,:2] = np.mgrid[0:13,0:9].T.reshape(-1,2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

video = cv.VideoCapture(0)

while(video.isOpened()):
    ret, img = video.read()
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(gray, (13,9),None)
    if ret == True:
        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        # Find the rotation and translation vectors.
        ret,rvecs, tvecs = cv.solvePnP(objp, corners2, mtx, dist)
        # project 3D points to image plane
        imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
        img = draw(img,corners2,imgpts)
    cv.imshow('img',img)
    if cv.waitKey(1) == ord('q'):
        video.release()
cv.destroyAllWindows()