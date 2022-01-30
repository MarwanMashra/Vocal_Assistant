How to run 
===============
1. Download [Tensorflow](https://files.pythonhosted.org/packages/70/dc/e8c5e7983866fa4ef3fd619faa35f660b95b01a2ab62b3884f038ccab542/tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl) and put it in emotion_recognition without changing its name. It should give :
    ```
    
    TER_S6
    │
    |─── emotion_recognition
    │   │---tensorflow-2.4.1-cp37-cp37m-manylinux2010_x86_64.whl

    ```
2. Install packages with 
    ```

    $ pip install -r requirements.txt

    ````
3. Make sure **Docker Desktop** is running. If you donn't have it yet, you can install it from [here](https://docs.docker.com/get-docker/)

4. Create docker images by running
    ```

    $ docker-compose -f ./docker-compose/docker-compose-x86.yml -p app build

    ````
5. Finally, start the app with 
    ```

    $ python ./main.py

    ```




