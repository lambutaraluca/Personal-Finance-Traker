from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QFileDialog, QMessageBox, QSizePolicy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#dictionar pentru a asocia lunile scrise cu echivalentul lor in numere
luni_ntd = {
    "ianuarie": "2024-01",
    "februarie": "2024-02",
    "martie": "2024-03",
    "aprilie": "2024-04",
    "mai": "2024-05",
    "iunie": "2024-06",
    "iulie": "2024-07",
    "august": "2024-08",
    "septembrie": "2024-09",
    "octombrie": "2024-10",
    "noiembrie": "2024-11",
    "decembrie": "2024-12"
}

#functie pentru a citi datele din fisier
def load_data(nume_fisier):
    df = pd.read_csv(nume_fisier)
    return df

#functie pentru a calcula veniturile si cheltuielile totale
def calculate_totals(df):
    venit = df[df["Tip"] == "Venit"]["Suma"].sum()
    cheltuieli = df[df["Tip"] == "Cheltuiala"]["Suma"].sum()
    return venit, cheltuieli

#functie pentru a calcula veniturile si cheltuielile intr-o anumita luna
def calculate_monthly(df, luna):
    luna_c = luni_ntd[luna.lower()]
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df_luna = df[df["Data"].dt.strftime('%Y-%m') == luna_c]
    venit_m = df_luna[df_luna["Tip"] == "Venit"]["Suma"].sum()
    cheltuieli_m = df_luna[df_luna["Tip"] == "Cheltuiala"]["Suma"].sum()
    return venit_m, cheltuieli_m

