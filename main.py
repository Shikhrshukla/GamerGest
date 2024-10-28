# import cv2
# from cvzone.HandTrackingModule import HandDetector
# from pynput.keyboard import Key, Controller as KeyboardController
# from pynput.mouse import Button, Controller as MouseController
#
# # Initialize camera, hand detector, keyboard, and mouse controllers
# cap = cv2.VideoCapture(0)
# cap.set(3, 320)
# cap.set(4, 210)
#
# detector = HandDetector(detectionCon=0.7, maxHands=2)  # Detect up to 2 hands
# keyboard = KeyboardController()
# mouse = MouseController()
#
# # Sensitivity for mouse movement based on hand position
# sensitivity = 1  # Adjust to control how quickly the camera moves
#
# while True:
#     _, img = cap.read()
#     hands, img = detector.findHands(img)
#
#     if hands:
#         for hand in hands:
#             finger = detector.fingersUp(hand)
#             hand_type = hand["type"]
#
#             # Check if the hand is right or left
#             if hand_type == "Right":
#                 # Right-hand fist for controlling mouse pointer
#                 if finger == [0, 0, 0, 0, 0]:
#                     # Get index finger tip position for smoother camera control
#                     index_tip = hand["lmList"][8]  # Index finger tip landmark
#                     x, y = index_tip[0], index_tip[1]
#                     mouse.move(sensitivity * (x - 160), sensitivity * (y - 105))  # Center is around (160, 105)
#
#             elif hand_type == "Left":
#                 # Define left-hand gestures for specific game actions
#                 # Move Left: Pinky finger only extended
#                 if finger == [0, 0, 0, 0, 1]:
#                     keyboard.press('a')
#                     keyboard.release('d')
#                 # Move Right: Only index finger extended
#                 elif finger == [0, 1, 0, 0, 0]:
#                     keyboard.press('d')
#                     keyboard.release('a')
#                 # Move Forward: Index, middle, ring, and pinky fingers extended
#                 elif finger == [0, 1, 1, 1, 1]:
#                     keyboard.press('w')
#                 # Move Backward: Fist gesture, all fingers down
#                 elif finger == [0, 0, 0, 0, 0]:
#                     keyboard.press('s')
#                 # Shoot: Thumb only extended
#                 elif finger == [1, 0, 0, 0, 0]:
#                     mouse.press(Button.left)  # Left mouse button click
#                     mouse.release(Button.left)
#                 # Reload: Only middle finger extended
#                 elif finger == [1, 0, 1, 0, 0]:
#                     keyboard.press('r')
#                 # Crouch: Thumb and index fingers extended
#                 elif finger == [1, 1, 0, 0, 0]:
#                     keyboard.press('c')
#                 # Jump: Middle, ring, and pinky fingers extended
#                 elif finger == [0, 0, 1, 1, 1]:
#                     keyboard.press(Key.space)
#                 # Run: Index, middle, and pinky fingers extended
#                 elif finger == [0, 1, 1, 0, 1]:
#                     keyboard.press('w')
#                     keyboard.press(Key.shift)  # Press Left Shift for running
#                 else:
#                     # Release all movement keys if no specific gesture is detected
#                     keyboard.release('a')
#                     keyboard.release('d')
#                     keyboard.release('w')
#                     keyboard.release('s')
#                     keyboard.release(Key.space)
#                     keyboard.release('r')
#                     keyboard.release('c')
#                     keyboard.release(Key.shift)  # Release Left Shift
#
#     else:
#         # Releasing all keys when no hand is detected
#         keyboard.release('a')
#         keyboard.release('d')
#         keyboard.release('w')
#         keyboard.release('s')
#         keyboard.release(Key.space)
#         keyboard.release('r')
#         keyboard.release('c')
#         keyboard.release(Key.shift)  # Release Left Shift
#
#     cv2.imshow("Valorant Control", img)
#     if cv2.waitKey(1) == ord("q"):
#         break
#
# cap.release()
# cv2.destroyAllWindows()




import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# Initialize camera, hand detector, keyboard, and mouse controllers
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 210)

