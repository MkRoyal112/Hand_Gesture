# First we will load the Libraries for the Project:

import cv2 #cv2 is to open the webcam and capture the video frames of the system.
import mediapipe as mp #Mediapipe is a Google AI to detect the hand and its landmarks in the video frames.
import pyautogui #PyAutoGUI is a Python library that allows you to control the mouse and keyboard.
import math #Importing the math library to calculate the distance between the thumb and fingers.
import time #This is to add delay between actions to avoid multiple actions.

#Now we have all the things we need to run the project. Let's write the codes:

# PyAutoGUI Safety Setup
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.01

class MediaPipeGestureController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.cap = cv2.VideoCapture(0)
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Timers and States
        self.last_action_time = time.time()
        self.prev_palm_y = None
        
        # Create Window and Make it ALWAYS ON TOP (Tab switching fix)
        self.window_name = "MediaPipe Flawless Controller"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)

    def get_distance(self, p1, p2):
        return math.hypot(p2.x - p1.x, p2.y - p1.y)

    def run(self):
        print("[INFO] Starting MediaPipe Gesture Controller on Python 3.10...")
        print("[INFO] Window is pinned 'Always on Top'. Press 'q' to quit.")

        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                break
            
            # Mirror frame
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    lm = hand_landmarks.landmark
                    
                    # Core Landmarks
                    thumb_tip = lm[4]
                    index_tip = lm[8]
                    palm_base = lm[0]
                    
                    # Screen Mapping
                    cursor_x = int(index_tip.x * self.screen_width)
                    cursor_y = int(index_tip.y * self.screen_height)
                    palm_y_px = int(palm_base.y * h)
                    
                    # Check which fingers are UP
                    index_up = lm[8].y < lm[6].y
                    middle_up = lm[12].y < lm[10].y
                    ring_up = lm[16].y < lm[14].y
                    pinky_up = lm[20].y < lm[18].y
                    
                    all_fingers_up = index_up and middle_up and ring_up and pinky_up
                    
                    # Custom states for precise clicking
                    three_fingers_folded = not middle_up and not ring_up and not pinky_up
                    all_fingers_folded = not index_up and not middle_up and not ring_up and not pinky_up
                    
                    current_time = time.time()

                    # ---------------- GESTURE MAPPING ----------------

                    # 1 & 2. CURSOR MOVE & LEFT CLICK (Pinch)
                    if three_fingers_folded and not all_fingers_folded:
                        dist_pinch = self.get_distance(thumb_tip, index_tip)
                        
                        # PINCH = LEFT CLICK (Works even if index finger bends slightly)
                        if dist_pinch < 0.05: 
                            if current_time - self.last_action_time > 0.3:
                                pyautogui.click()
                                self.last_action_time = current_time
                                cv2.putText(frame, "Action: Left Click!", (20, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        
                        # OPEN INDEX = CURSOR MOVE
                        elif index_up: 
                            pyautogui.moveTo(cursor_x, cursor_y, duration=0.03)
                            cv2.putText(frame, "Mode: Cursor Move", (20, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
                    # 3. RIGHT CLICK: Index + Middle Finger Up (Peace Sign)
                    elif index_up and middle_up and not ring_up and not pinky_up:
                        if current_time - self.last_action_time > 0.6:
                            pyautogui.rightClick()
                            self.last_action_time = current_time
                            cv2.putText(frame, "Action: Right Click!", (20, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            
                    # 4. SCROLL: Open Palm (All Fingers Up)
                    elif all_fingers_up:
                        if self.prev_palm_y is not None:
                            dy = palm_y_px - self.prev_palm_y
                            if dy < -15:
                                pyautogui.scroll(150)
                                cv2.putText(frame, "Action: Scroll UP", (20, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                            elif dy > 15:
                                pyautogui.scroll(-150)
                                cv2.putText(frame, "Action: Scroll DOWN", (20, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                        
                        self.prev_palm_y = palm_y_px
                    else:
                        # Reset scroll tracker if hand closes
                        self.prev_palm_y = None
                        
                    # 5. VOLUME CONTROL: Thumbs Up / Down (All other fingers folded)
                    if all_fingers_folded:
                        # Thumbs UP (Thumb tip is higher than the rest of the knuckles)
                        if thumb_tip.y < lm[2].y and thumb_tip.y < lm[17].y:
                            if current_time - self.last_action_time > 0.2:
                                pyautogui.press('volumeup')
                                self.last_action_time = current_time
                                cv2.putText(frame, "Action: Vol UP (+)", (20, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                        # Thumbs DOWN (Thumb tip is lower than the wrist/knuckles)
                        elif thumb_tip.y > lm[2].y and thumb_tip.y > lm[17].y:
                            if current_time - self.last_action_time > 0.2:
                                pyautogui.press('volumedown')
                                self.last_action_time = current_time
                                cv2.putText(frame, "Action: Vol DOWN (-)", (20, 50), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow(self.window_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    controller = MediaPipeGestureController()
    controller.run()