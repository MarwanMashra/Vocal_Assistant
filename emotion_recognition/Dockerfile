# set base image (host OS)
# FROM python:3.8 as emotion_recognition
FROM jjanzic/docker-python3-opencv:opencv-4.0.1
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./
RUN pip install tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl
RUN rm tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl

# command to run on container start
CMD [ "python","./app.py"]