detector = HandDetector(detectionCon=0.7, maxHands=2)  # Detect up to 2 hands
keyboard = KeyboardController()
mouse = MouseController()

# Sensitivity for mouse movement based on hand position
sensitivity = 1  # Adjust to control how quickly the camera moves

# Variable to track if right mouse button is pressed for scope mode
scope_mode_active = False

while True:
    _, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            finger = detector.fingersUp(hand)
            hand_type = hand["type"]

            # Check if the hand is right or left
            if hand_type == "Right":
                # Right-hand fist for controlling mouse pointer
                if finger == [0, 0, 0, 0, 0]:
                    # Get index finger tip position for smoother camera control
                    index_tip = hand["lmList"][8]  # Index finger tip landmark
                    x, y = index_tip[0], index_tip[1]
                    mouse.move(sensitivity * (x - 160), sensitivity * (y - 105))  # Center is around (160, 105)

                # Scope mode: Right-hand index finger extended
                elif finger == [0, 1, 0, 0, 0]:
                    if not scope_mode_active:  # Activate scope mode
                        mouse.press(Button.right)  # Hold right mouse button
                        scope_mode_active = True

                # Camera control and scope mode together: Right thumb extended
                elif finger == [1, 0, 0, 0, 0]:
                    # Activate both camera control and scope mode
                    if not scope_mode_active:
                        mouse.press(Button.right)  # Hold right mouse button
                        scope_mode_active = True

                    # Get index finger tip position for smoother camera control
                    index_tip = hand["lmList"][8]  # Index finger tip landmark
                    x, y = index_tip[0], index_tip[1]
                    mouse.move(sensitivity * (x - 160), sensitivity * (y - 105))  # Center is around (160, 105)

            elif hand_type == "Left":
                # Define left-hand gestures for specific game actions
                # Move Left: Pinky finger only extended
                if finger == [0, 0, 0, 0, 1]:
                    keyboard.press('a')
                    keyboard.release('d')
                # Move Right: Only index finger extended
                elif finger == [0, 1, 0, 0, 0]:
                    keyboard.press('d')
                    keyboard.release('a')
                # Move Forward: Index, middle, ring, and pinky fingers extended
                elif finger == [0, 1, 1, 1, 1]:
                    keyboard.press('w')
                # Move Backward: Fist gesture, all fingers down
                elif finger == [0, 0, 0, 0, 0]:
                    keyboard.press('s')
                # Shoot: Thumb only extended
                elif finger == [1, 0, 0, 0, 0]:
                    mouse.press(Button.left)  # Left mouse button click
                    mouse.release(Button.left)
                # Reload: Only middle finger extended
                elif finger == [0, 0, 1, 0, 0]:
                    keyboard.press('r')
                # Crouch: Thumb and index fingers extended
                elif finger == [1, 1, 0, 0, 0]:
                    keyboard.press('c')
                # Jump: Middle, ring, and pinky fingers extended
                elif finger == [0, 0, 1, 1, 1]:
                    keyboard.press(Key.space)
                # Run: Index, middle, and pinky fingers extended
                elif finger == [0, 1, 1, 0, 1]:
                    keyboard.press('w')
                    keyboard.press(Key.shift)  # Press Left Shift for running
                else:
                    # Release all movement keys if no specific gesture is detected
                    keyboard.release('a')
                    keyboard.release('d')
                    keyboard.release('w')
                    keyboard.release('s')
                    keyboard.release(Key.space)
                    keyboard.release('r')
                    keyboard.release('c')
                    keyboard.release(Key.shift)  # Release Left Shift

    else:
        # Releasing all keys when no hand is detected
        keyboard.release('a')
        keyboard.release('d')
        keyboard.release('w')
        keyboard.release('s')
        keyboard.release(Key.space)
        keyboard.release('r')
        keyboard.release('c')
        keyboard.release(Key.shift)  # Release Left Shift

    # Release right mouse button when scope mode is no longer active
    if scope_mode_active and (finger != [0, 1, 0, 0, 0] and finger != [1, 0, 0, 0, 0]):
        mouse.release(Button.right)
        scope_mode_active = False

    cv2.imshow("Valorant Control", img)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
