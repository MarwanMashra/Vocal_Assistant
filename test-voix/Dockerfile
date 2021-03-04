# set base image (host OS)
FROM python:3.7
# set the working directory in the container
WORKDIR /

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pgi

# copy the content of the local src directory to the working directory
COPY * ./
# RUN update-alternatives --config python3
# RUN apt install python3-gi
# RUN apt-get install python3-gi
# RUN ln -s /usr/lib/python3/dist-packages/gi/_gi.cpython-37m-x86_64-linux-gnu.so
# RUN pip install python3-gi

RUN apt-get update
RUN apt-get install python3-gi python3-gi-cairo python3-gst-1.0 -y
# gir1.2-gtk-3.0
# RUN apt-get install python3-gst-1.0

# RUN apt-get install sudo -y

# RUN pip install vext
# RUN pip install vext.gi

RUN ln -s /usr/lib/python3/dist-packages/gi/ /usr/local/lib/python3.7/site-packages/

# RUN pip install --ignore-installed PyGObject

# RUN cd /usr/local/lib/python3.8/site-packages/gi
# RUN sudo cp /usr/local/lib/python3.8/site-packages/gi_gi.cpython-37m-x86_64-linux-gnu.so /usr/local/lib/python3.8/site-packages/gi_gi.cpython-38m-x86_64-linux-gnu.so
# RUN cp _gi_cairo.cpython-35m-x86_64-linux-gnu.so _gi_cairo.cpython-38m-x86_64-linux-gnu.so

# command to run on container start
# CMD [ "python","./test.py"]
ENTRYPOINT ["python","./app.py"]
# CMD ["ls","/usr/local/lib/python3.8/site-packages/gi/","-all"]
