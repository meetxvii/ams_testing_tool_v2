
# AMS Testing Tool

## Installation

Run below command to create docker image
```bash
docker build -t testingapp .
```

## Usage

1. Run the application:
```bash
docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -u qtuser --network="host" testingapp python3 /app/app.py
```
2. Enter your name when prompted.
3. Select the model you want to validate from the given options.
4. The corresponding model window will open, allowing you validate images
5. To change model press `CTRL+Q`
   