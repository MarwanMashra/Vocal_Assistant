############ This image is built for Raspberry Pi (arm64-v8) ############ 

# set base image (host OS)
FROM python:3.8 as speech_to_text-docker-arm
# set the working directory in the container
WORKDIR /
RUN apt-get update && apt-get install -y apt-utils 
RUN apt-get install net-tools
RUN apt-get install flac -y
RUN apt-get install portaudio19-dev python-all-dev -y

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./


# command to run on container start
ENTRYPOINT ["python", "__init__.py"]




############ This image is built for x86 based processors ############


FROM python:3.8 as speech_to_text-docker-x86
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./

# command to run on container start
ENTRYPOINT ["python","./__init__.py"]

