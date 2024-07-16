# Webcam Face Masker

This application applies a facial mask to any faces captured by the webcam. 
In addition, it includes a "Save snapshot" feature that captures the current frame and saves it as a JPEG file.

Note: project developed in Python 3.7

## Instructions

### Environment setup
To setup the Python environment please use the **environment.yml** file and run the following in your terminal: **conda env create -f environment.yml**

### Running Face Masker
You can run the Face Masker app from the "*facemasker_main.py**" script.

The app requires dlib's face landmark predictor file (**shape_predictor_68_face_landmarks.dat**) to properly work. 
In the first run, it will automatically download this file and save it in the *data* folder, so it will take some time to launch the app window.
Once the file is downloaded and saved to your disk (in the data folder of the project) the app will initiate immediately on the following runs. 

**Note**: 
The application initiates the system's webcam. 
This may trigger some actions from your antivirus software, such as requests for camera access.
If this happens, the application will only work if you allow temporary access to the camera.
The app works entirely in your local machine, and as you may confirm in the source code, no data is collected or sent anywhere else.


This was developed during my free time as a hobby project.
There are some limitations in version 1.0 that I am still trying to overcome, especially the low frame rate.
