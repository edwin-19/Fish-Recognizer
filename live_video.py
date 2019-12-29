from __future__ import division, print_function, absolute_import

import cv2
import os 
from PIL import Image
import numpy as np 

from yolo import YOLO

from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from deep_sort.detection import Detection as ddet
from tools import generate_detections as gdet

# definition of the paramaters
max_cosine_distance = 0.3
nn_budget = None
nms_max_overlap = 1.0

# deep sort
model_filename = 'model_config/original/mars-small128.pb'
encoder = gdet.create_box_encoder(model_filename, batch_size=1)

metric = nn_matching.NearestNeighborDistanceMetric(
    "cosine", max_cosine_distance, nn_budget
)
tracker = Tracker(metric)

# YOLO Object
yolo = YOLO()

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    
    while True:
        frame = cap.read()[1]
        frame = cv2.flip(frame, 1)
        
        # You may need to convert the color.
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        
        boxs = yolo.detect_image_boxes(im_pil)
        # cv2.imshow('TEST', np.array(boxs)[:,:,::-1])
        features = encoder(frame, boxs)
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        
        # Run non-maxima suppression
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        
        # Call the tracker
        tracker.predict()
        tracker.update(detections)
        
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(track.track_id),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)
        
        for det in detections:
            bbox = det.to_tlbr()
            cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)
        
        cv2.imshow('Human Tracker', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # esc to quit
    
    cap.release()
    cv2.destroyAllWindows()
    yolo.close_session()