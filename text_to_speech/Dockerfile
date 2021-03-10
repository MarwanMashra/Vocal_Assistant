# set base image (host OS)
FROM python:3.8 as text_to_speech-docker
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY * ./

# command to run on container start
ENTRYPOINT ["python","./__init__.py"]


# pour utiliser playsound:
# RUN apt-get update
# RUN apt-get install python3-gi python3-gi-cairo python3-gst-1.0 -y
# RUN ln -s /usr/lib/python3/dist-packages/gi/ /usr/local/lib/python3.7/site-packages/
