import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import time
import cv2
import numpy as np
import pyvirtualcam
from PIL import Image, ImageDraw, ImageFont
from deleteMe import DeleteMe


backgroundFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.jpg")
captureCountdownSeconds = 5
frameTimeoutSeconds = 3
cameraWidth = 1280
cameraHeight = 720
virtualCameraName = "OBS Virtual Camera"  #< our own output, never offered as an input
defaultLanguage = "tr"

languageNames = {"tr": "Türkçe", "en": "English"}

texts = {
    "en": {
        "languageLabel": "Language:",
        "instructions": (
            "1. Clear the scene and make sure nobody is visible.\n"
            "2. Choose your camera from the list.\n"
            "3. Click \"Capture Background\" and move out of frame before the countdown ends.\n"
            "4. Click \"Start App\".\n"
            "5. In your video call app, choose OBS Virtual Camera as the camera.\n"
            "6. Close your fist to disappear from the image."
        ),
        "cameraLabel": "Camera:",
        "refreshButton": "Refresh",
        "refreshTitle": "Camera list refreshed",
        "refreshFoundMessage": "{count} camera(s) found:\n\n{names}",
        "statusCamerasFound": "Camera list refreshed: {count} camera(s) found.",
        "noCameraOption": "No camera found",
        "captureButton": "Capture Background",
        "startButton": "Start App",
        "drawBbox": "Draw a box around the person",
        "virtualCam": "Send the image to the virtual camera (OBS Virtual Camera)",
        "statusInitial": "Clear the scene, then capture a background image from the live camera preview.",
        "statusOpening": "Opening the camera preview. Move out of frame before the {seconds}-second countdown ends.",
        "statusCameraUnavailable": "Camera not available.",
        "statusPreview": "Preview running. The background will be captured in {seconds} seconds.",
        "statusCancelled": "Background capture cancelled.",
        "statusCaptureFailed": "Capture failed.",
        "statusCaptured": "Background captured and saved to {file}.",
        "cameraErrorTitle": "Camera error",
        "cameraErrorMessage": "Could not open the camera.",
        "cameraNoFramesMessage": "The camera opened but is not sending any images. Choose another camera.",
        "noCameraMessage": "No camera was found on this computer.",
        "cameraChangedTitle": "Camera changed",
        "cameraChangedMessage": "The background was captured with the {captured} camera, but {current} is selected now. Capture the background again.",
        "captureErrorTitle": "Capture error",
        "captureErrorMessage": "Could not capture a background image.",
        "missingBackgroundTitle": "Missing background",
        "missingBackgroundMessage": "Capture a background image first.",
        "virtualCamErrorTitle": "Virtual camera error",
        "virtualCamErrorMessage": "Could not start the virtual camera, continuing without it.\n\n{error}",
        "previewWindow": "DeleteMe - Background",
        "overlayPreview": "Live background preview",
        "overlayMoveOut": "Move out of frame before the capture",
        "overlayCountdown": "Capturing in {seconds} s",
    },
    "tr": {
        "languageLabel": "Dil:",
        "instructions": (
            "1. Sahneyi boşalt ve kimsenin görünmediğinden emin ol.\n"
            "2. Listeden kameranı seç.\n"
            "3. \"Arka Planı Yakala\" düğmesine tıkla ve geri sayım bitmeden kadrajdan çık.\n"
            "4. \"Uygulamayı Başlat\" düğmesine tıkla.\n"
            "5. Görüntülü görüşme uygulamasında kamera olarak OBS Virtual Camera'yı seç.\n"
            "6. Görüntüden silinmek için yumruğunu sık."
        ),
        "cameraLabel": "Kamera:",
        "refreshButton": "Yenile",
        "refreshTitle": "Kamera listesi yenilendi",
        "refreshFoundMessage": "{count} kamera bulundu:\n\n{names}",
        "statusCamerasFound": "Kamera listesi yenilendi: {count} kamera bulundu.",
        "noCameraOption": "Kamera bulunamadı",
        "captureButton": "Arka Planı Yakala",
        "startButton": "Uygulamayı Başlat",
        "drawBbox": "Kişinin etrafına çerçeve çiz",
        "virtualCam": "Görüntüyü sanal kameraya gönder (OBS Virtual Camera)",
        "statusInitial": "Sahneyi boşalt, ardından canlı kamera önizlemesinden bir arka plan görüntüsü yakala.",
        "statusOpening": "Kamera önizlemesi açılıyor. {seconds} saniyelik geri sayım bitmeden kadrajdan çık.",
        "statusCameraUnavailable": "Kamera kullanılamıyor.",
        "statusPreview": "Önizleme açık. Arka plan {seconds} saniye sonra yakalanacak.",
        "statusCancelled": "Arka plan yakalama iptal edildi.",
        "statusCaptureFailed": "Yakalama başarısız oldu.",
        "statusCaptured": "Arka plan yakalandı ve {file} dosyasına kaydedildi.",
        "cameraErrorTitle": "Kamera hatası",
        "cameraErrorMessage": "Kamera açılamadı.",
        "cameraNoFramesMessage": "Kamera açıldı ama görüntü göndermiyor. Başka bir kamera seç.",
        "noCameraMessage": "Bu bilgisayarda kamera bulunamadı.",
        "cameraChangedTitle": "Kamera değişti",
        "cameraChangedMessage": "Arka plan {captured} kamerasıyla yakalandı ama şu an {current} kamerası seçili. Arka planı yeniden yakala.",
        "captureErrorTitle": "Yakalama hatası",
        "captureErrorMessage": "Arka plan görüntüsü yakalanamadı.",
        "missingBackgroundTitle": "Arka plan yok",
        "missingBackgroundMessage": "Önce bir arka plan görüntüsü yakala.",
        "virtualCamErrorTitle": "Sanal kamera hatası",
        "virtualCamErrorMessage": "Sanal kamera başlatılamadı, sanal kamera olmadan devam ediliyor.\n\n{error}",
        "previewWindow": "DeleteMe - Arka Plan",
        "overlayPreview": "Canlı arka plan önizlemesi",
        "overlayMoveOut": "Yakalamadan önce kadrajdan çık",
        "overlayCountdown": "{seconds} saniye sonra yakalanacak",
    },
}


