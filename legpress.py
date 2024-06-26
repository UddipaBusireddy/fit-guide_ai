import cv2
import numpy as np
import mediapipe as mp
from thread import ThreadedCamera
from exercise import Exercise
from utils import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

class LegPress(Exercise):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.press_down = False
        self.press_up = False
        self.correct_form = True

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)

        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue

            image = cv2.flip(image, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)

            idx_to_coordinates = get_idx_to_coordinates(image, results)

            try:
                if 23 in idx_to_coordinates and 25 in idx_to_coordinates and 27 in idx_to_coordinates:  
                    ang1 = ang((idx_to_coordinates[23], idx_to_coordinates[25]),
                               (idx_to_coordinates[25], idx_to_coordinates[27]))
                    if ang1 < 95:
                        self.press_down = True

                    if ang1 > 125 and self.press_down:
                        self.press_up = True

                    if self.press_down and self.press_up :
                        self.count += 1
                        self.press_down = False
                        self.press_up = False
                    cv2.line(image, idx_to_coordinates[23], idx_to_coordinates[25], thickness=6, color=(255, 0, 0))
                    cv2.line(image, idx_to_coordinates[25], idx_to_coordinates[27], thickness=6, color=(255, 0, 0))
                    cv2.putText(image, str(round(ang1, 2)),
                                (idx_to_coordinates[25][0] - 40, idx_to_coordinates[25][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, idx_to_coordinates[23], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[23], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[25], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[25], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[27], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[27], 15, (0, 0, 255), 2)
                if 24 in idx_to_coordinates and 26 in idx_to_coordinates and 28 in idx_to_coordinates:  # right side
                    ang_right = ang((idx_to_coordinates[24], idx_to_coordinates[26]),
                                (idx_to_coordinates[26], idx_to_coordinates[28]))
                    if ang_right < 85:
                        self.press_down_right = True

                    if ang_right > 125 and self.press_down_right:
                        self.press_up_right = True

                    if self.press_down_right and self.press_up_right :
                        self.count += 1
                        self.press_down_right = False
                        self.press_up_right = False
                    cv2.line(image, idx_to_coordinates[24], idx_to_coordinates[26], thickness=6, color=(0, 255, 0))
                    cv2.line(image, idx_to_coordinates[26], idx_to_coordinates[28], thickness=6, color=(0, 255, 0))
                    cv2.putText(image, str(round(ang_right, 2)),
                                (idx_to_coordinates[26][0] - 40, idx_to_coordinates[26][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, idx_to_coordinates[24], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[24], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[26], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[26], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[28], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[28], 15, (0, 0, 255), 2)
            except Exception as e:
                print(f"Error processing frame: {e}")

            # Provide feedback if form is incorrect

            cv2.putText(image, "Leg Press: " + str(self.count),
                        (50, 50),  # Fixed coordinates for top placement
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(0, 255, 0), thickness=2)

            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        pose.close()

    

if __name__ == "__main__":
    leg_press = LegPress()
    leg_press.exercise(0)  # Use 0 for webcam or provide the path to the video file
