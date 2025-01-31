import cv2
import imutils
import sys
from imutils.video import FPS
from imutils.video import WebcamVideoStream

# dict containing different Tracker types
OPENCV_OBJECT_TRACKERS={
	"csrt":cv2.legacy.TrackerCSRT_create,
	"kcf":cv2.legacy.TrackerKCF_create,
	"boosting":cv2.legacy.TrackerBoosting_create,
	"mil":cv2.legacy.TrackerMIL_create,
	"tld":cv2.legacy.TrackerTLD_create,
	"medianflow":cv2.legacy.TrackerMedianFlow_create,
	"mosse":cv2.legacy.TrackerMOSSE_create,
	"goturn":cv2.TrackerGOTURN_create
}

print(OPENCV_OBJECT_TRACKERS.keys())
print("For GOTURN you are required to download GOTURN model files")
tracker_inp=input("Which tracker would you like to use? ")

multiTracker=cv2.legacy.MultiTracker_create()

#inititalize
bboxes=[]
k=cv2.waitKey(1) & 0xFF
tracker_objects=[]
vs=WebcamVideoStream(src=0).start()
#video_stream=cv2.VideoCapture(0)
fps=FPS().start()

# def rectangles(boundingBox):
# 				#cv2.rectangle(frame,(int(boundingBox[0,0],int(boundingBox[0,1]))),
# 				#(int(boundingBox[0,0]+boundingBox[0,2]),int(boundingBox[0,1]+boundingBox[0,3])),
# 				#(127,255,0),2)
# 				print(boundingBox[0])
# 				cv2.rectangle(frame,(int(boundingBox[0],int(boundingBox[1]))),
# 				(int(boundingBox[0]+boundingBox[2]),int(boundingBox[1]+boundingBox[3])),
# 				(127,255,0),2)


while True:
	frame=vs.read()
	#resize the frame to process it faster
	frame=imutils.resize(frame,width=400)
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	if cv2.waitKey(1) & 0xFF==ord("s"):
		while True:		
			bbox=cv2.selectROI("MultiTracker",frame,fromCenter=False,
			showCrosshair=False)
			tracker=OPENCV_OBJECT_TRACKERS[tracker_inp]()
			tracker_objects.append(tracker)
			bboxes.append(bbox)
			print("Press q to quit selecting boxes and start tracking.")
			#if cv2.waitKey(1) & 0xFF==ord("b")
			if cv2.waitKey(0) & 0xFF==ord("q"):
				print("INSIDE IF CONDITION")
				break
	[(multiTracker.add(tracker_objects[b],frame,bboxes[b])) for b in range(len(bboxes))]
	(success,boundingBox)=multiTracker.update(frame)
	[cv2.rectangle(frame,(int(newbox[0]),int(newbox[1])),
			(int(newbox[0]+newbox[2]),int(newbox[1]+newbox[3])),(127,255,0),2)
			for i,newbox in enumerate(boundingBox)]
		

	cv2.imshow("MultiTracker",frame)
	fps.update()
	if cv2.waitKey(1) & 0xFF==ord("x"):
		break

	fps.stop()
print(f"ELAPSED TIME {fps.elapsed()}")
print(f"APPROX FPS {fps.fps()}")
cv2.destroyAllWindows()
vs.stop()
		