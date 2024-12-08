import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

# Initialize camera, hand detector, keyboard, and mouse controllers
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Increased resolution for better accuracy
cap.set(4, 480)
detector = HandDetector(detectionCon=0.8, maxHands=2)  # Higher confidence
keyboard = KeyboardController()
mouse = MouseController()

# Sensitivity for mouse movement based on hand position
mouse_sensitivity = 1.5  # Adjustable

# Game Modes
game_mode = "RACING"  # Switch to "RACING" for car racing games

# Track states
scope_mode_active = False


def handle_fps_controls(hand, fingers, hand_type):
    """Handles controls for FPS games like Valorant."""
    global scope_mode_active

    if hand_type == "Right":
        # Mouse movement with a closed fist
        if fingers == [0, 0, 0, 0, 0]:
            index_tip = hand["lmList"][8]
            x, y = index_tip[0], index_tip[1]
            mouse.move(mouse_sensitivity * (x - 320), mouse_sensitivity * (y - 240))
        # Scope mode: Index finger extended
        elif fingers == [0, 1, 0, 0, 0] and not scope_mode_active:
            mouse.press(Button.right)
            scope_mode_active = True
        elif fingers == [1, 0, 0, 0, 0]:
            # Move and scope at the same time
            index_tip = hand["lmList"][8]
            x, y = index_tip[0], index_tip[1]
            mouse.move(mouse_sensitivity * (x - 320), mouse_sensitivity * (y - 240))
            if not scope_mode_active:
                mouse.press(Button.right)
                scope_mode_active = True
    elif hand_type == "Left":
        # WASD movement
        if fingers == [0, 0, 0, 0, 1]:  # Pinky for 'A' (left)
            keyboard.press('a')
            keyboard.release('d')
        elif fingers == [0, 1, 0, 0, 0]:  # Index for 'D' (right)
            keyboard.press('d')
            keyboard.release('a')
        elif fingers == [0, 1, 1, 1, 1]:  # All extended for 'W' (forward)
            keyboard.press('w')
        elif fingers == [0, 0, 0, 0, 0]:  # Fist for 'S' (backward)
            keyboard.press('s')
        elif fingers == [1, 0, 0, 0, 0]:  # Thumb for shooting
            mouse.click(Button.left)
        elif fingers == [0, 0, 1, 0, 0]:  # Middle finger for reload
            keyboard.press('r')
        elif fingers == [1, 1, 0, 0, 0]:  # Thumb and index for crouch
            keyboard.press('c')
        elif fingers == [0, 0, 1, 1, 1]:  # Middle, ring, pinky for jump
            keyboard.press(Key.space)
        elif fingers == [0, 1, 1, 0, 1]:  # Index, middle, pinky for run
            keyboard.press('w')
            keyboard.press(Key.shift)
        else:  # Release all keys if no gesture is detected
            release_all_keys()


def handle_racing_controls(hand, fingers):
    """Handles controls for car racing games."""
    if fingers == [0, 0, 0, 0, 1]:  # Pinky extended to steer left
        keyboard.press('a')
        keyboard.release('d')
    elif fingers == [0, 1, 0, 0, 0]:  # Index extended to steer right
        keyboard.press('d')
        keyboard.release('a')
    elif fingers == [0, 1, 1, 1, 1]:  # All extended for accelerate
        keyboard.press('w')
    elif fingers == [0, 0, 0, 0, 0]:  # Fist to brake
        keyboard.press('s')
    elif fingers == [1, 0, 0, 0, 0]:  # Thumb for nitro boost
        keyboard.press(Key.shift)
    else:  # Release all keys if no gesture is detected
        release_all_keys()


def release_all_keys():
    """Releases all keyboard keys."""
    for key in ['a', 'd', 'w', 's', 'r', 'c']:
        keyboard.release(key)
    keyboard.release(Key.space)
    keyboard.release(Key.shift)


# Main loop
while True:
    _, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        for hand in hands:
            fingers = detector.fingersUp(hand)
            hand_type = hand["type"]

            if game_mode == "FPS":
                handle_fps_controls(hand, fingers, hand_type)
            elif game_mode == "RACING":
                handle_racing_controls(hand, fingers)
    else:
        release_all_keys()
        if scope_mode_active:
            mouse.release(Button.right)
            scope_mode_active = False

    # Display the video feed
    cv2.imshow("Game Control", img)
    if cv2.waitKey(1) == ord("q"):  # Exit on 'q'
        break

cap.release()
cv2.destroyAllWindows()





# import cv2
# from cvzone.HandTrackingModule import HandDetector
# from pynput.keyboard import Key, Controller as KeyboardController
# from pynput.mouse import Button, Controller as MouseController

# # Initialize camera, hand detector, keyboard, and mouse controllers
# cap = cv2.VideoCapture(0)
# cap.set(3, 320)
# cap.set(4, 210)

# detector = HandDetector(detectionCon=0.7, maxHands=2)  # Detect up to 2 hands
# keyboard = KeyboardController()
# mouse = MouseController()

# # Sensitivity for mouse movement based on hand position
# sensitivity = 1  # Adjust to control how quickly the camera moves

# # Variable to track if right mouse button is pressed for scope mode
# scope_mode_active = False

# while True:
#     _, img = cap.read()
#     hands, img = detector.findHands(img)

#     if hands:
#         for hand in hands:
#             finger = detector.fingersUp(hand)
#             hand_type = hand["type"]

#             # Check if the hand is right or left
#             if hand_type == "Right":
#                 # Right-hand fist for controlling mouse pointer
#                 if finger == [0, 0, 0, 0, 0]:
#                     # Get index finger tip position for smoother camera control
#                     index_tip = hand["lmList"][8]  # Index finger tip landmark
#                     x, y = index_tip[0], index_tip[1]
#                     mouse.move(sensitivity * (x - 160), sensitivity * (y - 105))  # Center is around (160, 105)

#                 # Scope mode: Right-hand index finger extended
#                 elif finger == [0, 1, 0, 0, 0]:
#                     if not scope_mode_active:  # Activate scope mode
#                         mouse.press(Button.right)  # Hold right mouse button
#                         scope_mode_active = True

#                 # Camera control and scope mode together: Right thumb extended
#                 elif finger == [1, 0, 0, 0, 0]:
#                     # Activate both camera control and scope mode
#                     if not scope_mode_active:
#                         mouse.press(Button.right)  # Hold right mouse button
#                         scope_mode_active = True

#                     # Get index finger tip position for smoother camera control
#                     index_tip = hand["lmList"][8]  # Index finger tip landmark
#                     x, y = index_tip[0], index_tip[1]
#                     mouse.move(sensitivity * (x - 160), sensitivity * (y - 105))  # Center is around (160, 105)

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
#                 elif finger == [0, 0, 1, 0, 0]:
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

#     # Release right mouse button when scope mode is no longer active
#     if scope_mode_active and (finger != [0, 1, 0, 0, 0] and finger != [1, 0, 0, 0, 0]):
#         mouse.release(Button.right)
#         scope_mode_active = False

#     cv2.imshow("Valorant Control", img)
#     if cv2.waitKey(1) == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()
