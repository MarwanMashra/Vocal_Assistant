# set base image (host OS)
# FROM python:3.8 as emotion_recognition
FROM jjanzic/docker-python3-opencv:opencv-4.0.1 as emotion_recognition-docker
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy all files from the local directory to the working directory
COPY *.* /
RUN pip install tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl
RUN rm tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl

# copy the content of all directories to the working directory while keeping the path
COPY emojis /emojis/
COPY haarcascades /haarcascades/
COPY media /media/
COPY models /models/
COPY save_loc /save_loc/
COPY saved_images /saved_images/

# command to run on container start
ENTRYPOINT [ "python","./__init__.py"]