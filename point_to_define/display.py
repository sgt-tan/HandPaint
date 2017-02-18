import cv2
from draw_frame import DrawFrame
#from paper_detection import PaperDetection
from hand_detection import HandDetection
import numpy as np
from gesture import gesture_rec
import time

def loop(output_video):
	camera = cv2.VideoCapture(0)
	if output_video != None:
		fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
		video = cv2.VideoWriter(output_video, fourcc, 20, (711,800))
		record_video = True
	else:
		record_video = False	
	
	df = DrawFrame()
	#pd = PaperDetection()
	hd = HandDetection()

	prev_point = None
	curr_point = None
	point_buffer = []
	curr_time = 0
	prev_time = 0
	time_diff = 0
	img = None

	while True:
		# get frame
		(grabbed, frame_in) = camera.read()

		# original frame
		frame_orig = frame_in.copy()

		# shrink frame
		frame = df.resize(frame_in)

		# flipped frame to draw on

		frame_final = df.flip(frame)

		#code commented: functionality disabled
		# click p to train paper
		#if cv2.waitKey(1) == ord('p') & 0xFF:
		#	if not pd.trained_paper:
		#		pd.train_paper(frame)
		#		pd.set_paper(frame)
		#		pd.set_ocr_text(frame_orig)
		# click h to train hand
		if cv2.waitKey(1) == ord('a') & 0xFF:
		#	if pd.trained_paper and not hd.trained_hand:
			if not hd.trained_hand:
				hd.train_hand(frame)
				print "hand train debug point"
		#click q to quit 
		if cv2.waitKey(1) == ord('q') & 0xFF:
		 	break	

		if cv2.waitKey(1) == ord('s') & 0xFF:
			cv2.imwrite('result.jpg',img)
			#cv2.SaveImage('result.jpg',img)
			break

		# create frame depending on trained status
		'''
		if not pd.trained_paper:
			frame_final = pd.draw_paper_rect(frame_final)
		elif pd.trained_paper and not hd.trained_hand:
			frame_final = hd.draw_hand_rect(frame_final)
		elif pd.trained_paper and hd.trained_hand:
			frame_final = df.draw_final(frame_final, pd, hd)
		'''
		count=0

		img = np.zeros((512,512,3), np.uint8)
		img = img+255

		#replace previous and next and use a list. Last added element 
		# would be accessed 

		#code fix to redraw using previous points
		#realised need for a buffer for continuous drawing which
		#hence commented
		'''
		if not hd.trained_hand:
			frame_final= hd.draw_hand_rect(frame_final)
		elif hd.trained_hand:
			count = count+1
			curr_point, frame_final = df.draw_final(frame_final, hd)
			if count<1:
				prev_point = curr_point
			else:
				img = cv2.line(img,prev_point,curr_point,(255,225,0),5)
				cv2.imshow('disp',img)
				print prev_point,"  ",curr_point
				prev_point = curr_point
		
		'''
		#check the number of contours and select - draw | abort| stop draw



		i =1
		j =0

		if not hd.trained_hand:
			frame_final = hd.draw_hand_rect(frame_final)
		elif hd.trained_hand:
			num_defects, curr_point, frame_final = df.draw_final(frame_final, hd)
			if num_defects<=3:
				point_buffer.append(curr_point)
				while i < len(point_buffer):
					img = cv2.line(img,point_buffer[j],point_buffer[i],(0,0,0),5)
					cv2.imshow('disp',img)
					j+=1
					i+=1
		
			'''
			elif num_defects >= 4:
				curr_time = time.time()
				time_diff = time_diff + curr_time-prev_time
				prev_time = curr_time
				if time_diff > 10:
					cv2.imwrite('result.jpg',img)
					cv.SaveImage('result.jpg',img)
					break
			'''



		
		# record frame
		if record_video:
			video.write(frame_final)	

		# display frame	
		
		cv2.imshow('image', frame_final)			 	
		#cv2.imwrite('result.jpg',img)

	# cleanup
	if record_video:
		video.release()
	camera.release()
	cv2.destroyAllWindows()				