#functie pentru a gasi luna cu cele mai mari cheltuieli
def cm_luna_c(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df_cheltuieli = df[df["Tip"] == "Cheltuiala"]
    df_cheltuieli["Luna"] = df_cheltuieli["Data"].dt.strftime('%Y-%m')
    luna_c = df_cheltuieli.groupby("Luna")["Suma"].sum()
    max_c = luna_c.max()
    max_luna = luna_c.idxmax()
    for nume_luna, month_num in luni_ntd.items():
            if month_num == max_luna:
                break
    return nume_luna, max_c

#functie pentru a gasi luna cu cele mai mari venituri
def cm_luna_v(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df_cheltuieli = df[df["Tip"] == "Venit"]
    df_cheltuieli["Luna"] = df_cheltuieli["Data"].dt.strftime('%Y-%m')
    luna_c = df_cheltuieli.groupby("Luna")["Suma"].sum()
    max_c = luna_c.max()
    max_luna = luna_c.idxmax()
    for nume_luna, month_num in luni_ntd.items():
            if month_num == max_luna:
                break
    return nume_luna, max_c

#functie pentru a calcula veniturile in fiecare luna
def venituri_pe_luna(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df_venituri = df[df["Tip"] == "Venit"]
    df_venituri["Luna"] = df_venituri["Data"].dt.strftime('%Y-%m')
    venituri_tot = df_venituri.groupby("Luna")["Suma"].sum().sort_index()
    return venituri_tot

#functie pentru a calcula cheltuielile in fiecare luna
def cheltuieli_pe_luna(df):
    df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')
    df_cheltuiala = df[df["Tip"] == "Cheltuiala"]
    df_cheltuiala["Luna"] = df_cheltuiala["Data"].dt.strftime('%Y-%m')
    cheltuieli_tot = df_cheltuiala.groupby("Luna")["Suma"].sum().sort_index()
    return cheltuieli_tot

#functie pentru a grupa cheltuielile pe descriere
def cheltuiala_desc(df):
    df_chelt = df[df["Tip"]== "Cheltuiala"]
    chelt_tot = df_chelt.groupby("Descriere")["Suma"].sum()
    return chelt_tot, df_chelt["Descriere"].unique().tolist()

#clasa pentru GUI ul nostru
class PersonalFinanceTracker(QWidget):
    def __init__(self):
        super().__init__()

        #crearea ferestrei
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        self.layout = QVBoxLayout()

        #creare buton pentru incarcarea fisierului
        self.load_button = QPushButton("Incarca Fisier CSV")
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

        #creare buton pentru calcularea veniturilor si cltuielilor totale
        self.total_button = QPushButton("Calculeaza venituri si cheltuieli totale")
        self.total_button.clicked.connect(self.calculate_totals)
        self.total_button.setVisible(False)
        self.layout.addWidget(self.total_button)

        #creare text pentru afisarea veniturilor si cheltuielilor
        self.total_label = QLabel("Total venituri si cheltuieli: ")
        self.total_label.setVisible(False)
        self.layout.addWidget(self.total_label)

        #creare buton pentru crearea bar chartului
        self.grafic_button_bar = QPushButton("Creeaza grafic pentru fiecare luna")
        self.grafic_button_bar.clicked.connect(self.create_grafic_bar)
        self.grafic_button_bar.setVisible(False)
        self.layout.addWidget(self.grafic_button_bar)

        #creare buton pentru crearea pie chartului
        self.grafic_button_pie = QPushButton("Creeaza grafic pentru cheltuieli")
        self.grafic_button_pie.clicked.connect(self.create_grafic_pie)
        self.grafic_button_pie.setVisible(False)
        self.layout.addWidget(self.grafic_button_pie)

        #creare lista de luni
        self.month_combo = QComboBox(self)
        self.month_combo.addItems(luni_ntd.keys())
        self.month_combo.setVisible(False)
        self.layout.addWidget(self.month_combo)

        #creare buton pentru calcularea veniturilor si cheltuielilor intr o anumita luna
        self.month_button = QPushButton("Calculeaza venituri si cheltuieli pe luna")
        self.month_button.clicked.connect(self.calculate_monthly)
        self.month_button.setVisible(False)
        self.layout.addWidget(self.month_button)

        #creare text pentru afisarea veniturilor si cheltuielilor intr o anumita luna
        self.month_label = QLabel("Venituri si cheltuieli pe luna: ")
        self.month_label.setVisible(False)
        self.layout.addWidget(self.month_label)

        #creare buton pentru gasirea lunii cu cele mai mari cheltuieli
        self.max_expenses_button = QPushButton("Luna cu cele mai mari cheltuieli")
        self.max_expenses_button.clicked.connect(self.max_cheltuieli)
        self.max_expenses_button.setVisible(False)
        self.layout.addWidget(self.max_expenses_button)

        #creare text pentru afisarea lunii cu cele mai mari cheltuieli
        self.max_expenses_label = QLabel("Luna cu cele mai mari cheltuieli: ")
        self.max_expenses_label.setVisible(False)
        self.layout.addWidget(self.max_expenses_label)

        #creare buton pentru gasirea lunii cu cele mai mari venituri
        self.max_income_button = QPushButton("Luna cu cele mai mari venituri")
        self.max_income_button.clicked.connect(self.max_venit)
        self.max_income_button.setVisible(False)
        self.layout.addWidget(self.max_income_button)

        #creare text pentru afisarea lunii cu cele mai mari venituri
        self.max_income_label = QLabel("Luna cu cele mai mari venituri: ")
        self.max_income_label.setVisible(False)
        self.layout.addWidget(self.max_income_label)

        #creare dataframe al clasei
        self.df = None
        self.setLayout(self.layout)

    #metoda pentru a incarca fisierul csv
    def load_file(self):
        #creare fereastra pentru incarcarea fisierului
        file_name, _ = QFileDialog.getOpenFileName(self, "Deschide fisier CSV", "", "CSV Files (*.csv)")
        if file_name:
            self.df = load_data(file_name)

            #crearea ferestra de confirmare pentru incarcare
            reply = QMessageBox.question(self, 'Confirmare', 'Fisierul a fost incarcat cu succes. Doriti sa continuati?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            #afiseaza butoanele ascunse si le regleaza dimensiunile
            if reply == QMessageBox.Yes:
                self.total_button.setVisible(True)
                self.total_label.setVisible(False)
                self.month_combo.setVisible(True)
                self.month_button.setVisible(True)
                self.month_label.setVisible(False)
                self.grafic_button_bar.setVisible(True)
                self.grafic_button_pie.setVisible(True)
                self.max_expenses_button.setVisible(True)
                self.max_expenses_label.setVisible(False)
                self.max_income_button.setVisible(True)
                self.max_income_label.setVisible(False)
                self.load_button.setText("Incarca un nou fisier CSV")
                self.adjust_button_sizes()

    #metoda pentru a regla dimensiunile butoanelor vizibile
    def adjust_button_sizes(self):
        buttons = [self.load_button, self.total_button, self.month_button, self.grafic_button_bar, self.grafic_button_pie, self.max_expenses_button, self.max_income_button]
        visible_buttons = [btn for btn in buttons if btn.isVisible()]
        for btn in visible_buttons:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    #metoda pentru a afisa totalurile
    def calculate_totals(self):
        venit, cheltuieli = calculate_totals(self.df)
        self.total_label.setVisible(True)
        self.total_label.setText(f"Total venituri: {round(venit, 2)} | Total cheltuieli: {round(cheltuieli, 2)}")

    #metoda pentru crearea bar chartului
    def create_grafic_bar(self):
        v = venituri_pe_luna(self.df)
        c = cheltuieli_pe_luna(self.df)
        n = 12
        r = np.arange(n)
        width = 0.25
        plt.barh(r, c, color = 'cyan', height = width, label='Cheltuieli')
        plt.barh(r + width, v, color = 'orange', height = width, label = 'Venituri')
        plt.yticks(r+(width/2), luni_ntd)
        plt.title("Cheltuieli si Venituri in fiecare luna")
        plt.ylabel("Luna") 
        plt.xlabel("Suma") 
        plt.grid(True)
        plt.legend(["Cheltuieli", "Venituri"])
        plt.show()

    #metoda pentru crearea pie chartului
    def create_grafic_pie(self):
        c, desc = cehltuiala_desc(self.df)
        plt.pie(c, labels = desc, autopct='%1.1f%%')
        plt.title("Tipuri cheltuieli")
        plt.show()
    
    #metoda pentru afisarea veniturilor si cheltuielilor intr o luna
    def calculate_monthly(self):
        luna = self.month_combo.currentText()
        venit, cheltuieli = calculate_monthly(self.df, luna)
        self.month_label.setVisible(True)
        self.month_label.setText(f"Venituri: {round(venit, 2)} | Cheltuieli: {round(cheltuieli, 2)}")

    #metoda pentru afisraea lunii cu cele mai mari cheltuieli
    def max_cheltuieli(self):
        luna, suma = cm_luna_c(self.df)
        self.max_expenses_label.setVisible(True)
        self.max_expenses_label.setText(f"Luna cu cele mai mari cheltuieli este {luna} cu suma {round(suma, 2)}")

    #metoda pentru afisarea lunii cu cele mai mari venituri
    def max_venit(self):
        luna, suma = cm_luna_v(self.df)
        self.max_income_label.setVisible(True)
        self.max_income_label.setText(f"Luna cu cele mai mari venituri este {luna} cu suma {round(suma, 2)}")

#rularea programului
if __name__ == "__main__":
    app = QApplication([])
    window = PersonalFinanceTracker()
    window.show()
    app.exec_()