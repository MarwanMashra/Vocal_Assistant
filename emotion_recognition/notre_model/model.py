import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, BatchNormalization, Conv2D, MaxPool2D
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

model = Sequential(
    [
        Conv2D(32, 3, input_shape=(48, 48, 1), padding='SAME', activation='relu'),
        BatchNormalization(),
        Conv2D(32, 3, padding='SAME',activation='relu'),
        BatchNormalization(),
        MaxPool2D(pool_size=(2, 2), strides=2),

        Conv2D(64, 3, padding='SAME',activation='relu'),
        BatchNormalization(),
        Conv2D(64, 3, padding='SAME',activation='relu'),
        BatchNormalization(),
        MaxPool2D(pool_size=(2, 2), strides=2),
        Dropout(0.25),

        Conv2D(128, 3, padding='SAME',activation='relu'),
        BatchNormalization(),
        Conv2D(128, 3, padding='SAME',activation='relu'),
        BatchNormalization(),
        MaxPool2D(pool_size=(2, 2), strides=2),
        Dropout(0.25),

        Flatten(),

        Dense(256,activation='relu'),
        BatchNormalization(),
        Dropout(0.5),

        Dense(256,activation='relu'),
        BatchNormalization(),
        Dropout(0.5),

        Dense(256,activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        
        Dense(7,activation='softmax')
    ]
) 

model.compile(loss='categorical_crossentropy',optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), metrics=['accuracy'])

pickle_in = open("data/X.pickle","rb")
X = np.array(pickle.load(pickle_in))
X = X/255.0
pickle_in = open("data/y.pickle","rb")
y = np.array(pickle.load(pickle_in))

X_train, X_valid, y_train, y_valid= train_test_split(X,y,test_size=0.1)

model.fit(X_train, y_train, batch_size=32, epochs=30)

model.save('data/model.h5')

val_loss, val_acc = model.evaluate(X_valid, y_valid)
print("val_loss : "+str(val_loss))
print("val_acc : "+str(val_acc))

"""
1: Epoch 1/10
1010/1010 [==============================] - 774s 766ms/step - loss: 2.9293 - accuracy: 0.1883

2:Epoch 1/10
1010/1010 [==============================] - 831s 816ms/step - loss: 2.1144 - accuracy: 0.2227

3: Epoch 1/10
1010/1010 [==============================] - 791s 772ms/step - loss: 2.4010 - accuracy: 0.2036

val_loss : 1.1818501949310303
val_acc : 0.6270902752876282
"""