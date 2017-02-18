import cv2


def gesture_rec(img):
	crop_img = img[100:300, 100:300]
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	value = (35, 35)
	blurred = cv2.GaussianBlur(grey, value, 0)

    #threshholding the pixel values
	_, thresh1 = cv2.threshold(blurred, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #find contours
	image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
    		cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	cnt = max(contours, key = lambda x: cv2.contourArea(x))

	hull = cv2.convexHull(cnt)

	drawing = np.zeros(crop_img.shape,np.uint8)
	cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
	cv2.drawContours(drawing,[hull],0,(0,0,255),0)

	hull = cv2.convexHull(cnt,returnPoints = False)
	defects = cv2.convexityDefects(cnt,hull)
	count_defects = 0

	cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)


	for i in range(defects.shape[0]):
		s,e,f,d = defects[i,0]
		start = tuple(cnt[s][0])
		end = tuple(cnt[e][0])
		far = tuple(cnt[f][0])
		a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
		b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
		c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
		angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
		if angle <= 90:
			count_defects += 1
			cv2.circle(crop_img,far,1,[0,0,255],-1)
		#dist = cv2.pointPolygonTest(cnt,far,True)
		cv2.line(crop_img,start,end,[0,255,0],2)
		#cv2.circle(crop_img,far,5,[0,0,255],-1)

	if count_defects == 1:
		cv2.putText(img,"I am Aditya", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
	elif count_defects == 2:
		cv2.putText(img,"I am BARS", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

	return img

#convert images to gray
#blur the gray