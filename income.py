from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget,QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mysql.connector
import sys

class LaporanIncome(QMainWindow):
    def __init__(self):
        super(LaporanIncome, self).__init__()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.layout.addWidget(self.canvas)
        self.setWindowTitle('Income bulanan')

    def plot_monthly_income(self):
        import matplotlib.pyplot as plt

         # Fetch monthly income data from the database
        monthly_income_data = self.fetch_monthly_income()

        # Extract months and income from the data
        months = [entry[0] for entry in monthly_income_data]
        income = [entry[1] for entry in monthly_income_data]

        # Plotting
        fig, ax = plt.subplots()
        ax.bar(months, income, color='blue')
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Income (Rp)')
        ax.set_title('Laporan Income Bulanan')

        for i, val in enumerate(income):
            ax.text(i, val + 1, str(val), ha='center', va='bottom')

        # Display the plot
        self.canvas.figure = fig
        self.canvas.draw()

        # Start Matplotlib event loop
        plt.show(block=False)


    def fetch_monthly_income(self):
        db = mysql.connector.connect(user="root", database="Hotel")
        cursor = db.cursor()

        query = "SELECT MONTH(tanggal_in) AS month, SUM(jumlah) AS total_income FROM Transaksi GROUP BY MONTH(tanggal_in)"
        cursor.execute(query)

        monthly_income_data = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return monthly_income_data