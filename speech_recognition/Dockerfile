# set base image (host OS)
FROM python:3.8 as speech_recognition-docker
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./

# command to run on container start
ENTRYPOINT ["python","./__init__.py"]

