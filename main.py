#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/3/25
# @original Author : Chen Shan
# @edit Author : LinkX
# Function :GUI programming - a naive Sketchpad tool

import copy
import os
import platform
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np


class myMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(800, 300, 500, 500)
        self.setWindowTitle("draw")
        self.pix = QPixmap()
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        # 初始化参数
        self.initData()
        # 清空画布
        self.initView()
        # 菜单栏

        self.fileMenu = self.menuBar().addMenu("文件")
        self.Menu = self.menuBar().addMenu("菜单")


        # 清空
        self.ClearAction = QAction(QIcon("images/clear.png"), "清空", self)
        self.ClearAction.triggered.connect(self.initView)
        self.Menu.addAction(self.ClearAction)

        # 调画笔颜色
        self.changeColor = QAction(QIcon("images/icon.png"), "颜色", self)
        self.changeColor.triggered.connect(self.showColorDialog)
        self.Menu.addAction(self.changeColor)

        # 调画笔粗细
        self.changeWidth = QAction(QIcon("images/width.png"), "宽度", self)
        self.changeWidth.triggered.connect(self.showWidthDialog)
        self.Menu.addAction(self.changeWidth)

        # 设置采样点间隔
        self.sampleInterval = QAction(QIcon("images/Sample.png"), "采样间距", self)
        self.sampleInterval.triggered.connect(self.showSampleDialog)
        self.Menu.addAction(self.sampleInterval)

        # 各种动作
        self.fileOpenAction = QAction(QIcon("images/fileopen.png"), "&Open Image", self)
        self.fileOpenAction.setShortcut(QKeySequence.Open)
        self.fileOpenAction.setToolTip("Open an image.")
        self.fileOpenAction.setStatusTip("Open an image.")
        self.fileOpenAction.triggered.connect(self.fileOpen)
        self.fileMenu.addAction(self.fileOpenAction)

        self.fileSaveAction = QAction(QIcon("images/filesave.png"), "&Save Image", self)
        self.fileSaveAction.setShortcut(QKeySequence.Save)
        self.fileSaveAction.setToolTip("Save an image.")
        self.fileSaveAction.setStatusTip("Save an image.")
        self.fileSaveAction.triggered.connect(self.fileSaveAs)
        self.fileMenu.addAction(self.fileSaveAction)

        self.waySaveAction = QAction(QIcon("images/SaveWay.png"), "&Save WayPoints",self)
        self.waySaveAction.setToolTip("Save WayPoints.")
        self.waySaveAction.triggered.connect(self.WaypointsSaveAs)
        self.fileMenu.addAction(self.waySaveAction)

        # 工具栏
        fileToolbar = self.addToolBar("文件")
        fileToolbar.addAction(self.fileOpenAction)
        fileToolbar.addAction(self.fileSaveAction)
        fileToolbar.addAction(self.waySaveAction)

        editToolbar = self.addToolBar("清空")
        editToolbar.addAction(self.ClearAction)

        colorToolbar = self.addToolBar("颜色")
        colorToolbar.addAction(self.changeColor)

        widthToolbar = self.addToolBar("宽度")
        widthToolbar.addAction(self.changeWidth)

        sampleToolbar = self.addToolBar("采样间距")
        sampleToolbar.addAction(self.sampleInterval)

        # 状态栏
        self.sizeLabel = QLabel()
        self.sizeLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)


    def initData(self):
        self.size = QSize(1000, 1040)
        self.pixmap = QPixmap(self.size)

        self.dirty = False
        self.filename = None
        self.recentFiles = []

        self.sampleValue = 5
        self.pointArray = np.empty(shape=[0, 2])
        self.newArray = np.empty(shape=[0,2])

        # 新建画笔
        self.width = 5
        self.color = QColor(0, 0, 0)
        self.pen = QPen()  # 实例化画笔对象
        self.pen.setColor(self.color)  # 设置画笔颜色
        self.pen = QPen(Qt.SolidLine)  # 实例化画笔对象.参数：画笔样式
        self.pen.setWidth(self.width)  # 设置画笔粗细

        # 新建绘图工具
        self.painter = QPainter(self.pixmap)
        self.painter.setPen(self.pen)

        # 鼠标位置
        self.__lastPos = QPoint(0, 0)  # 上一次鼠标位置
        self.__currentPos = QPoint(0, 0)  # 当前的鼠标位置

        self.image = QImage()

    def initView(self):
        # 设置界面的尺寸为__size
        self.Clear()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.pixmap)
        self.setCentralWidget(self.imageLabel)

    def Clear(self):
        # 清空画板
        self.pixmap.fill(Qt.white)
        self.update()
        self.dirty = False
        self.pointArray = np.empty(shape=[0, 2])
        self.newArray = np.empty(shape=[0,2])


    def mousePressEvent(self, event):
        # 鼠标按下时，获取鼠标的当前位置保存为上一次位置

        pointX = event.globalX()
        pointY = event.globalY()

        # pointX = QCursor.pos().x()
        # pointY = QCursor.pos().Y()

        self.__currentPos = QPoint(pointX, pointY)
        print(self.__currentPos)
        self.dirty = True
        self.__currentPos = event.pos()
        self.__lastPos = self.__currentPos

    def mouseMoveEvent(self, event):

        # 鼠标移动时，更新当前位置，并在上一个位置和当前位置间画线
        self.__currentPos = event.pos()
        self.pointArray = np.append(self.pointArray, [[self.__currentPos.x(), self.__currentPos.y()]],axis=0)


        # 画线
        # 用begin和end抱起来，表示针对这个对象，就可以在pixmap有图的情况下继续画画
        self.painter.begin(self.pixmap)

        self.painter.setPen(self.pen)
        self.painter.drawLine(self.__lastPos, self.__currentPos)

        self.__lastPos = self.__currentPos
        self.painter.end()
        self.update()  # 更新显示
        self.imageLabel.setPixmap(self.pixmap)
        self.drawPixmap = self.pixmap.copy()


    # 调画笔颜色
    def showColorDialog(self):
        col = QColorDialog.getColor()
        self.pen.setColor(col)
        self.painter.setPen(self.pen)

    def updateWidth(self):
        self.pen.setWidth(self.width)
        self.painter.setPen(self.pen)


    def showWidthDialog(self):
        num, ok = QInputDialog.getInt(self, '画笔宽度设置', '画笔宽度', value=self.width, min=1, max=20)
        if ok:
            self.width = num
            self.updateWidth()

    def sampleLine(self):
        self.newArray = np.empty(shape=[0,2])

        for i in range(self.pointArray.shape[0]):
            if(i % (self.sampleValue +1) == 0):
                self.newArray = np.append(self.newArray,[self.pointArray[i]],axis=0)

        color = QColor(255,255,0)
        self.pen.setColor(color)
        self.painter.begin(self.drawPixmap)
        self.painter.setPen(self.pen)
        for pos in self.newArray:
            tempPoint = QPoint(int(pos[0]),int(pos[1]))
            self.painter.drawPoint(tempPoint)
        self.painter.end()
        self.update()  # 更新显示
        self.imageLabel.setPixmap(self.drawPixmap)
        self.pen.setColor(self.color)
        self.drawPixmap = self.pixmap.copy()


    def showSampleDialog(self):
        num, ok = QInputDialog.getInt(self, '采样间距设置', '采样间距',value=self.sampleValue,min=1,max=50)
        if ok and num:
            self.sampleValue = num
            self.sampleLine()



    ###########################################################
    def okToContinue(self):  # 警告当前图像未保存
        if self.dirty:
            reply = QMessageBox.question(self,
                                         "Image Changer - Unsaved Changes",
                                         "图片已被更改，请问要保存吗?",
                                         QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSaveAs()
        return True

    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (["*.{}".format(format.data().decode("ascii").lower())
                    for format in QImageReader.supportedImageFormats()])
        fname = QFileDialog.getOpenFileName(self,
                                            "Image Changer - Choose Image", dir,
                                            "Image files ({})".format(" ".join(formats)))
        if fname:
            print(fname[0])
            self.loadFile(fname[0])
            self.updateFileMenu()

    def loadFile(self, fname=None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = action.data()
                if not self.okToContinue():
                    return
            else:
                return
        if fname:
            self.filename = None
            image = QImage(fname)
            if image.isNull():
                message = "Failed to read {}".format(fname)
            else:
                self.addRecentFile(fname)
                self.image = QImage()
                # self.editUnMirrorAction.setChecked(True)
                self.image = image
                self.filename = fname
                self.showImage()
                self.dirty = False
                self.sizeLabel.setText("{} x {}".format(
                    image.width(), image.height()))
                message = "Loaded {}".format(os.path.basename(fname))
            self.updateStatus(message)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        # self.listWidget.addItem(message)
        if self.filename:
            self.setWindowTitle("Image Changer - {}[*]".format(
                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)

    def updateFileMenu(self):
        self.Menu.clear()
        self.Menu.addAction(self.fileOpenAction)
        self.Menu.addAction(self.fileSaveAction)
        current = self.filename
        recentFiles = []
        print(self.recentFiles)
        for fname in self.recentFiles:
            if fname != current and QFile.exists(fname):
                recentFiles.append(fname)
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                action = QAction(QIcon("images/icon.png"),
                                 "&{} {}".format(i + 1, QFileInfo(
                                     fname).fileName()), self)
                action.setData(fname)
                action.triggered.connect(lambda: self.loadFile(fname))
                self.fileMenu.addAction(action)

    def addRecentFile(self, fname):
        if fname is None:
            return
        if fname not in self.recentFiles:
            if len(self.recentFiles) < 10:
                self.recentFiles = [fname] + self.recentFiles
            else:
                self.recentFiles = [fname] + self.recentFiles[:8]
            print(len(self.recentFiles))


    def WaypointsSaveAs(self):
        savePath = QFileDialog.getSaveFileName(self,"Save wayoints",".\\","*.txt")
        if savePath[0] =="":
            return
        if self.newArray.size == 0:
            print("the waypoints array is empty")
            return
        saveArray = np.empty(shape=[0,2])
        for pos in self.newArray:
            _x = pos[0]
            _y = (1040 - pos[1])
            saveArray = np.append(saveArray,[[_x,_y]],axis=0)
        np.savetxt(savePath[0], saveArray, fmt='%0.4f')
        self.updateStatus("Saved as {}".format(savePath))


    def fileSaveAs(self):
        savePath = QFileDialog.getSaveFileName(self, 'Save Your Paint', '.\\', '*.png')
        print(savePath)
        if savePath[0] == "":
            print("Save cancel")
            return
        image = self.pixmap
        print("save...")
        image.save(savePath[0])
        self.updateStatus("Saved as {}".format(savePath))

    def showImage(self, percent=None):
        if self.image.isNull():
            return
        self.pixmap = QPixmap.fromImage(self.image)
        self.imageLabel.setPixmap(self.pixmap)


app = QApplication(sys.argv)
form = myMainWindow()
form.setMinimumSize(1000, 1000)
form.show()
app.exec_()
