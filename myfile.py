import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class SupplierIDGenerator:
    def __init__(self):
        self.current_id = 0  # Initialize the counter

    def generate_dynamic_supplier_Id(self):
        if self.current_id <= 1000:  # Ensure it stays within the range
            dynamic_supplier_id = str(self.current_id)
            self.current_id += 1  # Increment the counter for the next ID
            return dynamic_supplier_id
        else:
            raise ValueError("No more IDs available within the range 0 to 1000")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.id_generator = SupplierIDGenerator()  # Instantiate the ID generator

        # Create a QLineEdit for displaying the supplier ID
        self.supplier_id = QLineEdit(self)
        self.supplier_id.setGeometry(50, 50, 200, 30)

        # Set the first supplier ID directly into the QLineEdit
        self.set_initial_supplier_id()

        # Create a QPushButton to generate a new supplier ID
        self.generate_button = QPushButton("Generate Next ID", self)
        self.generate_button.setGeometry(50, 100, 200, 30)
        self.generate_button.clicked.connect(self.on_generate_button_clicked)

    def set_initial_supplier_id(self):
        try:
            initial_id = self.id_generator.generate_dynamic_supplier_Id()
            self.supplier_id.setText(initial_id)  # Set the initial ID
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def on_generate_button_clicked(self):
        try:
            # Generate a new dynamic supplier ID
            dynamic_supplier_id = self.id_generator.generate_dynamic_supplier_Id()
            self.supplier_id.setText(dynamic_supplier_id)  # Update the QLineEdit
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Dynamic Supplier ID Generator")
    window.setGeometry(100, 100, 300, 200)
    window.show()
    sys.exit(app.exec_())
