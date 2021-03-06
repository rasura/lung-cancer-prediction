import os
import tensorflow as tf

from utils import store_to_csv
import config

from model_utils import x, evaluate_test_set, evaluate_solution
from model_factory import ModelFactory


# Construct model
factory = ModelFactory()
model = factory.get_network_model()

softmax_prediction = tf.nn.softmax(model.conv_net(x, 1.0), 
    name='softmax_prediction')

data_loader = factory.get_data_loader()
test_set = data_loader.get_exact_tests_set()
out_dir = data_loader.results_out_dir()
print(out_dir)


saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    if os.path.exists(os.path.join(out_dir, config.RESTORE_MODEL_CKPT + '.index')):
        saver.restore(sess, os.path.join(out_dir, config.RESTORE_MODEL_CKPT))

        evaluate_test_set(sess, 
                          test_set,
                          softmax_prediction,
                          x)
        if os.path.exists(config.SOLUTION_FILE_PATH):
            print("Evaluate generated solution...")
            evaluate_solution(config.SOLUTION_FILE_PATH)
        else:
          print("Solution file was not generated, check if test data is complete...")
    else:
        print("Checkpoint file {} does not exist in the configured directory {}.".format(
            config.RESTORE_MODEL_CKPT, out_dir))

