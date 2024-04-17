import cv2
import mediapipe as mp
import win32api
import win32con

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
frame_h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frame_w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    cv2.flip(frame,1,frame)
    mouse_x, mouse_y = win32api.GetCursorPos()
    #     #wykrywanie twarzy
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray_frame, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #wykrywanie twarzy w obszarze i dzialanie
        if x+w < int(frame_w/3)  and (y > int(frame_h/3) and y+h < int(2*frame_h/3)):
            win32api.SetCursorPos((mouse_x-2, mouse_y )) #w lewo

        elif x > int(2*frame_w/3) and (y > int(frame_h/3) and y+h < int(2*frame_h/3)):
            win32api.SetCursorPos((mouse_x+2, mouse_y )) #w prawo
                
        elif (x > int(frame_w/3) and x+w < int(2*frame_w/3)) and y+h < int(frame_h/3):
            win32api.SetCursorPos((mouse_x, mouse_y-2 )) #w gore
                
        elif (x > int(frame_w/3) and x+w < int(2*frame_w/3)) and y > int(2*frame_h/3):
            win32api.SetCursorPos((mouse_x, mouse_y+2 )) #w dol
          
        else:
            next

        #wykrywanie dłoni
    lmx = []
    lmy = []
    
    with mp_hands.Hands(static_image_mode=False, 
                        model_complexity=1, 
                        min_detection_confidence=0.75, 
                        min_tracking_confidence=0.75, 
                        max_num_hands=1 ) as hands:
        process_frames = hands.process(frame)

    if process_frames.multi_hand_landmarks:
        
            for lm in process_frames.multi_hand_landmarks:
                for lm in process_frames.multi_hand_landmarks:
                    for i in range(21):
                        lmy.append((lm.landmark[i].y) *frame_h) 
                        lmx.append((lm.landmark[i].x) *frame_w) 
            
            up = int(min(lmy))
            down = int(max(lmy))
            left = int(min(lmx))
            right = int(max(lmx))
            top_left = (left, up)
            bottom_right = (right, down)
            
            cv2.rectangle(frame,top_left, bottom_right, (255,0,0), 2)
                
            #wykrywanie dłoni w obszarze i działanie
            if right < int(frame_w/3) and down < int(frame_h/3):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) #lewy gorny rog klik lewy przycisk
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
         
            elif left > int(2*frame_w/3) and down < int(frame_h/3):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0) #prawy gorny rog klik prawy przycisk
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
                      
            elif right < int(frame_w/3) and up > int(2*frame_h/3):
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) #lewy dolny rog klik lewy przycisk
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

            elif left > int(2*frame_w/3) and up > int(2*frame_h/3):
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0) #prawy dolny rog klik prawy przycisk
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0) 
                
            else:
                next
            
        #wyswietlanie linii obszarow
    cv2.line(frame, (int(frame_w/3),0), (int(frame_w/3),int(frame_h)), (0,0,255), 2)
    cv2.line(frame, (int(2*frame_w/3),0), (int(2*frame_w/3),int(frame_h)), (0,0,255), 2)
    cv2.line(frame, (0,int(frame_h/3)), (int(frame_w),int(frame_h/3)), (0,0,255), 2)
    cv2.line(frame, (0,int(2*frame_h/3)), (int(frame_w),int(2*frame_h/3)), (0,0,255), 2)
        
   
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
