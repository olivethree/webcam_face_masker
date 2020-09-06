import time
import tkinter
from math import hypot
from tkinter import *

import PIL.Image
import PIL.ImageTk
import cv2
import dlib
import numpy as np
import os


class App:
    def __init__(self, video_source=0):
        self.appName = "Face Masker v1.0"
        self.window = tkinter.Tk()
        self.window.title("Face Masker v1.0 | Manuel Barbosa de Oliveira")
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a label at the top of the app window
        self.label = Label(
            self.window, text=self.appName, font=15, bg="NavajoWhite4", fg="black"
        ).pack(side=TOP, fill=BOTH)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(
            self.window, width=self.vid.width, height=self.vid.height, bg="black"
        )
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot = tkinter.Button(
            self.window, text="Save snapshot", width=50, command=self.snapshot
        )
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

        # Prevent window to start minimized, make it pop on the screen when app starts
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.after_idle(self.window.attributes, '-topmost', False)

        self.window.mainloop()

    def face_mask(self, filepath=os.path.abspath("../data/img/facemask.png")):
        mask_img = cv2.imread(filepath)
        return mask_img

    def mask_face(self):
        # Load face mask image
        mask_image = self.face_mask()

        # Load dlib's face detector (HOG-based) and create facial landmark predictor based on pre-trained data file
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(
            os.path.abspath("../data/shape_predictor_68_face_landmarks.dat")
        )

        # Note: adding "while self.vid" loop below prevents app freezing when faces go out of boundaries
        while self.vid:

            # Get a frame from the video source
            ret, frame = self.vid.get_frame()

            # Get capture frame dimensions
            rows, cols, _ = frame.shape

            # Create empty numpy array with frame dimensions to create frame mask layer
            frame_fill_mask = np.zeros((rows, cols), np.uint8)
            frame_fill_mask.fill(0)

            # Convert input to grayscale
            grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = detector(frame)

            # Overlay facial mask image onto faces in faces detected by the camera
            # based on facial landmark coordinates defining face mask region
            for face in faces:
                # Extract facial landmarks for each face
                landmarks = predictor(grayscaled_frame, face)

                # Masking coordinates
                top_nose_landmark = (landmarks.part(27).x, landmarks.part(27).y)
                left_face_edge = (landmarks.part(2).x, landmarks.part(2).y)
                right_face_edge = (landmarks.part(15).x, landmarks.part(15).y)

                # Define face width
                face_width = int(
                    hypot(
                        left_face_edge[0] - right_face_edge[0],
                        left_face_edge[1] - right_face_edge[1],
                    )
                    * 1.0
                )

                # To compute face height:
                # get face mask image dimensions (485 x 400 pixels)
                # compute width-to-height ratio = 400 / 485 = 0.8247422680412371134020618556701
                face_height = int(
                    face_width * 400 / 485
                )  # mask.png image dimensions (485 x 400 pixels) ratio = 400 / 485 = 0.8247422680412371134020618556701

                # Calculate point at the center of rectangle defining the face mask image (= center of face mask region)
                center_mask = (
                    int(left_face_edge[0] + face_width / 2),
                    int(top_nose_landmark[1] + face_height / 2),
                )

                """ in top_left coordinates were adjusted (x - 3, y + 9) to compensate for the gap 
                between the top left corner of the rectangle region and the actual top left vertex 
                region of the mask image. Compensation on y-axis (+20) stretches mask to cover jaw 
                region in longer faces with wider jawlines. 
                Switch to alternative less tweaked top_left parameters using uncomment (leave only
                one object activated!)"""
                top_left = (
                    int(center_mask[0] - face_width / 2) - 3,
                    int(center_mask[1] - face_height / 2) + 20,
                )

                # Alternatively, activate the simpler approach below for top_left:
                # top_left = (
                #     int(center_mask[0] - face_width / 2),
                #     int(center_mask[1] - face_height / 2),
                # )

                # Face mask overlaying procedure
                facemask = cv2.resize(mask_image, (face_width, face_height))
                facemask_gray = cv2.cvtColor(facemask, cv2.COLOR_BGR2GRAY)

                _, frame_fill_mask = cv2.threshold(
                    facemask_gray, 25, 255, cv2.THRESH_BINARY_INV
                )

                face_area = frame[
                            top_left[1]: top_left[1] + face_height,
                            top_left[0]: top_left[0] + face_width,
                            ]

                face_area_no_facemask = cv2.bitwise_and(
                    face_area, face_area, mask=frame_fill_mask
                )

                # Finalize masking the detected face
                final_mask = cv2.add(face_area_no_facemask, facemask)

                frame[
                top_left[1]: top_left[1] + face_height,
                top_left[0]: top_left[0] + face_width,
                ] = final_mask

                cv2image = cv2.flip(frame, 1)

                return cv2image

    def snapshot(self):
        # Get a masked face frame from the video source
        masked_frame = self.mask_face()
        # Save image in current directory
        cv2.imwrite(
            "MASKED_FACE_SNAPSHOT_" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
            cv2.cvtColor(masked_frame, cv2.COLOR_RGB2BGR),
        )

    def update(self):
        # Get a masked frame from the video source
        maskedface = self.mask_face()
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(maskedface))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Run app
#App()
