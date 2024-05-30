
# AMS Testing Tool

## Installation

Run below command to create docker image
```bash
docker build -t ams_testing_tool .
```

OR

Pull docker image
```bash
docker pull meetxvii/ams_testing_tool:2.0
```

## Usage

1. Run the application:
```bash
docker run --rm -it --network host -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -e XDG_RUNTIME_DIR=/tmp/runtime-qtuser -u qtuser   --security-opt apparmor=unconfined meetxvii/ams_testing_tool:2.0 python3 /app/app.py
```
>Note: in case of ```no protocols specified``` error run 

```
xhost +local:docker
```

2. Enter your name when prompted.
3. Select the model you want to validate from the given options.
4. The corresponding model window will open, allowing you validate images
5. To change model press `CTRL+Q`
   