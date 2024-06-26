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

class PullUps(Exercise):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.curlUp = False
        self.curlDown = False

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
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)

            idx_to_coordinates = get_idx_to_coordinates(image, results)

            try:
                # Detect key points for shoulder, elbow, and wrist for both sides
                if 11 in idx_to_coordinates and 13 in idx_to_coordinates and 15 in idx_to_coordinates: 
                    ang1 = ang((idx_to_coordinates[11], idx_to_coordinates[13]),
                               (idx_to_coordinates[13], idx_to_coordinates[15]))

                    # Calculate angle for left side
                    if ang1 < 90:
                        self.curlUp = True

                    if ang1 > 160 and self.curlUp:
                        self.curlDown = True

                    if self.curlUp and self.curlDown:
                        self.count += 1
                        self.curlUp = False
                        self.curlDown = False

                    # Visualize landmarks and angles (optional)
                    cv2.line(image, idx_to_coordinates[11], idx_to_coordinates[13], thickness=6, color=(255, 0, 0))
                    cv2.line(image, idx_to_coordinates[13], idx_to_coordinates[15], thickness=6, color=(255, 0, 0))
                    cv2.putText(image, str(round(ang1, 2)),
                                (idx_to_coordinates[13][0] - 40, idx_to_coordinates[13][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, idx_to_coordinates[11], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[11], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[13], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[13], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[15], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[15], 15, (0, 0, 255), 2)

                if 12 in idx_to_coordinates and 14 in idx_to_coordinates and 16 in idx_to_coordinates:
                    ang2 = ang((idx_to_coordinates[12], idx_to_coordinates[14]),
                               (idx_to_coordinates[14], idx_to_coordinates[16]))

                    # Calculate angle for right side
                    if ang2 < 90:
                        self.curlUp = True

                    if ang2 > 160 and self.curlUp:
                        self.curlDown = True

                    if self.curlUp and self.curlDown:
                        self.count += 1
                        self.curlUp = False
                        self.curlDown = False

                    # Visualize landmarks and angles (optional)
                    cv2.line(image, idx_to_coordinates[12], idx_to_coordinates[14], thickness=6, color=(255, 0, 0))
                    cv2.line(image, idx_to_coordinates[14], idx_to_coordinates[16], thickness=6, color=(255, 0, 0))
                    cv2.putText(image, str(round(ang2, 2)),
                                (idx_to_coordinates[14][0] - 40, idx_to_coordinates[14][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, idx_to_coordinates[12], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[12], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[14], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[14], 15, (0, 0, 255), 2)
                    cv2.circle(image, idx_to_coordinates[16], 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, idx_to_coordinates[16], 15, (0, 0, 255), 2)

            except Exception as e:
                print(f"Error processing frame: {e}")

            cv2.putText(image, "Pull-ups: " + str(self.count),
                        (50, 50),  # Fixed coordinates for top placement
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1.2, color=(0, 255, 0), thickness=5)

            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break

        pose.close()

if __name__ == "__main__":
    pull_ups = PullUps()
    pull_ups.exercise(0)  # Use 0 for webcam or provide the path to the video file
