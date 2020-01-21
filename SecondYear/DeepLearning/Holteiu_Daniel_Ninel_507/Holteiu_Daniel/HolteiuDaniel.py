import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.optimizers import Adam, SGD
from keras.utils import to_categorical
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sn
import matplotlib.pyplot as plt


def load_data(train_data, path_to_image):
    print("Loading data")
    features = []
    labels = []

    for line in train_data:
        line = line[:-1].split(",")
        id = line[0]
        label = int(line[1])
        labels.append(label)

        # Use opencv to read the images. No preprocessing is done on the images
        img = cv2.imread(path_to_image.format(id))
        features.append(img)

    # Transform the training data into numpy arrays
    features = np.array(features, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    # Transform label to categorical
    labels = to_categorical(labels)

    print("Data loaded!")

    return features, labels


def create_model(data_shape):
    # There are 2 classes
    n_classes = 2

    # The model is a Sequential model
    model = Sequential()

    # First layer is a Convolutional 2D layer and has 128 filters, with a kernel size of (7, 7)
    # and the activation function of the layer is "RELU"
    model.add(Conv2D(128, (7, 7), activation='relu', input_shape=data_shape))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())
    # A max pooling 2D is being done on this layer. The pool size is the default (2, 2)
    model.add(MaxPooling2D())

    # Second layer is a Convolutional 2D layer and has 64 filters, with a kernel size of (6, 6)
    # and the activation function of the layer is "RELU"
    model.add(Conv2D(64, (6, 6), activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())
    # A max pooling 2D is being done on this layer. The pool size is the default (2, 2)
    model.add(MaxPooling2D())

    # Third layer is a Convolutional 2D layer and has 32 filters, with a kernel size of (5, 5)
    # and the activation function of the layer is "RELU"
    model.add(Conv2D(32, (5, 5), activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())
    # A max pooling 2D is being done on this layer. The pool size is the default (2, 2)
    model.add(MaxPooling2D())

    # Fourth layer is a Convolutional 2D layer and has 16 filters, with a kernel size of (4, 4)
    # and the activation function of the layer is "RELU"
    model.add(Conv2D(16, (4, 4), activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())
    # A max pooling 2D is being done on this layer. The pool size is the default (2, 2)
    model.add(MaxPooling2D())

    # Fifth layer flattens the data
    model.add(Flatten())

    # Sixth layer is a Dense layer with 512 units and the activation function of the layer is "RELU"
    model.add(Dense(512, activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())

    # Seventh layer is a Dense layer with 256 units and the activation function of the layer is "RELU"
    model.add(Dense(256, activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())

    # Eighth layer is a Dense layer with 256 units and the activation function of the layer is "SIGMOID"
    model.add(Dense(256, activation='sigmoid'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())

    # Ninth layer is a Dense layer with 128 units and the activation function of the layer is "RELU"
    model.add(Dense(128, activation='relu'))
    # A Batch normalization is being done on this layer
    model.add(BatchNormalization())

    # The last layer is a Dense layer with 2 units (the categorical labels) and activation function of the layer is "SOFTMAX"
    model.add(Dense(n_classes, activation='softmax'))

    # The learning rate of the model is 0.0001
    learning_rate = 1e-4
    # The optimizer of the model is an ADAM optimizer
    adam = Adam(lr=learning_rate)
    model.compile(loss='binary_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])

    return model


def train_model(model, features, labels):
    # Train the model for 15 epochs
    # And a batch size of 64 values
    epochs = 15
    batch_size = 64
    fit = model.fit(features, labels, epochs=epochs, batch_size=batch_size)

    return model


def predict_for_submission_data(model, path_to_image):
    print("Start predicting")
    f = open("submission.txt", "w")
    f.write("id,class\n")
    for i in range(17001, 22150):
        id = "0" + str(i)
        img = cv2.imread(path_to_image.format(id))
        prediction = model.predict(np.array([img], dtype=np.float32))

        prediction = prediction[0]
        if prediction[0] > prediction[1]:
            prediction = 0
        else:
            prediction = 1
        f.write("{},{}\n".format(id, prediction))

    f.close()
    print("Predictions complete")


def cross_validation(n_split, features, labels):
    print("Starting {}-Fold Cross Validation!".format(n_split))
    results = []
    index = 1
    # Split the data into 3 equal parts
    for train_index, test_index in KFold(n_split, shuffle=True).split(features):
        model = create_model(tuple(features.shape[1:]))
        # Train the model on 2 parts
        trained_model = train_model(model, features[train_index], labels[train_index])
        res.append(model.evaluate(features[test_index], labels[test_index]))

        # Test the model on the 3rd remaining part
        y_pred = model.predict(features[test_index])
        # Get argmax for the class
        y_pred = np.argmax(y_pred, axis=1)
        y_expected = np.argmax(labels[test_index], axis=1)

        # Create the confusion matrix
        cm = confusion_matrix(y_expected, y_pred)

        # Plot and save the confusion matrix
        plt.figure(index)
        heatmap_plot = sn.heatmap(cm, annot=True)
        heatmap_plot.get_figure().savefig("confusion_matrix_{}.png".format(index))
        plt.show()

        index = index + 1
    # The results of the model. It will contain 3 arrays with 2 values each. The first value is the loss value
    # and the second one is the Accuracy of the model
    print("Results: " + results)
    print("Cross validation completed!")


# The code ran on google colab. The data was exported to Google Drive.
if __name__ == "__main__":
    # path_to_image = "/content/drive/My Drive/DataForMlMasterSecondYear/data/data/{}.png" # An example of path to Google Drive
    path_to_image = "path/to/data/directory/data/data/{}.png"
    # path_to_train_data = "/content/drive/My Drive/DataForMlMasterSecondYear/train_labels.txt" # An example of path to Google Drive
    path_to_train_data = "path/to/train/data/labels/train_labels.txt"

    train_data = open(path_to_train_data)
    train_data.readline() # read the header

    # Train and predict only for submission
    features, labels = load_data(train_data, path_to_image)  # load the images and the labels
    model = create_model(tuple(features.shape[1:]))  # create model to be trained
    trained_model = train_model(model, features, labels)  # train the model
    predict_for_submission_data(model, path_to_image)  # write to file the submission data
    train_data.close()

    # Cross validation
    cross_validation(3, features, labels)



