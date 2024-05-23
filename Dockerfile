FROM jozo/pyqt5

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get -y install python3-pip
