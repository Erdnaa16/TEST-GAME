import cv2
import mediapipe as mp
import numpy as np
from questions import questions

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)

current_q = 0
score = 0
answer_selected = False

def get_hand_direction(landmarks):
    # Wrist landmark
    wrist_x = landmarks[0].x
    
    # Index finger tip
    index_x = landmarks[8].x
    
    # Compare positions
    if index_x < wrist_x - 0.05:
        return "left"
    elif index_x > wrist_x + 0.05:
        return "right"
    return None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Display Question
    if current_q < len(questions):
        q = questions[current_q]

        cv2.putText(frame, q["question"], (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, "LEFT: " + q["left"], (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.putText(frame, "RIGHT: " + q["right"], (50, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            direction = get_hand_direction(hand_landmarks.landmark)

            if direction and not answer_selected:
                answer_selected = True

                if direction == q["answer"]:
                    score += 1
                    print("Correct!")
                else:
                    print("Wrong!")

                current_q += 1

    # Reset delay
    if answer_selected:
        cv2.putText(frame, "Answer detected...", (50, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Game", frame)
        cv2.waitKey(1000)
        answer_selected = False

    # Game Over
    if current_q >= len(questions):
        cv2.putText(frame, f"Final Score: {score}", (50, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    cv2.imshow("Hand Gesture Quiz", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
def is_valid_advice(sentence):
    sentence = sentence.lower()
    return "should" in sentence
if direction and not answer_selected:
    answer_selected = True

    chosen_answer = q[direction]

    # Check grammar first
    if not is_valid_advice(chosen_answer):
        print("Invalid answer format!")
    else:
        if direction == q["answer"]:
            score += 1
            print("Correct advice!")
        else:
            print("Wrong advice!")

    current_q += 1
    cv2.putText(frame, "Use: SHOULD / SHOULDN'T",
            (50, 300),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    feedback = ""

if direction == q["answer"]:
    feedback = "Good! Correct advice."
else:
    feedback = "Try again! Think carefully."

cv2.putText(frame, feedback, (50, 350),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
{
    "question": "You have a headache.",
    "left": "You should rest.",
    "right": "You should play football.",
    "answer": "left"
}
