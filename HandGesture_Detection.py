import numpy as np
import cv2

def is_contour_bad(c):
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.03 * peri, True) 
	# the contour is 'bad' if it is not a rectangle
	return not len(approx) == 4

# Initlaize background subtractor
foreground_background = cv2.BackgroundSubtractorMOG()

def get_contour_areas(contours):
    # returns the areas of all contours as list
    all_areas = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        all_areas.append(area)
    return all_areas

cap = cv2.VideoCapture(0)
lower_purple = np.array([0,48,80])
upper_purple = np.array([20,255,255])
image = cv2.imread('paper_1.png')
template = cv2.resize(image, (640, 480), interpolation = cv2.INTER_AREA)
image = template
template  = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(template, (7, 7), 0)
ret, thresh1 = cv2.threshold(template, 127, 255, 1)
# Extract Contours
contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
template_contour = sorted_contours[0]      #to select the second largest image after the background
hull = cv2.convexHull(template_contour)
template_size = len(hull)

while True:
	ret, frame = cap.read()
	frame = cv2.bilateralFilter(frame, 9, 75, 75)
	 # Convert imagclee from RBG/BGR to HSV so we easily filter
	hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    	# Use inRange to capture only the values between lower & upper_blue
	mask = cv2.inRange(hsv_img, lower_purple, upper_purple)
    	# Perform Bitwise AND on mask and our original frame
	frame = cv2.bitwise_and(frame, frame, mask=mask)
	frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#gray = foreground_background.apply(gray)
	#gray = cv2.Canny(gray, 30, 200)
	ret, thresh = cv2.threshold(gray, 127, 255, 0)
	contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	shape_paper = "paper hand"
	shape_scissor = "scissor"
	shape_stone = "stone"
	cx = 0
	cy = 0
	for cnt in contours:
		if is_contour_bad(cnt) == False :	
			hull1 = cv2.convexHull(cnt)
			match = cv2.matchShapes(template_contour, cnt, 3, 0.0)    
			if (match < 0.15 ):
				cv2.drawContours(frame, [hull1], 0, (0, 255, 0), 3)
					M = cv2.moments(cnt)
					cx = int(M["m10"] / M["m00"])
					cy = int(M["m01"] / M["m00"])
					cv2.putText(frame, shape_paper, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

	cv2.imshow('matching', frame)
	if cv2.waitKey(1) == 13: #13 is the Enter Key
	 	break

cap.release()
cv2.destroyAllWindows()
