import tensorflow as tf

print(tf. __version__)

# Check that GPU is available: cf. https://colab.research.google.com/notebooks/gpu.ipynb
#assert(tf.test.gpu_device_name())

tf.keras.backend.clear_session()
tf.config.optimizer.set_jit(False) # Start with XLA disabled.

def load_data():
  (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
  x_train = x_train.astype('float32') / 256
  x_test = x_test.astype('float32') / 256

  # Convert class vectors to binary class matrices.
  y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
  y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
  return ((x_train, y_train), (x_test, y_test))

(x_train, y_train), (x_test, y_test) = load_data()

# gerar modelo
def generate_model():
  return tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(32, (3, 3)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Conv2D(64, (3, 3), padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(64, (3, 3)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Activation('softmax')
  ])

model = generate_model()

# optimizer: RMSprop
def compile_model(model):
  opt = tf.keras.optimizers.RMSprop(learning_rate=0.0001)
  model.compile(loss='categorical_crossentropy',
                optimizer=opt,
                metrics=['accuracy'])
  return model

model = compile_model(model)

def train_model(model, x_train, y_train, x_test, y_test, epochs=25):
  model.fit(x_train, y_train, batch_size=256, epochs=epochs, validation_data=(x_test, y_test), shuffle=True)

def warmup(model, x_train, y_train, x_test, y_test):
  # Warm up the JIT, we do not wish to measure the compilation time.
  initial_weights = model.get_weights()
  train_model(model, x_train, y_train, x_test, y_test, epochs=1)
  model.set_weights(initial_weights)

warmup(model, x_train, y_train, x_test, y_test)
train_model(model, x_train, y_train, x_test, y_test)

scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
