# cam_stream
R24 streaming script 

## Switch Stream
This will detect different video devices and stream them with fixed intervals
```
usage: switch_stream.py [-h] [--nc NC] [-p PORT] [-i IP] [--timelimit TIMELIMIT]

options:
  -h, --help            show this help message and exit
  --nc NC               number of cameras to check
  -p PORT, --port PORT  port of the first stream
  -i IP, --ip IP        ip address of the server
  --timelimit TIMELIMIT
                        Time between switches in secs

```
## Viewer
Viewer script to stream data and run spect.py script on a selected stream
```
usage: viewer.py [-h] [-i IP] [-p PORT]

options:
  -h, --help            show this help message and exit
  -i IP, --ip IP        ip address of the server to which the client will connect
  -p PORT, --port PORT  port number of the server to which the client will connect
```

## Spect
Script to run analysis on the given image for spectrography
```
usage: spect.py [-h] [--image IMAGE]

options:
  -h, --help     show this help message and exit
  --image IMAGE  image to test
```

**Note** : Run the following if you get backend qt errors (ubuntu)
```
sudo apt install libxcb-cursor0
```
