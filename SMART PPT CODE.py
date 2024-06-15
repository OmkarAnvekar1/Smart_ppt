from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

width, height = 500,200 #This is completely for my image/video


folderPath = r"C:\Users\omkar\Downloads\ppt final part\MINOR 1 PPT"
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)



imgNumber=0
hs, ws = int(150 * 0.95), int(250 * 0.85)  #This one is completely for my slides size
gestureThreshold = 125
buttonPressed = False
buttonCounter = 0
buttonDelay = 30 #frames per second : this is the speed of the switching between 2 consecutive slides
# 30 fps = 1 seconds
annotations = [[]] # create LIST and go on appending
annotationNumber = 0
annotationStart = False #at starting(annotation) it is false, and when we will put a number it willl be trur



#hand detector

detector = HandDetector(detectionCon = 0.8 , maxHands=1)


while True:

    success, img = cap.read()
    img = cv2.flip(img, 1) # 1=horizontal, 0 = Vertical
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)
    #hand correct right/left
    #hands, img = detector.findHands(img,flipType=False) try this 
    hands, img = detector.findHands(img)
    
    
    # when presenting if suddenly a hand comes then it should not detect that random hand 
    # so we considered threshold
    
    cv2.line(img,(0, gestureThreshold),(width, gestureThreshold), (0,255,0),5)
    if hands and buttonPressed is False:#if hands detect get landmarks
    # if hands and buttonPressed is False:"buttonPressed is False"is just to avoid the quick triggering of the slides
        hand = hands[0]#just accept the 1st seen hand
        fingers = detector.fingersUp(hand)
       # print(fingers) # this will print my fingers coordinates [1,0,0,0,0]
        
        # if our centre of the hand is above threshold line then and only then we will 
        # accept our gestures
        cx, cy = hand['center']
        lmList = hand['lmList'] #landmark list
       # indexFinger =  lmList[8][0], lmList[8][1] - i
        
        #Constrain values for easier drawing 
        indexFinger =  lmList[8][0], lmList[8][1] # - ii
        xVal = int(np.interp(lmList[8][0],[width//2,w],[0,width]) )# ********** WARNING *********
        yVal = int(np.interp(lmList[8][1],[150,height-150],[0,height])) #EVEN THIS VALUE DEPENDS ON THE SCREEN RESOLUTION
        #in video value = height-150
        indexFinger = xVal,yVal
        
        
        
        
        
        if cy<=gestureThreshold: #check whether hand is at the height of the face
            annotationStart = False
            #gesture 1 - left
            if fingers == [1, 0, 0, 0, 0] :
                annotationStart = False
                print("left")
                
                if imgNumber > 0:
                    buttonPressed = True
                    #----------- this 3 lines i have put because when we draw in slide 1 and move to slide 2 the annotation marks should not appear in the slide 2
                    annotations = [[]] # create LIST and go on appending
                    annotationNumber = 0
                    annotationStart = False #at starting(annotation) it is false, and when we will put a number it willl be trur

                    imgNumber -= 1
                
            #gesture 2 - right
            if fingers == [0, 0, 0, 0, 1] :
                annotationStart = False #at starting(annotation) it is false, and when we will put a number it willl be trur
                print("right")
                
                if imgNumber < len(pathImages):
                    buttonPressed = True
                    #----------- this 3 lines i have put because when we draw in slide 1 and move to slide 2 the annotation marks should not appear in the slide 2
                    annotations = [[]] # create LIST and go on appending
                    annotationNumber = 0
                    
                     #-----------
                    imgNumber += 1
                    
            
            # here onwards start the drwaing part
            # gesture 3 - Add the pointer 
        if fingers == [0, 1, 1, 0, 0] :
             cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
             annotationStart = False
             
             # gesture 4 - Draw the pointed area when we have index finger
        if fingers == [0, 1, 0, 0, 0] :
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            
            
            
            cv2.circle(imgCurrent,indexFinger,12,(0,0,255),cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        
        else:
            annotationStart = False      
            
             # gesture 5 - The eraser
        if fingers == [0, 1, 1, 1, 0] :
            if annotations:
                annotations.pop(-1)#remove the last-one annotation
                annotationNumber -=1
                buttonPressed = True
                
    else:
        annotationStart = False
                     
    #button pressed iterations
    if buttonPressed: #45:10 
        buttonCounter +=1   
        if buttonCounter > buttonDelay :
            buttonCounter = 0
            buttonPressed = False
    
    
    for i in range (len(annotations)):#enumerate
        for j in range(len(annotations[i])):
            if j != 0:
       # if i != 0: # because to avoid -1, since i starts from 0
                 cv2.line(imgCurrent, annotations[i][j-1],annotations[i][j],(0,0,200),5)
         #to avoid the line between 2 cursor points
            
        
    
    
    
    #display webcam on slides as well - 1.resize the image
    imgSmall = cv2.resize(img,(ws,hs))
    h, w, _ = imgCurrent.shape
    #to get the TOP-Right corner to place my video on the slide
    imgCurrent[0:hs,w-ws:w] = imgSmall
    
    
  
    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)
   

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
