from Dashboard import DashboardWindow
from welcome_screen import WelcomeSplashScreen
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QProgressBar,
    QStackedWidget, QHBoxLayout, QFrame, QDateEdit, QProgressDialog, QDialog, QMessageBox, QGraphicsView,QFileDialog
)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF,QBuffer
import sys
from PyQt5.QtGui import QFont, QPixmap, QIcon, QPainter, QColor, QBrush, QTransform
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF,QRect,QDate
from google.cloud import firestore
import os
import re
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QPainter, QColor,QMovie
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRectF
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
import io
import base64
from PyQt5.QtWidgets import QMessageBox
import json
import bcrypt
from datetime import datetime,timedelta, timezone
from qt_material import apply_stylesheet  # Import qt-material
#################################################################################################################################################################
# Set environment variable for Firestore credentials
# Determine the path to the serviceAccountKey.json file
if getattr(sys, 'frozen', False):
    # If running in a bundle (exe), get the application path
    application_path = sys._MEIPASS
    service_account_path = os.path.join(application_path, 'serviceAccountKey.json')
else:
    # If running in a normal Python environment, set the path directly
    service_account_path = "serviceAccountKey.json"  # Ensure this path is correct
# Set environment variable for Firestore credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
# Initialize Firestore
db = firestore.Client()
splash = None
#####################################################################################################################
#Function to create a custom dialog with centered OK button
def show_custom_message(parent, message, title, is_success=True):
    # Create a QDialog for custom layout
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    # Set fixed height and width for the dialog
    dialog.setFixedHeight(120)  
    dialog.setFixedWidth(550)  
    # Set dialog layout
    layout = QVBoxLayout()
    # Add message label
    label = QLabel(message)
    layout.addWidget(label, alignment=Qt.AlignCenter)
    # Add OK button to the center
    button_box = QDialogButtonBox(QDialogButtonBox.Ok)
    # Use lambda to connect both dialog.accept and hide_loader
    button_box.accepted.connect(lambda: [dialog.accept(), parent.hide_loader()])
    # Add the button to the layout and center it
    layout.addWidget(button_box, alignment=Qt.AlignCenter)

    # Set layout and custom style
    dialog.setLayout(layout)

    # Set custom styles
    dialog.setStyleSheet(f"""
        QDialog {{
            background-color: {"#e0f7fa" if is_success else "#ffebee"};
            border: 0px solid {"green" if is_success else "red"};
            border-radius: 10px;
        }}
        QLabel {{
            color: black;
            font-size: 16px;
        }}
        QPushButton {{
            background-color: {"#81c784" if is_success else "#e57373"};
            color: white;
            padding: 8px 16px;
            border-radius: 5px;
        }}
    """)

    # Execute dialog
    dialog.exec_()
##############################################################################################################
# Ensure CircularLoader class is defined or imported
class CircularLoader(QWidget):
    def __init__(self, gif_path, parent=None):
        super().__init__(parent)
        self.gif_label = QLabel(self)
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.movie = QMovie(gif_path)
        self.gif_label.setMovie(self.movie)
        self.movie.start()
        layout = QVBoxLayout()
        layout.addWidget(self.gif_label)
        self.setLayout(layout)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: white;")
