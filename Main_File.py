from Login_Registration_Form import MainWindow
from Login_Registration_Form import RegisterForm
from Dashboard import DashboardWindow
from welcome_screen import WelcomeSplashScreen
import sys
import socket
import os
from PyQt5.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QRect
from PyQt5.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QFont
#####################
##################################################################################################
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.message = ""
        self._opacity = 1.0
        self._y_pos = 0
        ##########################################
    @pyqtProperty(str)
    def text(self):
        return self.message

    @text.setter
    def text(self, message):
        self.message = message
        self.showMessage(self.message, Qt.AlignTop | Qt.AlignHCenter, QColor("#FFFFFF"))

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    @pyqtProperty(int)
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, value):
        self._y_pos = value
        self.showMessage(self.message, Qt.AlignTop | Qt.AlignHCenter, QColor("#FFFFFF"))

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_history_manager=RegisterForm()
        self.show_splash_screen()
##########################################################################################################################################################
    def show_splash_screen(self):
        screen = self.app.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        splash_image = QPixmap(screen_width, screen_height)
        painter = QPainter(splash_image)
        gradient = QLinearGradient(0, 0, 0, screen_height)
        
        # Define dark gradient colors
        gradient.setColorAt(0, QColor("#1A1A1A"))  # Darker shade
        gradient.setColorAt(0.1, QColor("#2A2A2A"))
        gradient.setColorAt(0.2, QColor("#3A3A3A"))
        gradient.setColorAt(0.3, QColor("#4A4A4A"))
        gradient.setColorAt(0.4, QColor("#5A5A5A"))
        gradient.setColorAt(0.5, QColor("#6A6A6A"))
        gradient.setColorAt(0.6, QColor("#7A7A7A"))
        gradient.setColorAt(0.7, QColor("#8A8A8A"))
        gradient.setColorAt(0.8, QColor("#9A9A9A"))
        gradient.setColorAt(0.9, QColor("#AAAAAA"))  # Lighter shade
        gradient.setColorAt(1, QColor("#BBBBBB"))
        
        painter.fillRect(splash_image.rect(), gradient)
        
        #Load the image dynamically
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))  # Set the base path
        car_icon_path = os.path.join(base_path, "dashboard_images/report_header.jpg")  # Construct the path to the image
        
        car_icon = QPixmap(car_icon_path)  # Load the image
        icon_width=1200  # Adjusted width
        icon_height=500
        icon_rect = QRect(50, screen_height // 2 - icon_height // 2, icon_width,icon_height)
        car_icon = car_icon.scaled(icon_width, icon_height, Qt.KeepAspectRatio)  # Scale the image
        painter.drawPixmap(icon_rect, car_icon)
        painter.end()
        
        self.splash = SplashScreen(splash_image)
        self.splash.show()
        
        self.opacity_animation = QPropertyAnimation(self.splash, b"opacity")
        self.opacity_animation.setDuration(1000)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.start()
        
        # Set the custom font for the welcome message
        custom_font = QFont("Algerian", 30)  # Font size set to 30
        self.splash.setFont(custom_font)  # Set the font for the splash screen
        
        # Animate the welcome text character by character
        self.welcome_message = "Welcome to the Car Inventory Application"
        self.current_char_index = 0
        self.splash.text = ""  # Start with an empty text
        
        self.text_animation_timer = QTimer()
        self.text_animation_timer.timeout.connect(self.update_welcome_text)
        self.text_animation_timer.start(200)  # Adjust the interval for speed
        
        QTimer.singleShot(10000, self.check_internet_and_start)  # 10 seconds delay

    def update_welcome_text(self):
        if self.current_char_index < len(self.welcome_message):
            self.splash.text += self.welcome_message[self.current_char_index]
            self.current_char_index += 1

    def check_internet_and_start(self):
        if self.is_internet_available():
            self.splash.close()
            self.start_application()
        else:
            self.splash.close()
            self.show_error_message("No internet connection detected. Please connect to the internet to start the application.")

    def is_internet_available(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            return True
        except OSError:
            return False

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Internet Connection Required")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        sys.exit()
######################################################################################################################################################
    def start_application(self):
        self.last_login = self.login_history_manager.get_last_login()  # Get the last login
        if self.last_login:
           email=self.last_login['email']
           password=self.last_login['password']
           self.login_user(email, password)  # Automatically login the user
        else:
            self.window = MainWindow()  # This shows the login window
            self.window.showMaximized()  # Show window in full screen
############################################################################################################################################################################################
    def login_user(self, email, password):
        self.s1=email
        self.s2=password
         # Show the welcome splash screen
        splash = WelcomeSplashScreen()
        splash.show()
        # Set a timer to close the splash screen and open the dashboard after 12 seconds
        QTimer.singleShot(1200,lambda: self.show_dashboard())
    def show_dashboard(self):
        self.window = DashboardWindow(self.s1)  # Pass email to the dashboard
        self.window.showMaximized()
##################################################################################################################################################
    def run(self):
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    application = App()
    application.run()
