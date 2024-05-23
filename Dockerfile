FROM jozo/pyqt5

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apt-get update
RUN apt-get -y install python3-pip

RUN pip3 install --upgrade setuptools
RUN pip3 install --upgrade pip

RUN pip install --force-reinstall --no-deps PyQt5==5.14.1
RUN pip3 install -r requirements.txt