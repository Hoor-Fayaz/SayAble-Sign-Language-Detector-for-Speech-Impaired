import os
import cv2
import time

# Setup folder for travel & emergency category
DATA_DIR = './data_communication_videos'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Travel & Emergency related words
everyday_communication = [
    "hello", "goodbye", "thank_you", "sorry", "please",
    "welcome", "fine", "excuse", "sign", "language",
    "understand", "not", "again", "slow", "write",
    "talk", "maybe", "phone", "yes", "no", "No Gesture Detected"
]



videos_per_class = 30
video_duration = 3  # seconds
fps = 20  # frames per second

# Start webcam
cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))

for word in everyday_communication:
    word_path = os.path.join(DATA_DIR, word)
    if not os.path.exists(word_path):
        os.makedirs(word_path)

    print(f'\nPreparing to collect videos for: {word}')
    print("Press 'Q' to start recording each video...")

    existing_files = [f for f in os.listdir(word_path) if f.endswith('.avi')]
    counter = len(existing_files)

    while counter < videos_per_class:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, f'Ready for: {word} | Video #{counter+1}',
                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            avi_filename = os.path.join(word_path, f'{counter}.avi')
            mp4_filename = os.path.join(word_path, f'{counter}.mp4')

            out_avi = cv2.VideoWriter(avi_filename, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))
            out_mp4 = cv2.VideoWriter(mp4_filename, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

            print(f"Recording video {counter + 1}/{videos_per_class} for '{word}'...")

            start_time = time.time()
            while (time.time() - start_time) < video_duration:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                out_avi.write(frame)
                out_mp4.write(frame)
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('e'):  # emergency stop
                    break

            out_avi.release()
            out_mp4.release()
            print("Recording complete.")
            counter += 1

print("✅ All everyday communication videos collected.")
cap.release()
cv2.destroyAllWindows()