def listCameras():
    """Return the cameras on this PC as [(name, index, backend)], without our own virtual camera."""
    if sys.platform == "win32":
        try:
            from pygrabber.dshow_graph import FilterGraph

            names = FilterGraph().get_input_devices()
            # DirectShow device order matches OpenCV's CAP_DSHOW indices
            return [
                (name, index, cv2.CAP_DSHOW)
                for index, name in enumerate(names)
                if virtualCameraName not in name
            ]
        except Exception:
            pass  #< fall back to probing indices below

    cameras = []
    for index in range(5):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras.append((f"Camera {index}", index, cv2.CAP_ANY))
        cap.release()
    return cameras


def openCamera(camera):
    _, index, backend = camera
    cap = cv2.VideoCapture(index, backend)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, cameraWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cameraHeight)
    return cap


def loadFont(size):
    # OpenCV's built-in fonts are ASCII only, so overlays are drawn with a TrueType font
    fontsDir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for fontName in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(os.path.join(fontsDir, fontName), size)
        except OSError:
            try:
                return ImageFont.truetype(fontName, size)
            except OSError:
                continue
    return ImageFont.load_default(size)


overlayFonts = {size: loadFont(size) for size in (24, 30, 36)}


def drawOverlayLines(frame, lines):
    """Draw [(text, (x, y), size, bgrColor)] onto a BGR frame, supporting non-ASCII text."""
    image = Image.fromarray(frame)  #< colors are given as BGR to match the frame's channel order
    draw = ImageDraw.Draw(image)
    for text, position, size, color in lines:
        draw.text(
            position,
            text,
            font=overlayFonts[size],
            fill=color,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )
    return np.asarray(image).copy()


class DeleteMeApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("DeleteMe")
        self.root.resizable(False, False)

        self.language = defaultLanguage
        self.statusKey = "statusInitial"
        self.statusArgs = {}
        self.statusVar = tk.StringVar()
        self.backgroundImage = None
        self.backgroundCamera = None
        self.cameras = []
        self.drawBboxVar = tk.BooleanVar(value=True)
        self.virtualCamVar = tk.BooleanVar(value=True)
        self.languageVar = tk.StringVar(value=languageNames[self.language])

        container = ttk.Frame(self.root, padding=20)
        container.pack(fill="both", expand=True)

        headerRow = ttk.Frame(container)
        headerRow.pack(fill="x")

        title = ttk.Label(headerRow, text="DeleteMe", font=("Segoe UI", 20, "bold"))
        title.pack(side="left")

        languageCombobox = ttk.Combobox(
            headerRow,
            values=list(languageNames.values()),
            textvariable=self.languageVar,
            state="readonly",
            width=9,
        )
        languageCombobox.pack(side="right")
        languageCombobox.bind("<<ComboboxSelected>>", self.onLanguageSelected)

        self.languageLabel = ttk.Label(headerRow)
        self.languageLabel.pack(side="right", padx=(0, 6))

        self.instructions = ttk.Label(container, wraplength=470, justify="left")
        self.instructions.pack(anchor="w", pady=(8, 12))

        cameraRow = ttk.Frame(container)
        cameraRow.pack(anchor="w", pady=(0, 12))

        self.cameraLabel = ttk.Label(cameraRow)
        self.cameraLabel.pack(side="left")
        self.cameraCombobox = ttk.Combobox(cameraRow, state="readonly", width=32)
        self.cameraCombobox.pack(side="left", padx=(6, 0))
        self.refreshButton = ttk.Button(cameraRow, command=self.onRefreshClicked)
        self.refreshButton.pack(side="left", padx=(6, 0))

        buttonRow = ttk.Frame(container)
        buttonRow.pack(anchor="w", pady=(0, 12))

        self.captureButton = ttk.Button(
            buttonRow,
            command=self.captureBackground,
        )
        self.captureButton.pack(side="left")

        self.startButton = ttk.Button(
            buttonRow,
            command=self.startApp,
            state="disabled",
        )
        self.startButton.pack(side="left", padx=(10, 0))

        self.drawBboxCheckbox = ttk.Checkbutton(
            container,
            variable=self.drawBboxVar,
        )
        self.drawBboxCheckbox.pack(anchor="w", pady=(0, 4))

        self.virtualCamCheckbox = ttk.Checkbutton(
            container,
            variable=self.virtualCamVar,
        )
        self.virtualCamCheckbox.pack(anchor="w", pady=(0, 12))

        status = ttk.Label(container, textvariable=self.statusVar, wraplength=470)
        status.pack(anchor="w")

        self.refreshCameras()
        self.applyLanguage()
        self.centerWindow()

    def centerWindow(self) -> None:
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"+{x}+{y}")

    def t(self, key, **kwargs) -> str:
        return texts[self.language][key].format(**kwargs)

    def setStatus(self, key, **kwargs) -> None:
        self.statusKey = key
        self.statusArgs = kwargs
        self.statusVar.set(self.t(key, **kwargs))

    def onLanguageSelected(self, _event=None) -> None:
        for code, name in languageNames.items():
            if name == self.languageVar.get():
                self.language = code
        self.applyLanguage()

    def applyLanguage(self) -> None:
        self.languageLabel.config(text=self.t("languageLabel"))
        self.instructions.config(text=self.t("instructions"))
        self.cameraLabel.config(text=self.t("cameraLabel"))
        self.refreshButton.config(text=self.t("refreshButton"))
        self.captureButton.config(text=self.t("captureButton"))
        self.startButton.config(text=self.t("startButton"))
        self.drawBboxCheckbox.config(text=self.t("drawBbox"))
        self.virtualCamCheckbox.config(text=self.t("virtualCam"))
        if not self.cameras:
            self.cameraCombobox.set(self.t("noCameraOption"))
        self.setStatus(self.statusKey, **self.statusArgs)

    def refreshCameras(self) -> None:
        selected = self.getSelectedCamera()
        self.cameras = listCameras()
        self.cameraCombobox.config(values=[name for name, _, _ in self.cameras])
        if not self.cameras:
            self.cameraCombobox.set(self.t("noCameraOption"))
        elif selected in self.cameras:
            self.cameraCombobox.current(self.cameras.index(selected))
        else:
            self.cameraCombobox.current(0)

    def onRefreshClicked(self) -> None:
        self.refreshCameras()
        if self.cameras:
            cameraNames = "\n".join(f"• {name}" for name, _, _ in self.cameras)
            self.setStatus("statusCamerasFound", count=len(self.cameras))
            messagebox.showinfo(
                self.t("refreshTitle"),
                self.t("refreshFoundMessage", count=len(self.cameras), names=cameraNames),
            )
        else:
            self.setStatus("statusCameraUnavailable")
            messagebox.showwarning(self.t("refreshTitle"), self.t("noCameraMessage"))

    def getSelectedCamera(self):
        selectedIndex = self.cameraCombobox.current()
        if 0 <= selectedIndex < len(self.cameras):
            return self.cameras[selectedIndex]
        return None

    def captureBackground(self) -> None:
        camera = self.getSelectedCamera()
        if camera is None:
            messagebox.showerror(self.t("cameraErrorTitle"), self.t("noCameraMessage"))
            return

        self.setStatus("statusOpening", seconds=captureCountdownSeconds)
        self.root.update_idletasks()
        previewWindowName = self.t("previewWindow")

        cap = openCamera(camera)
        if not cap.isOpened():
            messagebox.showerror(self.t("cameraErrorTitle"), self.t("cameraErrorMessage"))
            self.setStatus("statusCameraUnavailable")
            return

        frame = None
        startTime = time.time()
        lastFrameTime = startTime

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    if time.time() - lastFrameTime > frameTimeoutSeconds:
                        messagebox.showerror(
                            self.t("cameraErrorTitle"), self.t("cameraNoFramesMessage")
                        )
                        self.setStatus("statusCameraUnavailable")
                        return
                    continue
                lastFrameTime = time.time()

                elapsed = time.time() - startTime
                remaining = max(0, int(captureCountdownSeconds - elapsed + 0.999))

                previewFrame = drawOverlayLines(
                    frame,
                    [
                        (self.t("overlayPreview"), (20, 15), 30, (0, 255, 255)),
                        (self.t("overlayMoveOut"), (20, 55), 24, (255, 255, 255)),
                        (self.t("overlayCountdown", seconds=remaining), (20, 90), 36, (0, 255, 0)),
                    ],
                )

                cv2.imshow(previewWindowName, previewFrame)
                self.setStatus("statusPreview", seconds=remaining)
                self.root.update_idletasks()

                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    self.setStatus("statusCancelled")
                    return
                if cv2.getWindowProperty(previewWindowName, cv2.WND_PROP_VISIBLE) < 1:
                    self.setStatus("statusCancelled")
                    return

                if elapsed >= captureCountdownSeconds:
                    break

            if frame is None:
                messagebox.showerror(
                    self.t("captureErrorTitle"), self.t("captureErrorMessage")
                )
                self.setStatus("statusCaptureFailed")
                return
        finally:
            cap.release()
            try:
                cv2.destroyWindow(previewWindowName)
            except cv2.error:
                pass  #< window already closed by the user

        if frame is None:
            messagebox.showerror(self.t("captureErrorTitle"), self.t("captureErrorMessage"))
            self.setStatus("statusCaptureFailed")
            return

        self.backgroundImage = frame.copy()
        self.backgroundCamera = camera
        cv2.imwrite(backgroundFile, self.backgroundImage)
        loadedBackground = cv2.imread(backgroundFile)
        if loadedBackground is not None:
            self.backgroundImage = loadedBackground

        self.setStatus("statusCaptured", file=os.path.basename(backgroundFile))
        self.startButton.config(state="normal")

    def startApp(self) -> None:
        if self.backgroundImage is None:
            messagebox.showinfo(
                self.t("missingBackgroundTitle"), self.t("missingBackgroundMessage")
            )
            return

        camera = self.getSelectedCamera()
        if camera is None:
            messagebox.showerror(self.t("cameraErrorTitle"), self.t("noCameraMessage"))
            return
        if camera != self.backgroundCamera:
            messagebox.showwarning(
                self.t("cameraChangedTitle"),
                self.t(
                    "cameraChangedMessage",
                    captured=self.backgroundCamera[0],
                    current=camera[0],
                ),
            )
            return

        self.root.withdraw()
        try:
            self.runCameraLoop(camera)
        finally:
            self.root.deiconify()

    def runCameraLoop(self, camera) -> None:
        fps = 30
        detector = DeleteMe(bgImage=self.backgroundImage, fps=fps)
        cap = openCamera(camera)
        appWindowName = "Delete Me"

        if not cap.isOpened():
            messagebox.showerror(self.t("cameraErrorTitle"), self.t("cameraErrorMessage"))
            return

        virtualCam = None
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                outputFrame = detector.deleteMe(
                    frame,
                    drawBbox=self.drawBboxVar.get(),
                )

                if self.virtualCamVar.get() and virtualCam is None:
                    height, width, _ = outputFrame.shape
                    try:
                        virtualCam = pyvirtualcam.Camera(
                            width=width,
                            height=height,
                            fps=fps,
                            fmt=pyvirtualcam.PixelFormat.BGR,
                        )
                    except RuntimeError as error:
                        messagebox.showwarning(
                            self.t("virtualCamErrorTitle"),
                            self.t("virtualCamErrorMessage", error=error),
                        )
                        self.virtualCamVar.set(False)
                if virtualCam is not None:
                    virtualCam.send(outputFrame)

                cv2.imshow(appWindowName, outputFrame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if cv2.getWindowProperty(appWindowName, cv2.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            cap.release()
            if virtualCam is not None:
                virtualCam.close()
            cv2.destroyAllWindows()

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    DeleteMeApp().run()
