import sys
import os
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QMovie, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
class WelcomeSplashScreen(QSplashScreen):
    def __init__(self):
        # Get screen geometry to cover the entire screen
        screen_geometry = QDesktopWidget().screenGeometry()
        # Load the GIF file dynamically
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))  # Set the base path
        gif_path = os.path.join(base_path, "dashboard_images/report_header.jpg")  # Construct the path to the GIF
        # Load the GIF file as a pixmap and scale it
        splash_pix = QPixmap(gif_path)
        scaled_pix = splash_pix.scaled(screen_geometry.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the splash screen with the scaled pixmap
        super().__init__(scaled_pix, Qt.WindowStaysOnTopHint)

        # Set splash screen geometry
        self.setGeometry(screen_geometry)

        # Create a label for the GIF
        self.gif_label = QLabel(self)
        self.gif_label.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        # Load and start the GIF using QMovie
        self.movie = QMovie(gif_path)  # Use the dynamically loaded GIF path
        self.gif_label.setMovie(self.movie)
        self.movie.setScaledSize(scaled_pix.size())
        self.movie.start()  # Ensure the movie starts

        # Create a label for the loading text
        self.loading_label = QLabel("Please wait, the application is starting.", self)
        self.loading_label.setStyleSheet("color:white;background-color:green;")  # Customize font size and color
        custom_font = QFont("Algerian", 30, QFont.Bold)  # Font size set to 30 and bold
        self.loading_label.setFont(custom_font)  # Set the font for the splash screen
        self.loading_label.setAlignment(Qt.AlignCenter)
        # Set the geometry of the loading label to be at the bottom of the splash screen
        self.loading_label.setGeometry(50, 620, screen_geometry.width() - 100, 50)  # Adjust height and width

        # Start the character-wise animation
        self.loading_text = self.loading_label.text()
        self.loading_label.setText("")  # Clear the label initially
        self.animate_loading_text()

        # Set a timer to close the splash screen after 12 seconds
        QTimer.singleShot(12000, self.close)  # Adjusted to match the timer in the main section

    def animate_loading_text(self):
        """Animate the loading text character by character."""
        total_duration = 1200  # 12 seconds
        duration_per_char = total_duration // len(self.loading_text)  # Duration for each character

        for i in range(len(self.loading_text) + 1):
            QTimer.singleShot(i * duration_per_char, lambda i=i: self.update_text(i))

    def update_text(self, index):
        """Update the text on the loading label up to the given index."""
        self.loading_label.setText(self.loading_text[:index])
        self.loading_label.adjustSize()  # Adjust size to fit the text

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        self.setGeometry(100, 100, 800, 600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = WelcomeSplashScreen()
    splash.show()

    # Show the main window after 12 seconds
    QTimer.singleShot(12000, lambda: MainWindow().show())

    sys.exit(app.exec_())
