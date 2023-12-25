import tensorflow_hub as hub

# For running inference on the TF-Hub module.
import tensorflow as tf
import numpy as np


module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"

detector = hub.load(module_handle).signatures['default']