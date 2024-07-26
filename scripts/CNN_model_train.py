#%%
#################################################################################
# Step 1. GPU setting ###########################################################
#################################################################################
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
import pickle
from tensorflow.python.client import device_lib


# print(device_lib.list_local_devices())
# # os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# devices = [0]
# gpus = tf.config.list_physical_devices("GPU")
# visible_gpus = [gpus[i] for i in devices]
# tf.config.set_visible_devices(visible_gpus, "GPU")



#%%
#################################################################################
# Step 2. Load the dataset ######################################################
#################################################################################
def _parse_function(proto):
    # Define the feature description
    feature_description = {
        'feature': tf.io.FixedLenFeature([6000], tf.float32),  # Feature as a 1D array with 6000 elements
        'label': tf.io.FixedLenFeature([5], tf.float32),     # Label as a 1D array with 50 elements
    }
    # Parse the input tf.train.Example proto using the feature description
    parsed_features = tf.io.parse_single_example(proto, feature_description)
    
    # Extract the features and labels directly without reshaping
    feature = parsed_features['feature']
    label = parsed_features['label']

    return feature, label
# Paths to your TFRecord files

train_tfrecord_files = ['./preprocessed_60s_{}.tfrecord'.format(i) for i in range(4)]
val_tfrecord_files = ['./preprocessed_60s_{}.tfrecord'.format(i) for i in range(4,5)]
# Create TFRecordDataset
train_dataset = tf.data.TFRecordDataset(train_tfrecord_files)
val_dataset = tf.data.TFRecordDataset(val_tfrecord_files)
# Map the parsing function to the dataset
train_dataset = train_dataset.map(_parse_function)
val_dataset = val_dataset.map(_parse_function)
# Set the batch size and prefetch
batch_size = 100
train_dataset = train_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)

# # Some dense layers for classification
# model.add(layers.Dense(512, activation='relu'))
# model.add(layers.Dropout(0.4))
# model.add(layers.Dense(256, activation='relu'))
# model.add(layers.Dropout(0.4))
# model.add(layers.Dense(50, activation='softmax'))
# # Compile the model
# opt = Adam(learning_rate=0.0001)
# model.compile(optimizer=opt,
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
# # Print the model summary
# model.summary()


def cnn_model_1d(input_length):
    # Input Layer
    input = layers.Input(shape=(input_length, 1), name='Input')

    # Normalize Input
    normalization = layers.Lambda(lambda x: x / 7500000.00)(input)

    # Convolution Layer
    conv1 = layers.Conv1D(filters=150, kernel_size=40, strides=1, padding='valid',
                          use_bias=True, activation=None)(normalization)
    conv1 = layers.BatchNormalization()(conv1)
    conv1 = layers.LeakyReLU()(conv1)
    conv1 = layers.Dropout(rate=0.4)(conv1)  # Dropout added here
    max1 = layers.AveragePooling1D(pool_size=10)(conv1)

    conv2 = layers.Conv1D(filters=150, kernel_size=40, strides=1, padding='valid',
                          use_bias=True, activation=None)(max1)
    conv2 = layers.LeakyReLU()(conv2)
    conv2 = layers.BatchNormalization()(conv2)
    conv2 = layers.Dropout(rate=0.4)(conv2)  # Dropout added here
    max2 = layers.AveragePooling1D(pool_size=10)(conv2)

    flat = layers.Flatten()(max2)

    dense_1 = layers.Dense(units=128, activation='relu')(flat)
    dense_2 = layers.Dropout(rate=0.4)(dense_1)
    dense_3 = layers.Dense(units=128, activation='relu')(dense_2)
    dense_4 = layers.Dropout(rate=0.4)(dense_3)

    outputs = layers.Dense(units=5, activation='softmax')(dense_4)

    model = models.Model(inputs=input, outputs=outputs)
    return model

# Create the model with 1D input
model = cnn_model_1d(input_length=6000)
print(model.summary())

# Compile the model
opt = Adam(learning_rate=0.01)
model.compile(optimizer=opt,
              loss='categorical_crossentropy',
              metrics=['accuracy'])
#%%
#################################################################################
# Step 4. Train the model #######################################################
#################################################################################
history = model.fit(train_dataset, epochs=5, validation_data=val_dataset) 

 #%%
#################################################################################
# Step 5. Save the model and history ############################################
#################################################################################
import pickle
with open('history_SA_90s.pkl', 'wb') as f:
    pickle.dump(history, f)
# save the model
model.save('VF_model_SA_90s.keras')


# #%%
# # #################################################################################
# # # Step 6. Load the saved model and do additional training #######################
# # #################################################################################
# import tensorflow as tf
# import pickle
# # Load the model
# model = tf.keras.models.load_model('VF_model_SA.h5')
# # Compile the model
# opt = Adam(learning_rate=0.0001)
# model.compile(optimizer=opt,
#               loss='categorical_crossentropy',
#               metrics=['accuracy'])
# # Load the previous history
# with open('history_SA.pkl', 'rb') as file:
#     history = pickle.load(file)
# # Continue training and get new history
# new_history = model.fit(train_dataset, epochs=10, validation_data=val_dataset)
# # Update history
# for key in history.keys():
#     history[key].extend(new_history.history[key])
# # Save the updated history
# with open('history_SA_updated.pkl', 'wb') as file:
#     pickle.dump(history, file)
# # Save the updated model
# model.save('VF_model_SA_updated.h5')



#%%
#################################################################################
# Step 7. Draw the history figure ###############################################
#################################################################################
# import matplotlib.pyplot as plt
# import pickle
# # Load the pickle file
# with open('history_SA_60s.pkl', 'rb') as f:
#     history = pickle.load(f)
# # Plotting the training and validation loss
# plt.figure(figsize=(12, 4))
# plt.subplot(1, 2, 1)
# plt.plot(history['loss'], label='Training Loss')
# plt.plot(history['val_loss'], label='Validation Loss')
# plt.legend()
# plt.title('Loss')
# # Plotting the training and validation accuracy
# plt.subplot(1, 2, 2)
# plt.plot(history['accuracy'], label='Training Accuracy')
# plt.plot(history['val_accuracy'], label='Validation Accuracy')
# plt.legend()
# plt.title('Accuracy')
# # Print the figure.
# plt.tight_layout()
# plt.show()
