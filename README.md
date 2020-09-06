# Webcam Face Masker (under development)

This application applies a facial mask to any faces captured by the webcam. 
In addition, it includes a "Save snapshot" feature that captures the current frame and saves it as a JPEG file.

Note: project developed in Python 3.7

## Instructions

### Environment setup
To setup the Python environment please use the **environment.yml** file and run the following in your terminal: **conda env create -f environment.yml**
*Note*: this approach should resolve the issues commonly associated with projects using libraries installed via "conda" and "pip" (such as this one).

### Running Face Masker
For now, the only way to run the Face Masker app is directly from the "[PROJECT_DIRECTORY]/src/**facemasker_main.py**" script.

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
Next, I'm planning on packaging the app and distribute it with an installer (possibly using the Rust-based PyOxidizer, since pyinstaller and cx_Freeze failed to accomplish this). 

- **Manuel Oliveira** (manueljbo@gmail.com)
