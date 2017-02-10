import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
import imutils


# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
 
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
 
	# initialize the list of picked indexes	
	pick = []
 
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
 
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
 
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
 
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
 
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
 
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
 
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")



def main():
	use_fast_nms = True
	use_cascade = False
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	cascade = cv2.CascadeClassifier('haarcascade_pedestrian.xml')

	vidCap = cv2.VideoCapture(0)
	while True:
		(flag, frame) = vidCap.read()
		# using hog descriptor + SVM
		if not use_cascade:
			frame = imutils.resize(frame, width=min(400, frame.shape[1]))
			(rects, weights) = hog.detectMultiScale(frame, scale=1.05, winStride=(4,4), padding=(8,8))
		else:
			#TODO: use cascade to find pedestrian
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			rects = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, minSize=(120, 120), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
		rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])
		# using fast nms or not
		if use_fast_nms:
			pick = non_max_suppression_fast(rects, overlapThresh=0.9)
		else:
			pick = non_max_suppression(rects, overlapThresh=0.65)
		for (xA, yA, xB, yB) in pick:
			cv2.rectangle(frame, (xA, yA), (xB, yB), (0,255,0), 2)
		cv2.imshow('nms test', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	vidCap.release()
	cv2.destroyAllWindows()

main()
