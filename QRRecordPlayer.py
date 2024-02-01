import cv2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep

# Spotify Authentication
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

# OpenCV Intialization with camera
cap = cv2.VideoCapture(0)
# QR code detection Method
detector = cv2.QRCodeDetector()

data = ""
oldData = ""

# Infinite loop to keep the camera searching for data at all times
while True:
    
    # image from the camera
    _, img = cap.read()
    
    # read the QR code by detetecting the bounding box coords and decoding QR data 
    data, bbox, _ = detector.detectAndDecode(img)
    
    # if there is a bounding box, draw one, along with the data
    if bbox is not None:
        bb_pts = bbox.astype(int).reshape(-1, 2)
        num_bb_pts = len(bb_pts)
        for i in range(num_bb_pts):
            cv2.line(img,
                     tuple(bb_pts[i]),
                     tuple(bb_pts[(i+1) % num_bb_pts]),
                     color=(255, 0, 255), thickness=2)
        cv2.putText(img, data,
                    (bb_pts[0][0], bb_pts[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        
        #If the data is a good Spotify URI it will begin to play the song, album, or playlist requested
        if data and data != oldData:
            oldData = data
            print("data found: ", data)
            try:
                sp.start_playback(device_id='ae985dc5eb61110a58403ca060edf50748bbee31',uris=[data])
            except:
                print("That was not a vaild Spotify UID try again...")


    # display the live camera feed to the Desktop on Raspberry Pi OS preview
    cv2.imshow("code detector", img)
    
    # press 'q' on keyboard to quit program
    if(cv2.waitKey(1) == ord("q")):
        break
    
# close all the applications/windows created
cap.release()
cv2.destroyAllWindows()



