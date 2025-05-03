#create the Easy Editor photo editor here!+
import os
from PyQt5.QtWidgets import(
    QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout 
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle('Easy Editor')
lb_image = QLabel('Image')
btn_dir = QPushButton('Folder')
lw_files = QListWidget()

btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_flip = QPushButton('Mirror')
btn_sharp = QPushButton('Sharpness')
btn_bw = QPushButton('B/W')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workir = ''
def filter(files, extentions):
    result = []
    for filename in files:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)
    return result        

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extentions = ['.jpg', '.jpeg', '.png', '.jif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extentions)
    lw_files.clear()
    for filename in filenames :
        lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.dir = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path= os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.SaveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.SaveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)    

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.SaveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)    
   
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.SaveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)   

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.SaveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.ShowImage(image_path)   

    def SaveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def ShowImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio )
        lb_image.setPixmap(pixmapimage)  
        lb_image.show()  
    
workimage = ImageProcessor()

def ShowChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.ShowImage(image_path)

lw_files.currentRowChanged.connect(ShowChosenImage)

btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)
app.exec()