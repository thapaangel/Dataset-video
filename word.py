import cv2
import os
import time

# ASL words
asl_words = [
    "Hello", "See_You_Later", "I_or_Me", "Father", "Mother", "Yes", "No",
    "Help", "Please", "Thank_You", "Want", "What"
]

# Dataset folder
dataset_path = "ASL_Video_Dataset"
os.makedirs(dataset_path, exist_ok=True)

# Camera setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

fps = 20
duration = 5        # seconds per video
frames_to_record = fps * duration
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
videos_per_word = 100

print("\nCamera started successfully!")

while True:
    print("\nAvailable ASL words:")
    for w in asl_words:
        print("-", w)

    selected = input("\nEnter word to record (or 'exit' to quit): ")

    if selected.lower() == "exit":
        break

    if selected not in asl_words:
        print("Invalid word! Try again.")
        continue

    # Folder for the selected word
    word_path = os.path.join(dataset_path, selected)
    os.makedirs(word_path, exist_ok=True)

    print(f"\nYou selected: {selected}")
    input("Press ENTER to start capturing 100 videos...")

    for vid in range(1, videos_per_word + 1):
        print(f"\nRecording video {vid}/100 for {selected}...")
        video_name = os.path.join(word_path, f"{selected}_{vid}.mp4")

        out = cv2.VideoWriter(video_name, fourcc, fps,
                              (int(cap.get(3)), int(cap.get(4))))

        frame_count = 0

        # Short pause before each video
        time.sleep(1)

        while frame_count < frames_to_record:
            ret, frame = cap.read()
            if not ret:
                print("Error capturing frame!")
                break

            cv2.putText(frame, f"{selected} | Video {vid}/100",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            cv2.imshow("ASL Video Capture", frame)
            out.write(frame)
            frame_count += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Stopped early.")
                break

        out.release()
        print(f"Saved: {video_name}")

print("Closing camera...")
cap.release()
cv2.destroyAllWindows()
