import cv2
import numpy as np
import zmq
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--port", nargs='+',type=int, default=[5555,5556,5557],
    help="port of the first stream")
ap.add_argument("-i", "--ip", type=str, default="192.168.1.99",
    help="ip address of the server")
ap.add_argument("-c", "--cam", nargs='+', type=int, default=[0, 1, 2],
    help="camera index to use")
args = vars(ap.parse_args())

cap1 = cv2.VideoCapture(args["cam"][0])
cap2 = cv2.VideoCapture(args["cam"][1])
cap3 = cv2.VideoCapture(args["cam"][2])

context_1 = zmq.Context()
context_2 = zmq.Context()
context_3 = zmq.Context()
footage_socket_1 = context_1.socket(zmq.PUB)
footage_socket_2 = context_2.socket(zmq.PUB)
footage_socket_3 = context_3.socket(zmq.PUB)
footage_socket_1.connect("tcp://{}:{}".format(args["ip"], args["port"][0]))
footage_socket_2.connect("tcp://{}:{}".format(args["ip"], args["port"][1]))
footage_socket_3.connect("tcp://{}:{}".format(args["ip"], args["port"][2]))

while True:
    try:
        grabbed, frame_from_first = cap1.read()
        grabbed, frame_from_second = cap2.read()
        grabbed, frame_from_third = cap3.read()

        _, buffer_from_first = cv2.imencode('.jpg', frame_from_first)
        _, buffer_from_second = cv2.imencode('.jpg', frame_from_second)
        _, buffer_from_third = cv2.imencode('.jpg', frame_from_third)
        
        footage_socket_1.send(buffer_from_first)
        footage_socket_2.send(buffer_from_second)
        footage_socket_3.send(buffer_from_third)
    except KeyboardInterrupt:
        cap1.release()
        cap2.release()
        cap3.release()
        cv2.destroyAllWindows()
        break    
