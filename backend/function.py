
import tflite_runtime.interpreter as tflite
import cv2
import numpy as np
import os
import glob
from backend.lib import FaceDetection, FaceRecognition


model_path = "./models/mobileNet.tflite"
detector = FaceDetection()
recognizer = FaceRecognition()


def get_emb(gal_dir):
    gal_embs = []
    gal_names = []
    gal_faces = []

    files = glob.glob("{}/*.jpg".format(gal_dir)) + glob.glob("{}/*.png".format(gal_dir))
    for file in files:
        img = cv2.imread(file)
        detections = detector.detect_faces(img)  
        _, points, _ = detections[0]  
        gal_names.append(os.path.basename(file).split(".")[0])
        face = detector.get_face(img, points)
        gal_faces.append(
            cv2.cvtColor(face.astype(np.float32) / 255, cv2.COLOR_BGR2RGB)
        ) 

    input_ = np.asarray(gal_faces)


    face_recognizer = tflite.Interpreter(model_path)
    input_details = face_recognizer.get_input_details()
    output_details = face_recognizer.get_output_details()


    face_recognizer.resize_tensor_input(input_details[0]["index"], input_.shape)
    face_recognizer.allocate_tensors()
    face_recognizer.set_tensor(input_details[0]["index"], input_)
    face_recognizer.invoke()

    res = [face_recognizer.get_tensor(elem["index"]) for elem in output_details]
    gal_embs = res[0]

    return gal_embs,gal_names,gal_faces



def recognize_faces(gal_dir,img):
			gal_embs,gal_names,gal_faces = get_emb(gal_dir)
			detections = detector.detect_faces(img) 
			if not detections:
				return []
			faces = []
			for detection in detections:
				bbox, points, conf = detection
				face = detector.get_face(img, points)
				faces.append(cv2.cvtColor(face.astype(np.float32) / 255, cv2.COLOR_BGR2RGB))
			embs = recognizer.get_emb(np.asarray(faces))[0]  # RGB float32 [0..1]
			ids = []
			for i in range(embs.shape[0]):
				pred, dist, conf = recognizer.identify(np.expand_dims(embs[i], axis=0), gal_embs, thresh=0.6)
				ids.append(
					[
						gal_names[pred] if pred is not None else "Other",
						cv2.cvtColor(gal_faces[pred] * 255, cv2.COLOR_RGB2BGR) if pred is not None else None,
						dist,
						conf,
					]
				)
			faces_ = []
			for face in faces:
				faces_.append(cv2.cvtColor(face * 255, cv2.COLOR_RGB2BGR))
			out = [i for i in zip(faces_, detections, ids)]
			return out

	








