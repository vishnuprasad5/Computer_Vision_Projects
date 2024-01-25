import cv2
import os

num_classes = 28
samples_per_class = 100

dataset_folder = 'data'
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

cap = cv2.VideoCapture(0)

def capture_images(class_id):
    class_folder = os.path.join(dataset_folder, str(class_id))
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)

    print(f"Press 'c' to capture images for class {class_id}...")

    while True:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)

        height, width, _ = frame.shape

        text_position = ((width - 400) // 2, 30)

        cv2.putText(frame, f"Press 'c' to capture for class {class_id}", text_position,
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Capture', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            break

    print(f"Capturing {samples_per_class} images for class {class_id}...")

    for sample in range(samples_per_class):
        ret, frame = cap.read()

        flipped_frame = cv2.flip(frame, 1)

        text_position = ((width - 400) // 2, 30)

        cv2.putText(flipped_frame, f"Capturing {sample + 1}/{samples_per_class} images", text_position,
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Capture', flipped_frame)

        img_filename = os.path.join(class_folder, f"{class_id}_{sample + 1}.png")
        cv2.imwrite(img_filename, frame)

        cv2.waitKey(100)

    print(f"{samples_per_class} images captured for class {class_id}")

starting_class = 0

for class_id in range(starting_class, num_classes):
    capture_images(class_id)

    print("Press 'q' to stop or any other key to continue...")
    key = cv2.waitKey(0) & 0xFF

    if key == ord('q'):
        break

    elif key == 27:
        cap.release()
        cv2.destroyAllWindows()
        exit()

cap.release()
cv2.destroyAllWindows()
