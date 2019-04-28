# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 14:11:54 2019

@author: divya
"""

from imageai.Detection import ObjectDetection
import os


execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
imagename="7691332970_b05c77bdd0_o.jpg"
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , imagename), output_image_path=os.path.join(execution_path , imagename))

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )