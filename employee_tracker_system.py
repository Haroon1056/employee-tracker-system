import cv2
import time
import os
from PIL import ImageGrab
from plyer import notification
from pynput import keyboard, mouse
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import sys  
from datetime import datetime

# Directory to save images and screenshots
SAVE_DIR = "monitoring_data"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class MonitoringThread(QThread):
    def __init__(self):
        super().__init__()
        self.last_active_time = time.time()               
        self.running = True
        self.countdown_active = False

    def run(self):
        print("Monitoring thread started.")
        while self.running:
            time.sleep(1)  # Check every second
            if not self.countdown_active:
                inactive_user_time = time.time() - self.last_active_time
                if inactive_user_time >= 1:  # User has been inactive for 20 seconds
                    print("Starting 20-second countdown.")
                    self.start_countdown(20, self.send_notification)

    def start_countdown(self, duration, on_complete):
        self.countdown_active = True
        countdown_start_time = time.time()
        while self.countdown_active:  
            time.sleep(1)
            elapsed_time = time.time() - countdown_start_time
            remaining_time = duration - int(elapsed_time)
            if remaining_time > 0:
                print(f"Countdown: {remaining_time}")
            else:
                on_complete()
                if duration == 20:
                    print("Starting 10-second countdown for picture and screenshot.")
                    self.start_countdown(10, self.take_picture_and_screenshot)
                self.countdown_active = False
                break
            if self.is_active():
                print("Countdown interrupted by user activity.")
                self.countdown_active = False

    def is_active(self):
        return (time.time() - self.last_active_time) < 1

    def take_picture_and_screenshot(self):
        self.take_picture()
        self.take_screenshot()

    def take_picture(self):
        print("Attempting to take a picture.")
        cap = cv2.VideoCapture(0)  # Open the camera
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            picture_path = os.path.join(SAVE_DIR, f"user_picture_{timestamp}.jpg")
            cv2.imwrite(picture_path, frame)
            print(f"Picture saved at {picture_path}")
        else:
            print("Failed to capture picture.")
        cap.release()

    def take_screenshot(self):
        print("Attempting to take a screenshot.")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot = ImageGrab.grab()
        screenshot_path = os.path.join(SAVE_DIR, f"screenshot_{timestamp}.png")
        screenshot.save(screenshot_path)
        print(f"Screenshot saved at {screenshot_path}")

    def send_notification(self):
        print("Sending notification.")
        notification.notify(
            title='Activity Alert',
            message='Focus on your work!',
            timeout=5
        )
        print("Notification sent.")

    def update_last_active_time(self):
        print("Updating last active time.")
        self.last_active_time = time.time()
        self.countdown_active = False

    def stop(self):
        print("Stopping monitoring thread.")
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.monitoring_thread = MonitoringThread()

    def initUI(self):
        self.start_button = QPushButton('Start Monitoring', self)
        self.start_button.clicked.connect(self.start_monitoring)
        self.start_button.setGeometry(100, 100, 200, 50)
        self.setGeometry(100, 100, 400, 300)

    def start_monitoring(self):
        print("Starting monitoring.")
        self.monitoring_thread.start()

        # Start keyboard and mouse listeners
        self.keyboard_listener = keyboard.Listener(on_press=self.on_activity)
        self.mouse_listener = mouse.Listener(on_click=self.on_activity)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def on_activity(self, *args):
        print("User activity detected.")
        self.monitoring_thread.update_last_active_time()

    def closeEvent(self, event):
        print("Closing application.")
        self.monitoring_thread.stop()
        self.monitoring_thread.wait()  # Wait for the thread to finish
             
        # Stop listeners
        self.keyboard_listener.stop()        
        self.mouse_listener.stop()

        event.accept()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
