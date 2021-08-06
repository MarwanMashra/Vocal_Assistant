############ This image is built for Raspberry Pi (arm64-v8) ############ 

# set base image (host OS)
FROM lbischof/face_recognition as face_recognizer-docker-arm
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./

# command to run on container start
ENTRYPOINT ["python","./__init__.py"]



############ This image is built for x86 based processors ############

# set base image (host OS)
FROM aaftio/face_recognition as face_recognizer-docker-x86
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./

# command to run on container start
ENTRYPOINT ["python","./__init__.py"]



