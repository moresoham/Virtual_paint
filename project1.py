import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fwidth = 640
fheight = 480

cap.set(3,fwidth)
cap.set(4,fheight)
#cap.set(10,150) # brightness


# list of values for colors
mycolors = [[5,107,0,19,255,255],
			[133,56,0,159,156,255],
			[57, 76, 0, 100, 255, 255]]
#bgr
mycolorvalues = [[51,153,255],[255,0,255],[0,255,0]] # orange, purple, green

mypts = []  #[x, y, colorid]


# find color
def findcolor(img, mycolors, mycolorvalues):
	count = 0
	newpoints = []
	imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	for colors in mycolors:
		lower = np.array(colors[0:3])
		upper = np.array(colors[3:6])
		mask = cv2.inRange(imghsv, lower ,upper)
		x,y = getContours(mask)
		cv2.circle(imres, (x,y), 10, mycolorvalues[count], cv2.FILLED)
		if x!=0 and y!=0:
			newpoints.append([x,y,count])
		count+=1
		#cv2.imshow(str(colors[0]), mask)
	return newpoints

def getContours(img):
	contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #(src_img, retrival_method)
	x,y,w,h = 0,0,0,0
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area > 500 :
			cv2.drawContours(imres, cnt, -1, (255,0,0), 3)

			# find corner points
			perimeter = cv2.arcLength(cnt, True)
			approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)

			# find object corners,  create bounding boxes
			x, y , w, h = cv2.boundingRect(approx)
	return x+w//2, y

def draw(mypts, mycolorvalues):
	for pt in mypts:
		cv2.circle(imres, (pt[0],pt[1]), 10, mycolorvalues[pt[2]], cv2.FILLED)

while True:
	success,vdo = cap.read()
	imres = vdo.copy()
	newpoints = findcolor(vdo,mycolors,mycolorvalues)
	if len(newpoints) != 0:
		for newpt in newpoints:
			mypts.append(newpt)

	if len(mypts)!=0:
		draw(mypts, mycolorvalues)
		
	cv2.imshow("Res", imres)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break