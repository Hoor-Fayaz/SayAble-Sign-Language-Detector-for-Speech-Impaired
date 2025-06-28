import os
import cv2

# Set up dataset directory
DATA_DIR = './digit_data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Define the 10 digit classes
digit_classes = [str(i) for i in range(10)]
dataset_size = 100  # Images per digit

# Open webcam
cap = cv2.VideoCapture(0)

for digit in digit_classes:
    save_path = os.path.join(DATA_DIR, digit)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    print(f'\nCollecting data for digit: {digit}')
    print("Press 'Q' to start capturing...")

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f'Digit: {digit} - Press "Q" to start', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    counter = 0
    print("Capturing images...")
    while counter < dataset_size:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        filename = os.path.join(save_path, f'{counter}.jpg')
        cv2.imwrite(filename, frame)
        counter += 1

    print(f'Done collecting for {digit}!')

cap.release()
cv2.destroyAllWindows()


