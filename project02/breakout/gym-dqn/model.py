import prettytensor as pt
import tensorflow as tf


class Model():
  def __init__(self):
    self.batch_size = 1

    input_data = tf.placeholder(tf.float32, [self.batch_size, 84, 84, 1])
    targets    = tf.placeholder(tf.float32, [self.batch_size, 1])

    self.lr_start = 0.01
    self.lr = self.lr_start
    self.lr_end = self.lr
    self.lr_endt = 1000000

    seq = pt.wrap(input_data).sequential()

    #reshape here
    seq.conv2d([8,8], 32, stride=8)
    seq.conv2d([4,4], 64, stride=4)
    seq.conv2d([3,3], 64, stride=1)
    seq.flatten()
    seq.fully_connected(512, activation_fn=tf.nn.relu)
    seq.softmax_classifier(1, targets)

#TODO check the model and compare with dm code before training
#https://github.com/google/prettytensor
