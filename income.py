from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QApplication
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
        self.canvas = FigureCanvas(Figure(figsize=(10, 6)))
        self.layout.addWidget(self.canvas)
        self.setWindowTitle('Income Bulanan')

    def plot_monthly_income(self):
        import matplotlib.pyplot as plt

        # Fetch monthly income data from the database
        monthly_income_data = self.fetch_monthly_income()

        # Extract years, months, and income from the data
        years_months_income = {entry[:2]: entry[2] for entry in monthly_income_data}

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        for (year, month), income in years_months_income.items():
            ax.bar(f"{year}-{month:02d}", income, label=f"{year}-{month:02d}", alpha=0.7)

        ax.set_xlabel('Bulan-Tahun')
        ax.set_ylabel('Income (Rp)')
        ax.set_title('Laporan Income Bulanan')
        ax.legend()

        # Display the plot
        self.canvas.figure = fig
        self.canvas.draw()

        # Start Matplotlib event loop
        plt.show(block=False)

    def fetch_monthly_income(self):
        db = mysql.connector.connect(user="root", database="Hotel")
        cursor = db.cursor()

        query = """
                SELECT YEAR(tanggal_in) AS year, MONTH(tanggal_in) AS month, SUM(jumlah) AS total_income 
                FROM Transaksi 
                GROUP BY YEAR(tanggal_in), MONTH(tanggal_in)
                """
        cursor.execute(query)

        monthly_income_data = cursor.fetchall()

        db.commit()
        cursor.close()
        db.close()

        return monthly_income_data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaporanIncome()
    window.plot_monthly_income()
    window.show()
    sys.exit(app.exec_())
