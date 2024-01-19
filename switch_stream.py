import cv2
import numpy as np
import zmq
import time

class SwitchStream:
    def __init__(self, nc: int = 5, ip: str = "192.168.88.63", port: int = 5555, time_limit: int = 10):
        self.cameras = []
        self.nc = nc
        self.time_limit = time_limit

        # Check for available video streams
        self._brute_check()

        # Setup zmq footage socket
        ctx = zmq.Context()
        self.footage_socket = ctx.socket(zmq.PUB)
        self.footage_socket.connect("tcp://{}:{}".format(ip, port))

    def _brute_check(self):
        """ 
            Iterates over video ports brutishly
        """
        index = 0
        curr_camera_count = 0
        
        while True:
            cap = cv2.VideoCapture(index)
            
            if not cap.read()[0]:
                if curr_camera_count == self.nc:
                    cap.release()
                    break
            else:
                self.cameras.append(index)
                curr_camera_count += 1
            
            cap.release()
            index += 1

        print(f"Available cameras: {self.cameras}")

    def capture_cam(self, index: int):
        """ 
            Captures camera for given time limit and releases them
        """
        now = time.time()
        timer = 0
        
        cap = cv2.VideoCapture(index)

        while timer != self.time_limit:
            grabbed, frame = cap.read()
            if not grabbed:
                print("Empty frame!!")
                continue

            _, buffer = cv2.imencode('.jpg', frame)
            self.footage_socket.send(buffer)
        
            end = time.time()
            timer = round(end - now)
        
        cap.release()

    def run(self):
        """ 
            method to iterate over available cams
        """

        while True:
            try:
                for cams in self.cameras:
                    self.capture_cam(cams)
            
            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser()
    ap.add_argument("--nc", type=int, default = 5,
                    help="number of cameras to check")
    ap.add_argument("-p", "--port", type=int, default=5555,
                    help="port of the first stream")
    ap.add_argument("-i", "--ip", type=str, default="192.168.1.99",
                    help="ip address of the server")
    ap.add_argument("--timelimit", type=int, default = 10,
                    help="Time between switches in secs")
    
    args = vars(ap.parse_args())


    switch_stream = SwitchStream(args["nc"], args["ip"], args["port"], args["timelimit"])
    switch_stream.run()
