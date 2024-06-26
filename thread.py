from threading import Thread, Lock
import cv2
import time

class ThreadedCamera:
    def __init__(self,src=0):
        print("Initializing camera...")
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            raise ValueError(f"Error: Couldn't read video stream from source '{src}'")
        print("Camera initialized.")
        
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.FPS = 1 / 60
        self.FPS_MS = int(self.FPS * 1000)
        self.frame = None
        self.status = False
        self.lock = Lock()  # Create a lock for synchronization

        # Start frame retrieval thread
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        print("Starting frame capture thread...")
        while self.capture.isOpened():
            status, frame = self.capture.read()
            if status:
                with self.lock:
                    self.status = status
                    self.frame = frame.copy()  # Make a copy of the frame for safety
            else:
                print("Failed to read frame.")
            time.sleep(self.FPS)
        print("Exiting frame capture thread.")

    def show_frame(self):
        with self.lock:
            if self.status:
                return True, self.frame
            return False, None

    def __del__(self):
        if self.capture.isOpened():
            self.capture.release()
        print("Camera released.")

# Test the ThreadedCamera class
def main():
    print("Starting main function...")
    threaded_camera = ThreadedCamera(0)
    while True:
        success, frame = threaded_camera.show_frame()
        if not success:
            print("Failed to grab frame.")
            continue

        cv2.imshow("Threaded Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    print("Exiting main function.")

if __name__ == "__main__":
    main()
