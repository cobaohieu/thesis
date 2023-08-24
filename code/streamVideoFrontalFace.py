import cv2
import imutils
import time
import threading


from imutils.video import VideoStream


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


def main():
    cascade_path = 'C://Users//{yourname}//AppData//Local//Programs//Python//Python37//Lib//site-packages//cv2//data//haarcascade_frontalface_default.xml'  # Replace with the actual path
    cascade = cv2.CascadeClassifier(cascade_path)

    # cap = cv2.VideoCapture(0)  # Use the appropriate camera index
    cap = VideoStream(src=0).start()

    # Initialize variables for FPS calculation
    start_time = time.time()
    frame_count = 0
    fps_text = 0
    fps = 0

    # while cap.isOpened():
    while True:
        # ret, frame = cap.read()
        # if not ret:
        #     break
        frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = cascade.detectMultiScale(gray, 1.2, 3, minSize=(5, 5))

        for (x, y, w, h) in rects:
            draw_border(frame, (x, y), (x + w, y + h), (0, 255, 255), 4, 5, 5)

        # Calculate and display FPS
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            start_time = current_time
            frame_count = 0

        # Prepare FPS text
        fps_text = f'FPS: {int(fps)}'

        # Display FPS on the frame
        print(fps_text)
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Press 'q' to exit the loop
    # cap.release()
    cap.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
