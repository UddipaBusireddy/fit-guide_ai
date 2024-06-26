import cv2
import numpy as np
import mediapipe as mp
from thread import ThreadedCamera
from exercise import Exercise
from utils import *

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5
performedPushUp = False


class Lunges(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        ang1 = 0
        ang2 = 0
        count = 0
        frames = 0
        performedLunge = False
        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue
            image = cv2.flip(image, 1)
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)
            idx_to_coordinates = get_idx_to_coordinates(image, results)
            try:
                # back - knee - ankle
                if 23 in idx_to_coordinates and 25 in idx_to_coordinates and 27 in idx_to_coordinates:  # left side of body
                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=6,
                             color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[25]), (idx_to_coordinates[27]), thickness=6,
                             color=(255, 0, 0))
                    ang1 = ang((idx_to_coordinates[23], idx_to_coordinates[25]),
                               (idx_to_coordinates[25], idx_to_coordinates[27]))
                    
                    if ang1 < 100:
                        performedLunge = True
                    if ang1 > 150 and performedLunge:
                        count += 1
                        performedLunge = False



                    cv2.putText(image, str(round(ang1, 2)),
                                (idx_to_coordinates[25][0] - 40, idx_to_coordinates[25][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[23]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[23]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[25]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[25]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[27]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[27]), 15, (0, 0, 255), 2)
                if 24 in idx_to_coordinates and 26 in idx_to_coordinates and 28 in idx_to_coordinates:  # right side of body
                    cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=6,
                             color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[26]), (idx_to_coordinates[28]), thickness=6,
                             color=(255, 0, 0))
                    ang2 = ang((idx_to_coordinates[24], idx_to_coordinates[26]),
                               (idx_to_coordinates[26], idx_to_coordinates[28]))
                    if ang1 < 100:
                        performedLunge = True
                    if ang1 > 150 and performedLunge:
                        count += 1
                        performedLunge = False
                    cv2.putText(image, str(round(ang2, 2)),
                                (idx_to_coordinates[26][0] - 40, idx_to_coordinates[26][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[24]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[24]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[26]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[26]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[28]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[28]), 15, (0, 0, 255), 2)
            except:
                pass

            if 0 in idx_to_coordinates:
                cv2.putText(image, "Lunges : " + str(round(count)),
                            (idx_to_coordinates[0][0] - 40, idx_to_coordinates[0][1] + 290),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.2, color=(0, 255, 0), thickness=5)
            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        pose.close()