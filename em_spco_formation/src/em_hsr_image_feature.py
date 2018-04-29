#! /usr/bin/env python

from __init__ import *

import glob
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import caffe

class GetImageFeature(object):

    # callback for word recognition
    def sycle_callback(self, hoge):

        scores = self.net.predict([self.frame])
        feat = self.net.blobs[self.layer].data
        prediction = zip(scores[0].tolist(), self.categories)
        
        feat = np.average(feat,axis=0)
        fw = open(self.IMAGE_FOLDER + "/feature_vector/" + str(hoge.data) + ".txt",'w')
        for rank in xrange(len(feat)):
            fw.write('%d %d\n' % (rank, feat[rank]*100))
        fw.close()
        prediction.sort(cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)

        fw=open(self.IMAGE_FOLDER + "/feature_rank/" + str(hoge.data) + ".txt",'w')
        for rank, (score, name) in enumerate(prediction[:1000], start=1):
            fw.write('#%d | %s | %4.1f%% \n' % (rank, name, score * 100))
        fw.close()

        image_name = self.IMAGE_FOLDER + "/image/" + str(hoge.data) + ".jpg"
        cv2.imwrite(image_name, self.frame)
        print "[GetImageFeature] save new image as " + image_name

    # hold image
    def image_callback(self, image):

        bridge = CvBridge()
        try:
            self.frame = bridge.imgmsg_to_cv2(image, "bgr8")
        except CvBridgeError, e:
            print e

    def __init__(self):

        rospy.Subscriber(IMAGE_TOPIC, Image, self.image_callback, queue_size=1)
        rospy.Subscriber("/em/spco_formation/sycle", Int32, self.sycle_callback, queue_size=1)

        self.IMAGE_FOLDER = DATASET_FOLDER + TRIALNAME
        
        self.categories = np.loadtxt("../caffe/data/ilsvrc12/synset_words.txt", str, delimiter="\t")
        self.MEAN_FILE = '../caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy'
        self.MODEL_FILE = "../caffe/models/bvlc_reference_caffenet/deploy.prototxt"
        self.PRETRAINED = "../caffe/models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"
        self.layer = 'prob' #'fc6wi'

        self.net = caffe.Classifier(self.MODEL_FILE, self.PRETRAINED)
        caffe.set_mode_cpu()
        self.net.transformer.set_mean('data', np.load(self.MEAN_FILE))
        self.net.transformer.set_raw_scale('data', 255)
        self.net.transformer.set_channel_swap('data', (2,1,0))

if __name__ == '__main__':

    rospy.init_node('GetImageFeature', anonymous=True)
    hoge = GetImageFeature()
    rospy.spin()
