#!/usr/bin/env python3

# Train multiple images per person
# Find and recognize faces in an image using a SVC with scikit-learn

"""
Structure:
        <test_image>.jpg
        <train>/
            <person_1>/
                <person_1_face-1>.jpg
                <person_1_face-2>.jpg
                .
                .
                <person_1_face-n>.jpg
           <person_2>/
                <person_2_face-1>.jpg
                <person_2_face-2>.jpg
                .
                .
                <person_2_face-n>.jpg
            .
            .
            <person_n>/
                <person_n_face-1>.jpg
                <person_n_face-2>.jpg
                .
                .
                <person_n_face-n>.jpg
"""

import face_recognition
from sklearn import svm
import os
import numpy as np
import pickle

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Training the SVC classifier

# The training data would be all the face Encodings from all the known images and the labels are their Names
Encodings = []
Names = []
tolerance=0.6

# Training directory
train = os.listdir('./train/')

# Loop through each person in the training directory
for person in train:
    pix = os.listdir("./train/" + person)
    print(pix)

    # Loop through each training image for the current person
    for person_img in pix:
        # Get the face Encodings for the face in each image file
        face = face_recognition.load_image_file("./train/" + person + "/" + person_img)

        # Default for model is HOG and execute with CPU -> fast
        # face_locations = face_recognition.face_locations(face)
        face_locations = face_recognition.face_locations(face, model="hog")
        
        # For model is CNN and execute with GPU NVIDIA CUDA -> slow
        # face_locations = face_recognition.face_locations(face, model="cnn")
        

        #If training image contains exactly one face
        if len(face_locations) == 1:
            # face_enc = face_recognition.face_encodings(face)[0]
            face_enc = face_recognition.face_encodings(face, face_locations)[0]

            # Add face encoding for current image with corresponding label (name) to the training data
            Encodings.append(face_enc)
            Names.append(person)
        else:
            print(person + "/" + person_img + " was skipped and can't be used for training")
print(Names)

with open('face_recognition_hog.pkl', 'wb') as f:
	pickle.dump(Names, f)
	pickle.dump(Encodings, f)
	print('training finished!')
    #f.close()

