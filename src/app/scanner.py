import queue
import threading

import customtkinter as ctk
import cv2
import serial
import serial.tools.list_ports as sertools
from PIL import Image
from pyzbar import pyzbar

from app import qr_hashing


class Scanner:
    """USB QR scanner using a serial/COM port."""

    def __init__(self, port, baudrate=9600, timeout=0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.lock = threading.Lock()

    @staticmethod
    def get_ports():
        return [port.device for port in sertools.comports()]

    def connect(self):
        if self.serial and self.serial.is_open:
            return

        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def disconnect(self):
        with self.lock:
            if not self.serial:
                return

            try:
                if self.serial.is_open:
                    self.serial.close()
            except (serial.SerialException, AttributeError):
                pass

            self.serial = None

    def scan(self):
        with self.lock:
            if not self.serial or not self.serial.is_open:
                return None

            if self.serial.in_waiting <= 0:
                return None

            response = self.serial.readline()

        if not response:
            return None

        return response.decode("utf-8", errors="ignore").strip()


class QRScanner(ctk.CTkToplevel):
    def __init__(self, master, controller, on_scan=None, class_id=None):
        super().__init__(master)

        self.controller = controller
        self.on_scan = on_scan
        self.class_id = class_id

        self.title("QR Scanner")
        self.geometry("800x600")
        self.minsize(640, 480)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # -----------------------------------------------------
        # Scanner state
        # -----------------------------------------------------

        self.webcam = None
        self.scanner = None

        self.running = False
        self.device_type = None
        self.device_value = None

        self.worker = None
        self.stop_event = None
        self.closed = False
        self.scan_handled = False

        # Thread -> Tkinter communication
        self.event_queue = queue.Queue()
        self.latest_frame = None
        self.frame_lock = threading.Lock()

        # Current CTkImage
        self.imgtk = None

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self._create_widgets()

        # Start device discovery in background.
        self._refresh_devices()

        # Process worker results from Tkinter's thread.
        self.after(10, self._process_queue)
        self.after(30, self._process_frame)

        self.focus_force()
        self.grab_set()

    # =========================================================
    # UI
    # =========================================================

    def _create_widgets(self):
        self.device_var = ctk.StringVar()

        self.controls = ctk.CTkFrame(self, fg_color="transparent")
        self.controls.pack(pady=20)

        self.device_menu = ctk.CTkOptionMenu(self.controls, variable=self.device_var, values=["Detecting devices..."], command=self._select_device)
        self.device_menu.pack(side="left", padx=(10, 5))

        self.refresh_button = ctk.CTkButton(self.controls, text="Refresh", width=80, command=self._refresh_devices)
        self.refresh_button.pack(side="left", padx=(5, 10))

        self.video_label = ctk.CTkLabel(self, text="Detecting scanner devices...", anchor="center")
        self.video_label.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # =========================================================
    # Device discovery
    # =========================================================

    def _get_devices(self):
        devices = [{"name": "Built-in Webcam", "type": "webcam", "value": 0}]

        for port in Scanner.get_ports():
            devices.append({"name": f"USB Scanner ({port})", "type": "serial", "value": port})

        return devices

    def _refresh_devices(self):
        """
        Start device discovery in a worker thread.
        Tkinter does not wait for COM-port enumeration.
        """

        self._stop_scanner()

        self.refresh_button.configure(state="disabled")

        self.device_menu.configure(state="disabled", values=["Detecting devices..."])

        self.device_var.set("Detecting devices...")

        self.video_label.configure(image="", text="Detecting scanner devices...")

        thread = threading.Thread(target=self._device_discovery_worker, daemon=True)

        thread.start()

    def _device_discovery_worker(self):
        devices = self._get_devices()

        self.event_queue.put(("devices", devices))

    def _handle_devices(self, devices):
        self.devices = devices

        names = [device["name"] for device in self.devices]

        self.refresh_button.configure(state="normal")

        if not names:
            names = ["No devices found"]

        self.device_menu.configure(state="normal", values=names)

        if self.devices:
            first_device = self.devices[0]["name"]

            self.device_var.set(first_device)

            self._select_device(first_device)
        else:
            self.device_var.set("No devices found")

            self.video_label.configure(image="", text="No scanner devices found")

    # =========================================================
    # Device selection
    # =========================================================

    def _select_device(self, device_name):
        self._stop_scanner()

        device = next((device for device in self.devices if device["name"] == device_name), None)

        if not device:
            return

        self.device_type = device["type"]
        self.device_value = device["value"]

        if self.device_type == "webcam":
            self._start_webcam()

        elif self.device_type == "serial":
            self._start_serial_scanner()

    # =========================================================
    # Worker management
    # =========================================================

    def _create_worker(self, target):
        self.running = True

        self.stop_event = threading.Event()

        self.worker = threading.Thread(target=target, args=(self.stop_event,), daemon=True)

        self.worker.start()

    def _stop_scanner(self):
        self.running = False

        if self.stop_event:
            self.stop_event.set()

        if self.webcam:
            self.webcam.release()
            self.webcam = None

        if self.scanner:
            self.scanner.disconnect()
            self.scanner = None

        self.stop_event = None
        self.worker = None
        self.device_type = None
        self.device_value = None

        with self.frame_lock:
            self.latest_frame = None

        if self.winfo_exists() and self.video_label.winfo_exists():
            self.video_label.configure(image="")

        self.imgtk = None

    # =========================================================
    # Webcam
    # =========================================================

    def _start_webcam(self):
        self.video_label.configure(image="", text="Starting webcam...")

        self._create_worker(self._webcam_worker)

    def _webcam_worker(self, stop_event):
        webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not webcam.isOpened():
            webcam.release()
            self.event_queue.put(("webcam_error", "Could not open webcam."))
            return

        self.webcam = webcam

        while not stop_event.is_set():
            success, frame = webcam.read()

            if not success:
                continue

            qr_codes = pyzbar.decode(frame)

            for qr in qr_codes:
                data = qr.data.decode("utf-8", errors="ignore").strip()

                if data:
                    key = qr_hashing.hash_qr(data)
                    self.event_queue.put(("scan", key))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            image = Image.fromarray(frame)

            image.thumbnail((800, 500))

            with self.frame_lock:
                self.latest_frame = image

        webcam.release()

    def _process_frame(self):
        if self.closed:
            return

        with self.frame_lock:
            image = self.latest_frame
            self.latest_frame = None

        if image is not None:
            self._display_frame(image)

        if self.winfo_exists():
            self.after(30, self._process_frame)

    def _display_frame(self, image):
        if not self.winfo_exists():
            return

        if not self.video_label.winfo_exists():
            return

        if self.device_type != "webcam":
            return

        self.imgtk = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)

        self.video_label.configure(image=self.imgtk, text="")

    # =========================================================
    # USB serial scanner
    # =========================================================

    def _start_serial_scanner(self):
        self.video_label.configure(image="", text=(f"Connecting to {self.device_value}..."))

        self._create_worker(self._serial_worker)

    def _serial_worker(self, stop_event):
        scanner = Scanner(port=self.device_value, baudrate=9600, timeout=0)

        try:
            scanner.connect()

        except serial.SerialException as error:
            self.event_queue.put(("serial_error", str(error)))

            return

        self.scanner = scanner

        self.event_queue.put(("serial_connected", self.device_value))

        while not stop_event.is_set():
            try:
                result = scanner.scan()

            except serial.SerialException as error:
                self.event_queue.put(("serial_error", str(error)))

                break

            if result:
                key = qr_hashing.hash_qr(result)
                self.event_queue.put(("scan", key))

            stop_event.wait(0.05)

    def _serial_connected(self, port):
        if not self.running:
            return
        if self.winfo_exists() and self.video_label.winfo_exists():
            self.video_label.configure(image="", text=(f"{port} connected.\n\nScan a QR code."))

    # =========================================================
    # Queue processing
    # =========================================================

    def _process_queue(self):
        try:
            while True:
                event, data = self.event_queue.get_nowait()

                if event == "devices":
                    self._handle_devices(data)

                elif event == "scan":
                    if self.winfo_exists():
                        self._on_scan(data)

                elif event == "serial_connected":
                    self._serial_connected(data)

                elif event == "serial_error":
                    self._handle_serial_error(data)

                elif event == "webcam_error":
                    self._handle_webcam_error(data)

        except queue.Empty:
            pass

        if self.winfo_exists():
            self.after(50, self._process_queue)

    # =========================================================
    # Errors
    # =========================================================

    def _handle_serial_error(self, error):
        self._stop_scanner()

        self.video_label.configure(image="", text=f"Could not open scanner:\n{error}")

    def _handle_webcam_error(self, error):
        self._stop_scanner()

        self.video_label.configure(image="", text=error)

    # =========================================================
    # Scan result
    # =========================================================

    def _on_scan(self, data):
        if self.scan_handled:
            return

        self.scan_handled = True

        if self.on_scan:
            self.on_scan(data)

        self.on_close()

    # =========================================================
    # Cleanup
    # =========================================================

    def on_close(self):
        if self.closed:
            return

        self.closed = True
        self._stop_scanner()
        self.grab_release()
        self.destroy()
