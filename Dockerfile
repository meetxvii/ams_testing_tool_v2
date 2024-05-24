FROM jozo/pyqt5

RUN mkdir /app
WORKDIR /app
COPY . /app

ENV QT_QUICK_BACKEND=software

RUN apt-get update
RUN apt-get install -y python3-pip

RUN apt-get update && apt-get install -y \
    python3-pyqt5.qtopengl \
    python3-pyqt5.qtquick \
    python3-pyqt5.qtmultimedia \
    # Install Qml
    qmlscene \
    qml-module-qtqml* \
    qml-module-qtquick* \
    qml-module-qmltermwidget \
    qml-module-qt-websockets \
    qml-module-qt3d \
    qml-module-qtaudioengine \
    qml-module-qtav \
    qml-module-qtbluetooth \
    qml-module-qtcharts \
    qml-module-qtdatavisualization \
    qml-module-qtgraphicaleffects \
    qml-module-qtgstreamer \
    qml-module-qtlocation \
    qml-module-qtmultimedia \
    qml-module-qtpositioning \
    # Libraries for multimedia
    libqt5multimedia5-plugins \
    gstreamer1.0-libav \
    gstreamer1.0-alsa \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    alsa-base \
    alsa-utils 
    

RUN pip3 install pymongo 