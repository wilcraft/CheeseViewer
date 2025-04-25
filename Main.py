import sys,csv,random,requests
from bs4 import BeautifulSoup
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


#CONSTS
LEFT = Qt.AlignmentFlag.AlignLeft
RIGHT = Qt.AlignmentFlag.AlignRight
TOP = Qt.AlignmentFlag.AlignTop
BOTTOM = Qt.AlignmentFlag.AlignBottom
CENTER = Qt.AlignmentFlag.AlignCenter


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Cheese Software")
        width = 800
        height = 500

        self.setFixedSize(width, height)
        self.cheese_info = QLabel(self)
        self.cheese_info.setAlignment(TOP)
        self.cheese_description = QLabel(self)
        self.cheese_description.setAlignment(TOP)
        self.cheese_description.setWordWrap(True)
        self.cheese_image = QLabel(self)
        self.pixmap = QPixmap('images/placeholder.jpg')
        self.cheese_image.setPixmap(self.pixmap)
        self.cheese_image.setFixedSize(400,400)

        self.exit_button = QPushButton("Exit", self)
        self.cheese_button = QPushButton("Show Cheese", self)

        self.exit_button.clicked.connect(self.close)
        self.cheese_button.clicked.connect(self.show_cheese)
        self.exit_button.setStyleSheet('QPushButton {color: red;}')
        self.cheese_button.setStyleSheet('QPushButton {color: green;}')
        self.cheese_image.setAlignment(CENTER)

        #self.cheese_country.setStyleSheet("QLabel {background-color: red;}")
        self.cheese_info.setStyleSheet("QLabel {font-size: 14pt;}")
        self.cheese_description.setStyleSheet("QLabel {font-size: 10pt;}")


        sub_window_one = QWidget(self)

        main_layout = QGridLayout()
        layout = QVBoxLayout()
        info_layout = QVBoxLayout()
        #row, column
        #layout.addWidget(self.button,3,0)
        #layout.addWidget(self.button2,1,0)
        layout.addWidget(self.cheese_image)
        layout.addWidget(self.cheese_button)
        layout.addWidget(self.exit_button)
        #layout.addLayout(info_layout)

        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(0)

        info_layout.addWidget(self.cheese_info)
        info_layout.addWidget(self.cheese_description)

        main_layout.addLayout(info_layout,0,0)
        main_layout.addLayout(layout,0,1)
        sub_window_one.setLayout(main_layout)

        self.setCentralWidget(sub_window_one)
        self.show()

    @Slot()
    def show_cheese(self):
        with open('Text_Files/cheese_details_new.csv', newline='', errors='ignore') as csvfile:
            reader = csv.reader(csvfile)
            random_cheese = random.choice(list(reader))
            URL = random_cheese[0]
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            #info
            name = soup.find('div', class_='unit').find('h1').text
            self.cheese_info.setText(f'Name: {name} \nMilk Type: {random_cheese[1].title()}\nCountry: {random_cheese[2]}\nRegion: {random_cheese[3].replace('NA', 'No Information')}\n'
                                     f'Family: {random_cheese[4].replace('NA', 'No Information')}\nType: {random_cheese[5].title()}\n'
                                     f'Texture: {random_cheese[9].replace('NA', 'No Information').title()}\nFlavour: {random_cheese[12].replace('NA', 'No Information').title()}' )
            #description
            description = soup.find('div', class_='description').find('p').text
            self.cheese_description.setText(f'Description:\n{description}')
            #image
            img_link = soup.find('div', class_='cheese-image-border').find('img')['src']
            temp_img = QImage()
            temp_img.loadFromData(requests.get('https://www.cheese.com'+img_link).content)
            self.cheese_image.setScaledContents(True)
            self.cheese_image.setPixmap(QPixmap(temp_img))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