############################################################################
class LoginForm(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.parent_window = parent  # Store reference to the parent window
        self.init_ui()
    def init_ui(self):
        # Main Layout for the form
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 50)  # Adjust margins as needed
        main_layout.setSpacing(20)

        # Header frame with background color fully attached to the top
        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("background-color:#42a5f5;")  # Set background color

        header_label = QLabel("Car Inventory Management System")
        header_label.setFont(QFont('Times New Roman', 18, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white;")

        header_layout = QVBoxLayout()
        header_layout.addWidget(header_label)
        header_frame.setLayout(header_layout)

        # Title label for the login form
        title_label = QLabel("Login Form")
        title_label.setFont(QFont('Times New Roman (Headings CS)',25,QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter|Qt.AlignLeft)
        title_label.setStyleSheet("color:#42a5f5;")
        title_label.setContentsMargins(0,0,40,0)

        # Form layout for email and password
        form_layout = QFormLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email ID")
        self.email_input.setFixedHeight(50)
        self.email_input.setFixedWidth(300)
        self.email_input.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(50)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        form_layout.addRow(self.email_input)
        form_layout.addRow(self.password_input)
        # Login button
        login_button = QPushButton("Login")
        login_button.setFixedHeight(40)
        login_button.setFixedWidth(300)
        login_button.setStyleSheet("background-color:#42a5f5;font-weight:bold;color:white;font-size:16px;border-radius:20px;")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.on_register_click)
        # New user link
        new_user_layout = QHBoxLayout()
        new_user_label = QLabel("New user?")
        register_button = QPushButton("Register")
        register_button.setStyleSheet("background: none; color: #007bff; text-decoration: underline;")
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.show_register_form)
        new_user_layout.addWidget(new_user_label,alignment=Qt.AlignCenter)
        new_user_layout.addWidget(register_button,alignment=Qt.AlignCenter)
        new_user_layout.addStretch(20)
        new_user_layout.setContentsMargins(90,0,0,90)
        # Create the card layout
        card_layout = QHBoxLayout()
        card_frame = QFrame()
        card_frame.setFixedSize(900, 450)
        card_frame.setStyleSheet("background-color:#FFFFFE; border-radius: 10px;")
        card_frame.setFrameShape(QFrame.StyledPanel)
        # Add image to the left side of the card
        ###########################################################################################################
        #image_label = QLabel()
        #pixmap = QPixmap('Images/Frame 422.png')  # Replace with the path to your login image
        #image_label.setPixmap(pixmap)
        #image_label.setAlignment(Qt.AlignCenter)
        ################################################################
        # Set the base path
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        # Construct the path to the login image
        login_image_path = os.path.join(base_path, "Images", "Frame 422.png")  # Adjust the path to your login image
        # Create a QLabel and set the pixmap
        image_label = QLabel()
        pixmap = QPixmap(login_image_path)  # Use the constructed path for the login image
        image_label.setPixmap(pixmap)
        ######################################################################################################
        # Layout to hold the form
        form_container_layout = QVBoxLayout()
        form_container_layout.setContentsMargins(0,0,30,0)  # Adjust the right margin for better spacing
        form_container_layout.addWidget(title_label)
        form_container_layout.addLayout(form_layout)
        form_container_layout.addWidget(login_button)
        form_container_layout.addLayout(new_user_layout)
        form_container_layout.addStretch()
        # Adding the image and form to the card layout
        card_layout.addWidget(image_label)
        card_layout.addLayout(form_container_layout)
        card_layout.setSpacing(20)
        card_frame.setLayout(card_layout)
        # Center the card frame in the main layout
        main_layout.addWidget(header_frame)  # Add the header at the top, flush with the border
        main_layout.addStretch()
        main_layout.addWidget(card_frame, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
##################################################################################################################################
####################################################################################################################################
    def show_register_form(self):
        # Switch to register form
        self.parent().setCurrentIndex(1)
################################################################################################################################
    def on_register_click(self):
        # Show loader immediately
        self.show_loader()
        # Use QTimer to delay registration logic
        QTimer.singleShot(2000,self.login_user)  # Adjust the time (3000 ms = 3 seconds)
    def show_loader(self):
        # Show the loader
        #####################################
        #Set the base path
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        # Construct the path to the GIF
        gif_path = os.path.join(base_path, "Images/my.gif")  # Adjust the path to your GIF
        # Set the GIF loader
        self.loader = CircularLoader(gif_path, self)  # Use the constructed path for the GIF
        ######################################################
        #self.loader = CircularLoader('Images/my.gif', self)  # Adjust your GIF path
        self.loader.setGeometry(793,420,100,100)  # Adjust position and size as needed
        self.loader.setFixedSize(230,90)  # Set a fixed size for the loader
        self.loader.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the loader is cleaned up when closed
        self.loader.show()
    def hide_loader(self):
        # Ensure loader is properly deleted and can be shown again
        if hasattr(self, 'loader') and self.loader is not None:
            self.loader.close()
            self.loader = None
    def show_custom_message(self, message, title, is_success=True):
        show_custom_message(self, message, title, is_success)
    #########################################################################################################################
    def clear_form(self):
        # Clear username input
        self.password_input.clear()
        # Clear email input
        self.email_input.clear()
    ######################################################################################################################
    def Firestore_login_history(self, email, password):
        self.m1 = email
        self.m2 = password
        utc_time = datetime.now(timezone.utc)
        pakistan_time = utc_time + timedelta(hours=5)
        login_timestamp = pakistan_time.strftime('%Y-%m-%d %I:%M:%S %p')
        data = {
            'email_id': self.m1,
            'password': self.m2,
            'login_time': login_timestamp  # Store the login timestamp in Pakistan time
        }
        existing_user = db.collection('Login').where('email_id', '==', self.m1).stream()
        if any(existing_user):  # Check if there are any existing records
            return
        try:
            doc_ref = db.collection('Login').add(data)
            document_id = doc_ref[1].id  # Get the auto-generated document ID
            db.collection('Login').document(document_id).update({'document_id': document_id})
            ###########################################################################
            #Create an instance of RegisterForm and call add_login_credentials1
            register_form=RegisterForm()
            register_form.add_login_credentials1(self.m1, self.m2, document_id)
        except Exception as e:
            self.show_custom_message(f"Error recording login history: {e}", "Error", is_success=False)
    #######################################################################################################
#################################################################################################################################
    def login_user(self):
        # Initialize loading dialog
        # Proceed with login process
        email_id = self.email_input.text()
        password = self.password_input.text()
        # Define regular expressions for validation
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{3,}$'
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        # Validate email
                # Check for empty fields
        if  not email_id or not password:
            self.hide_loader()
            self.show_custom_message("All fields are required.", "Error", is_success=False)
            return
        if not re.match(email_regex, email_id):
            self.hide_loader()
            self.show_custom_message("Invalid Email ID! Please enter a valid email address.","Error",is_success=False)
            #self.loading_dialog.close()  # Close loading dialog
            return

        # Validate password
        if not re.match(password_regex, password):
            self.hide_loader()
            self.show_custom_message("Invalid Password! Please enter a valid password.","Error",is_success=False)
            return
        # Authenticate the user
        try:
            user_ref = db.collection('Users').where('email_id', '==', email_id).where('password', '==', password).get()
            if user_ref:
                ########################################################
                self.hide_loader()
                self.show_custom_message("Login Successfully","Success")
                self.Firestore_login_history(email_id,password)
                self.user_login_history(email_id,password)
                self.clear_form()
                self.parent_window.hide()  # Hide the main window
                #self.show_dashboard(email_id)
                self.Showing_Form(email_id)
            else:
                self.hide_loader()
                self.show_custom_message("Invalid email or password! Please try again.","Error",is_success=False)  # Close loading dialog
        except Exception as e:
            self.hide_loader()
            self.show_custom_message(f"Error during login: {e}", "Error", is_success=False)
    ###########################################################
    def user_login_history(self,email,password_data):
        self.regis=RegisterForm()
        self.regis.add_login_credentials(email,password_data)
    ##################################################################
    def Showing_Form(self,email):
        self.my_email=email        
         # Show the welcome splash screen
        splash = WelcomeSplashScreen()
        splash.show()
        # Set a timer to close the splash screen and open the dashboard after 12 seconds
        QTimer.singleShot(1100,lambda: self.show_dashboard())
    ##############################################
    def show_dashboard(self):
        self.window = DashboardWindow(self.my_email)  # Pass email to the dashboard
        self.window.showMaximized()
################################################################################################################################
#################################################################################################################################
class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        ######################################################################### 
        ###############################################################################
    def init_ui(self):
        # Main Layout for the form
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        main_layout.setSpacing(0)
        self.setStyleSheet("background-color: #f0f0f0; color: black;")

        # Header frame with background image fully attached to the top
        header_frame = QLabel()
        header_frame.setFixedHeight(80)
        ################################################################################
        # Set the base path
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        # Construct the path to the header image
        header_image_path = os.path.join(base_path, "Images/Header.png")  # Adjust the path to your header image
        # Load the header image
        pixmap = QPixmap(header_image_path)  # Use the constructed path for the header image
        header_frame.setPixmap(pixmap)
        ###################################################
        header_frame.setAlignment(Qt.AlignCenter)
        # Create the card layout
        card_layout = QVBoxLayout()  # Use VBoxLayout for main card layout
        card_frame = QFrame()
        #card_frame.setFixedSize(900,530)
        card_frame.setFixedSize(900,550)
        ##############################################################################################################################################33
        ##########################################################################################################################################
        # Construct the base path, considering if the application is bundled with PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))  
        # Construct the path to the background image
        background_image_path = os.path.join(base_path, "Images", "Blur_image.png")  # Ensure "Blur_image.png" is the correct filename

        # Check if the image exists
        if os.path.isfile(background_image_path):
            # Apply the stylesheet with the constructed image path
            card_frame.setStyleSheet(f"""
                QFrame {{
                    border-radius: 10px;
                    /* Background Image */
                    background-image: url('{background_image_path.replace("\\", "/")}'); /* Ensure slashes are forward */
                    background-repeat: no-repeat;
                    background-position: center;
                }}
            """)
            card_frame.setFrameShape(QFrame.StyledPanel)
        else:
            # Log a warning and set a default background color or style
            print(f"Warning: The image file was not found at the path: {background_image_path}")
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightgray; /* Set a default color or alternative styling */
                    border-radius: 10px;
                }
            """)
        ############################################################################################################################################
        ##############################################################################################################################################33
        # Title label for the registration form
        title_label = QLabel("Create New Account")
        title_label.setFont(QFont('Times New Roman (Headings CS)',14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)  # Center the title
        title_label.setContentsMargins(0, 20, 0, 10)  # Add margin for spacing
        title_label.setStyleSheet("color:#42a5f5;")
        #Logo label
        ##########################################################################################
        self.logo_label = QLabel(self)
        self.logo_label.setFixedSize(130,130)
        self.logo_label.setStyleSheet("""
            background-color: darkgrey;
            border-radius:65px;
            border:6px solid darkgrey;
        """)
        self.logo_label.setAlignment(Qt.AlignCenter)
        ################################################################################################################################################
        #self.logo_label.setPixmap(QPixmap("Images/Admin_image.png").scaled(150,150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        #self.logo_label.mousePressEvent = self.upload_image  # Event for image upload
        ###############################################################################################################
        # Set the base path
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))  
        # Construct the path to the admin image
        admin_image_path = os.path.join(base_path, "Images/Admin_image.png")  # Adjust the path to your image
        # Set the pixmap for the logo label
        self.logo_label.setPixmap(QPixmap(admin_image_path).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # Event for image upload
        self.logo_label.mousePressEvent = self.upload_image

        ###############################################################################################
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setFixedWidth(265)                       #=>color:#afafb2
        self.username_input.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.username_input.setAlignment(Qt.AlignCenter)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setFixedHeight(40)
        self.email_input.setFixedWidth(265)                    #=>color:#afafb2
        self.email_input.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.email_input.setAlignment(Qt.AlignCenter)

        # Password input
        self.password_input=QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(40)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(265)                     #=>color:#afafb2
        self.password_input.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.password_input.setAlignment(Qt.AlignCenter)

        # Confirm Password input
        self.password_input1 = QLineEdit()
        self.password_input1.setPlaceholderText("Confirm Password")
        self.password_input1.setFixedHeight(40)
        self.password_input1.setEchoMode(QLineEdit.Password)
        self.password_input1.setFixedWidth(265)             #=>color:#afafb2
        self.password_input1.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.password_input1.setAlignment(Qt.AlignCenter)

        # Registration date
        self.registration_date=QDateEdit()
        self.registration_date.setDisplayFormat("yyyy-MM-dd")
        #Set the latest date (current date)
        self.registration_date.setDate(QDate.currentDate())
        self.registration_date.setCalendarPopup(True)
        self.registration_date.setFixedHeight(40)
        self.registration_date.setFixedWidth(265)                    #=>color:#afafb2
        self.registration_date.setStyleSheet("background-color:white;color:black;font-size:14px;font-weight:bold;padding:10px;border-radius:20px;border:3px solid #afafb2;")
        self.registration_date.setAlignment(Qt.AlignCenter)

        # Register button
        register_button = QPushButton("Create Account")
        register_button.setFixedHeight(40)
        register_button.setFixedWidth(265)
        register_button.setStyleSheet("background-color:#42a5f5;color:white; font-size: 16px; border-radius:20px;")
        register_button.setFont(QFont('Times New Roman (Headings CS)',14, QFont.Bold))
        register_button.setCursor(Qt.PointingHandCursor)
        register_button.clicked.connect(self.on_register_click)

        # Existing user link
        existing_user_layout = QHBoxLayout()
        existing_user_layout.setAlignment(Qt.AlignCenter)

        existing_user_label = QLabel("Already have an account?")
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background:none;color:#007bff;text-decoration:underline;border-radius:20px;")
        login_button.setCursor(Qt.PointingHandCursor)
        login_button.clicked.connect(self.show_login_form)

        existing_user_layout.addWidget(existing_user_label)
        existing_user_layout.addWidget(login_button)

        # Adding the components to the layout
        card_inner_layout = QVBoxLayout()
        card_inner_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(self.email_input, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(self.password_input1, alignment=Qt.AlignCenter)
        card_inner_layout.addWidget(self.registration_date, alignment=Qt.AlignCenter)
        card_inner_layout.addSpacing(20)
        card_inner_layout.addWidget(register_button, alignment=Qt.AlignCenter)
        card_inner_layout.addLayout(existing_user_layout)
        card_inner_layout.addStretch()
        card_frame.setLayout(card_inner_layout)
        main_layout.addWidget(header_frame)
        main_layout.addStretch()
        main_layout.addWidget(card_frame, alignment=Qt.AlignCenter)
        main_layout.addStretch()
        self.setLayout(main_layout)
#######################################################################
    def rotate_and_apply_circular_mask(self, pixmap):
        fixed_size = 120  # Fixed size for the label
        # Step 1: Crop to a square and resize to fixed size
        size = min(pixmap.width(), pixmap.height())
        square_pixmap = pixmap.copy(0, 0, size, size)
        resized_pixmap = square_pixmap.scaled(fixed_size, fixed_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        # Step 2: Rotate by 90 degrees
        transform = QTransform().rotate(360)
        rotated_pixmap = resized_pixmap.transformed(transform, Qt.SmoothTransformation)
        # Step 3: Apply circular mask
        mask = QPixmap(fixed_size, fixed_size)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(0, 0, fixed_size, fixed_size)
        painter.end()
        rotated_pixmap.setMask(mask.createMaskFromColor(Qt.transparent, Qt.MaskInColor))
        return rotated_pixmap

    def upload_image(self, event):
        image_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if image_path:
            pixmap = QPixmap(image_path)
            circular_pixmap = self.rotate_and_apply_circular_mask(pixmap)
            self.logo_label.setPixmap(circular_pixmap)
    #####################################################################################
    def clear_form(self):
        # Clear username input
        self.username_input.clear()
        # Clear email input
        self.email_input.clear()
        # Clear password input
        self.password_input.clear()
        # Clear confirm password input
        self.password_input1.clear()
####################################################################################
    def get_image_data_from_label(self):
        # Convert the image in the logo label to base64
        pixmap = self.logo_label.pixmap()
        if pixmap:
            image = pixmap.toImage()

            # Create a QBuffer to hold the image data
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            
            # Save the image to the buffer as PNG
            image.save(buffer, 'PNG')

            # Encode the image data as base64
            image_data = base64.b64encode(buffer.data()).decode('utf-8')
            return image_data

        return None
#############################################################################################################
    def show_login_form(self):
        # Switch to login form
        self.parent().setCurrentIndex(0)
#############################################
###############################################################################################################
    def on_register_click(self):
        # Show loader immediately
        self.show_loader()
        # Use QTimer to delay registration logic
        QTimer.singleShot(3000, self.register_user)  # Adjust the time (3000 ms = 3 seconds)

    def show_loader(self):
        # Show the loader
        ################################################################
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        # Construct the path to the GIF
        gif_path = os.path.join(base_path, "Images/my.gif")  # Adjust the path to your GIF
        # Set the GIF path for the CircularLoader
        self.loader = CircularLoader(gif_path, self)  # Use the constructed path for the GIF
        ########################################################################
        #self.loader = CircularLoader('Images/my.gif', self)  # Adjust your GIF path
        self.loader.setGeometry(570,185,200,200)  # Adjust position and size as needed
        self.loader.setFixedSize(230,90)  # Set a fixed size for the loader
        self.loader.setAttribute(Qt.WA_DeleteOnClose)  # Ensure the loader is cleaned up when closed
        self.loader.show()

    def hide_loader(self):
        # Ensure loader is properly deleted and can be shown again
        if hasattr(self, 'loader') and self.loader is not None:
            self.loader.close()
            self.loader = None
############################################################################################
#############################################################################################
    def show_custom_message(self, message, title, is_success=True):
        show_custom_message(self, message, title, is_success)
#############################################################################################
    def register_user(self):
        ###############################################################
        full_name = self.username_input.text()
        email_id = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.password_input1.text()
        registration_date = self.registration_date.text()

        # Define regular expressions for validation
        full_name_regex=r'^[A-Za-z0-9\s]{3,}$'
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{3,}$'
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'
        # Check for empty fields
        if not full_name or not email_id or not password or not confirm_password or not registration_date:
            self.hide_loader()
            self.show_custom_message("All fields are required.", "Error", is_success=False)
            return
        # Validate full name
        if not re.match(full_name_regex, full_name):
            self.hide_loader()
            self.show_custom_message("Full Name must be at least 3 letters.", "Error", is_success=False)
            return

        # Validate email
        if not re.match(email_regex, email_id):
            self.hide_loader()
            self.show_custom_message("Invalid email format.", "Error", is_success=False)
            return 

        # Validate password
        if not re.match(password_regex, password):
            self.hide_loader()
            self.show_custom_message("Password must be at least 8 characters with letters and numbers.", "Error", is_success=False)
            return

        if password != confirm_password:
            self.hide_loader()
            self.show_custom_message("Passwords do not match.", "Error", is_success=False)
            return

                # Convert the image to base64
        image_data=self.get_image_data_from_label()
        data = {
            'full_name': full_name,
            'email_id': email_id,
            'password': password,
            'confirm_password': confirm_password,
            'registration_date': registration_date,
            'profile_image':image_data  # Include the image data
        }
        ####################################
        # Check if the user already exists
        existing_user = db.collection('Users').where('email_id', '==', email_id).get()
        if existing_user:
            self.hide_loader()
            self.show_custom_message("User already exists! Please use another email address.", "Error",is_success=False)
            return
        # Add data to Firebase Firestore
        #self.hide_loader()
        try:
            doc_ref = db.collection('Users').add(data)
            document_id = doc_ref[1].id  # Get the document ID
            db.collection('Users').document(document_id).update({'document_id': document_id})
            #################################################################
            # Display a styled loading message box
            self.hide_loader()
            ##################################################################
            self.show_custom_message("Registration successful!", "Success", is_success=True)
            self.clear_form()
            # Redirect to login form after success
            self.redirect_to_login_form()
        except Exception as e:
            self.hide_loader()
            self.show_custom_message(f"Error adding document: {e}",is_success=False)
####################################################################################################################################################################
    def redirect_to_login_form(self):
        self.parent().setCurrentIndex(0)  # Assuming you have a login form object defined
##########################################################################################################################################################
    #############################################################################################################
    def get_login_history_directory(self):
        #Get the path to the user's desktop directory and create "User Login History" folder
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
        login_history_dir = os.path.join(desktop_path, 'User Login History')
        # Create the directory if it doesn't exist
        if not os.path.exists(login_history_dir):
            os.makedirs(login_history_dir)
        return login_history_dir
    ####################################################################################################################
    def get_login_history_file(self):
        # Construct the path to the JSON file within the "User Login History" folder on the desktop
        return os.path.join(self.get_login_history_directory(), 'login_history.json')
    ###########################################################################################################################
    def get_login_history_file1(self):
        return os.path.join(self.get_login_history_directory(), 'login_history1.json')
    ###############################################################################################################################
    def add_login_credentials1(self, email, password, document_id):
        try:
            # Use the updated path for the login history file
            login_history_file1 = self.get_login_history_file1()
            # Load existing login history or create a new one
            if os.path.exists(login_history_file1):
                with open(login_history_file1, 'r') as file:
                    login_history = json.load(file)
            else:
                login_history = []
            # Check if the combination of email, password, and document_id already exists
            if not any(entry['email'] == email and entry['password'] == password and entry['document_id'] == document_id for entry in login_history):
                # Add the new login credentials if they don't exist
                login_history.append({'email': email, 'password': password, 'document_id': document_id})
                # Write the updated data to the JSON file
                with open(login_history_file1, 'w') as file:
                    json.dump(login_history, file)
            else:
                print("Duplicate entry detected. Skipping addition.")
        except PermissionError:
            print(f"Permission denied: Unable to write to {login_history_file1}. Please check file permissions.")
    ##################################################################################################################################################
    def get_document_id(self):
        try:
            # Use the path for the login history file
            login_history_file1 = self.get_login_history_file1()
            # Check if the login history file exists
            if os.path.exists(login_history_file1):
                with open(login_history_file1, 'r') as file:
                    login_history = json.load(file)
                # Check if there are any records in the login history
                if login_history:
                    # Return the document_id from the first record
                    return login_history[0].get('document_id')
            # Return None if no records exist
            return None
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"An error occurred while reading the login history file: {e}")
            return None
    ############################################################################################################################
    def add_login_credentials(self, email, password):
        try:
            # Use the updated path for the login history file
            login_history_file = self.get_login_history_file()

            # Load existing login history or create a new one
            if os.path.exists(login_history_file):
                with open(login_history_file, 'r') as file:
                    login_history = json.load(file)
            else:
                login_history = []
            
            # Add the new login credentials
            login_history.append({'email': email, 'password': password})
            
            # Write the updated data to the JSON file
            with open(login_history_file, 'w') as file:
                json.dump(login_history, file)
        except PermissionError:
            print(f"Permission denied: Unable to write to {login_history_file}. Please check file permissions.")
    ################################################################################################################
    def get_last_login(self):
        try:
            # Use the updated path for the login history file
            login_history_file = self.get_login_history_file()

            # Check if the file exists before trying to open it
            if not os.path.exists(login_history_file):
                print(f"File not found: {login_history_file}. Please check if the file exists.")
                return None

            with open(login_history_file, 'r') as file:
                login_history = json.load(file)
            return login_history[-1] if login_history else None

        except PermissionError:
            print(f"Permission denied: Unable to read {login_history_file}. Please check file permissions.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {login_history_file}. The file may be corrupted.")
            return None
    ##################################################################################################
    def clear_login_history(self):
        try:
            # Use the updated path for the login history file
            login_history_file = self.get_login_history_file()

            # Clear the contents of the login history file
            with open(login_history_file, 'w') as file:
                json.dump([], file)  # Write an empty list to clear the records
            print(f"Login history cleared from '{login_history_file}'.")
        except PermissionError:
            print(f"Permission denied: Unable to clear {login_history_file}. Please check file permissions.")
    ##################################################################################################
    def clear_login_history_file1(self):
        login_history_file1 = self.get_login_history_file1()
        try:
            # Open the file in write mode and write an empty list to clear its contents
            with open(login_history_file1, 'w') as file:
                json.dump([], file)  # Clear the file by writing an empty list
            print(f"{login_history_file1} has been cleared.")
        except PermissionError:
            print(f"Permission denied: Unable to write to {login_history_file1}. Please check file permissions.")
    #######################################################################
#########################################################################################################################################################3
#########################################################################################################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Management System")
        self.setGeometry(100, 100, 1100, 800)

        # Central stacked widget
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        ########################################################################################################################
        # Initialize CircularLoader
        #################
        # Login and Register forms
        self.login_form = LoginForm(self)
        self.register_form = RegisterForm()
        ##self.register_form.show()

        # Add widgets to stacked widget
        self.central_widget.addWidget(self.login_form)
        self.central_widget.addWidget(self.register_form)

        # Set the login form as the initial view
        self.central_widget.setCurrentWidget(self.login_form)
if __name__ == '__main__':
    app=QApplication(sys.argv)
    Login_window=MainWindow()
    Login_window.showMaximized()  # Show window in full screen
    sys.exit(app.exec_())
