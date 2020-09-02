# Webcam Face Masker (under development)

This application applies a facial mask to any faces captured by the webcam. 
In addition, it includes a "Save snapshot" feature that captures the current frame and saves it as a JPEG file.

## Running the app

For now, the only way to run the Face Masker app is directly from the "[PROJECT_DIRECTORY]/src/facemasker_ui.py" script.

Note: 
The application initiates the system's webcam. 
This may trigger some actions from your antivirus software, such as requests for camera access.
If this happens, the application will only work if you allow temporary access to the camera.
The app works entirely in your local machine, and as you may confirm in the source code, no data is collected or sent anywhere else.


This was developed during my free time as a hobby project.
There are some limitations in version 1.0 that I am still trying to overcome, especially the "laggy" frame rate.
On top of that, I'm planning on packaging the app and distribute it with an installer.

- Manuel Oliveira (manueljbo@gmail.com)
