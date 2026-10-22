# DeleteMe

**English** | [Türkçe](README.tr.md)

DeleteMe is a small OpenCV-based webcam app that removes you from the camera image when you close your fist.

> This project is based on [TzurSoffer/deleteMe](https://github.com/TzurSoffer/deleteMe) by Tzur Soffer.
> Added in this version: virtual camera output (use it in Zoom, Meet, Teams, Discord), camera selection, Turkish/English interface and several bug fixes.

## Requirements

- Python 3.10+ recommended
- Webcam
- Windows, macOS, or Linux with camera access

Python packages are listed in [requirements.txt](requirements.txt).

## Install

Create and activate a virtual environment, then install the dependencies:

```bash
pip install -r requirements.txt
```

If you prefer to install manually, the project depends on:

- opencv-python
- mediapipe
- pyvirtualcam
- pillow
- pygrabber (Windows only, used to list cameras by name)

## Run

Start the GUI from the project root:

```bash
python main.py
```

Use the **Dil / Language** menu in the top-right corner of the window to switch between Turkish and English.

## How to use

1. Launch the app.
2. Choose your camera from the "Camera" list. Click "Refresh" if you plugged in a camera after starting the app.
3. Make sure the camera shows an empty background.
4. Click "Capture Background".
5. Watch the live preview window and move out of frame before the countdown ends.
6. Click "Start App" to start the effect.

### Virtual camera

With "Send the image to the virtual camera" checked, the processed video is also sent to
**OBS Virtual Camera** (via [pyvirtualcam](https://github.com/letmaik/pyvirtualcam)).
Select OBS Virtual Camera as the camera in Zoom, Google Meet, Teams, Discord, etc.

- OBS Studio (28+) must be installed; OBS itself must not be running its own virtual camera at the same time.
- The "Camera" list shows the cameras on your computer by name. OBS Virtual Camera is left out, because the app sends its output there.

### Controls

- In the background preview window, press `q` or `Esc` to cancel capture.
- In the main OpenCV window, press `q` to exit the loop.

## Files

- [main.py](main.py) contains the Tkinter GUI, the camera flow and the Turkish/English texts.
- [deleteMe.py](deleteMe.py) contains the main effect logic.
- [utils.py](utils.py) contains the person and hand detection helpers.
- `bg.jpg` is the background image the app creates at runtime.

## Notes

- The app saves the captured background to `bg.jpg`.
- If the camera fails to open, make sure no other app is using it.
- If the background capture looks wrong, clear the scene again and recapture it.

## License

This project is licensed under the MIT License, see [LICENSE](LICENSE). An unofficial Turkish translation is in [LICENSE.tr](LICENSE.tr).
