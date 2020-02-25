import cvnn.data_processing as dp
from utils import randomize
from cvnn.layers import ComplexDense
from cvnn.cvnn_model import CvnnModel
import tensorflow as tf
import numpy as np
from pdb import set_trace

if __name__ == "__main__":
    # monte_carlo_loss_gaussian_noise(iterations=100, filename="historgram_gaussian.csv")
    m = 10000
    n = 100
    num_classes = 2
    dataset = dp.CorrelatedGaussianNormal(m, n, num_classes, debug=False)
    x, y = dataset.get_all()
    x = x.astype(np.complex64)
    y = dp.sparse_into_categorical(y, num_classes=num_classes).astype(np.float32)
    x_train, y_train, x_test, y_test = dp.separate_into_train_and_test(x, y)
    x_train_real, x_test_real = dp.get_real_train_and_test(x_train, x_test)

    # Create complex network
    input_size = x.shape[1]  # Size of input
    output_size = y.shape[1]  # Size of output
    h1_size = 100
    h2_size = 40
    shape = [ComplexDense(input_size=input_size, output_size=h1_size, activation='cart_relu',
                          input_dtype=np.complex64, output_dtype=np.complex64),
             ComplexDense(input_size=h1_size, output_size=h2_size, activation='cart_relu',
                          input_dtype=np.complex64, output_dtype=np.complex64),
             ComplexDense(input_size=h2_size, output_size=output_size, activation='cart_softmax_real',
                          input_dtype=np.complex64, output_dtype=np.float32)]
    complex_network = CvnnModel(name="complex_network", shape=shape, loss_fun=tf.keras.losses.categorical_crossentropy,
                                verbose=True, tensorboard=True, save_csv_checkpoints=True)
    complex_network.fit(x_train, y_train, x_test, y_test, learning_rate=0.002, epochs=10)
    complex_network.plotter.plot_key(key='accuracy', library='plotly', name=complex_network.name)
    # Create real network   TODO: interesting to do a cast option like the deepcopy right?
    input_size *= 2
    h1_size *= 2
    h2_size *= 2
    shape = [ComplexDense(input_size=input_size, output_size=h1_size, activation='cart_relu',
                          input_dtype=np.float32, output_dtype=np.float32),
             ComplexDense(input_size=h1_size, output_size=h2_size, activation='cart_relu',
                          input_dtype=np.float32, output_dtype=np.float32),
             ComplexDense(input_size=h2_size, output_size=output_size, activation='cart_softmax_real',
                          input_dtype=np.float32, output_dtype=np.float32)]
    real_network = CvnnModel(name="real_network", shape=shape, loss_fun=tf.keras.losses.categorical_crossentropy,
                             verbose=True, tensorboard=True, save_csv_checkpoints=True)

    # Train both networks
    real_network.fit(x_train_real, y_train, x_test_real, y_test, learning_rate=0.002)
    real_network.plotter.plot_key(key='accuracy', library='plotly', name=real_network.name)

__author__ = 'J. Agustin BARRACHINA'
__version__ = '0.0.15'
__maintainer__ = 'J. Agustin BARRACHINA'
__email__ = 'joseagustin.barra@gmail.com; jose-agustin.barrachina@centralesupelec.fr'
