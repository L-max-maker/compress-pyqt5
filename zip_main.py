#!/usr/bin/env python3
# coding:utf-8
# Author: wangping@www.yuanrenxue.com



from PyQt5.QtCore import QThread, QSize
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon

import zip_console

import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class LogHandler(QtCore.QObject):
    # sig = QtCore.pyqtSignal(str)
    show = QtCore.pyqtSignal(str)


class ZipTask(QThread):
    done = QtCore.pyqtSignal(str)

    def set_attr(self, fn, flg):
        self.fn = fn
        self._flg = flg

    def run(self):
        # 1 表示压缩 2 表示解压
        if 1 == self._flg:
            to_save,before_size,after_size = zip_console.yzx_zip(self.fn)
            print(before_size,after_size)
            msg = '压缩成功，保存为：<b>{}</b>'.format(to_save)
            self.done.emit(msg)
            msg = '压缩前文件大小为：<b>{}</b>'.format(before_size)
            self.done.emit(msg)
            msg = '压缩后文件大小为：<b>{}</b>'.format(after_size)
            self.done.emit(msg)
        elif 2 == self._flg:
            to_save = zip_console.yzx_unzip(self.fn)
            msg = '解压成功，解压到：<b>{}</b>'.format(to_save)
            self.done.emit(msg)
        else:
            msg = '程序出错，请关闭程序程序打开'
            self.done.emit(msg)


class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.tree = self.findChild(QtWidgets.QTreeView)

        self._selFile = ''

    def accept(self):
        inds = self.tree.selectionModel().selectedIndexes()
        self._selFile = os.path.join(str(self.directory().absolutePath()),str(inds[0].data()))
        print('_selfile:',self._selFile)
        self.hide()

    def selectedFiles(self):
        return self._selFile


class Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.langlist = ['压缩','解压']

        self.browseButton = self.createButton("&选择...", self.browse)
        self.transButton = self.createButton("&开始", self.translate)

        self.lang_srcComboBox = self.createComboBox()
        srcIndex = self.langlist.index('压缩')
        self.lang_srcComboBox.setCurrentIndex(srcIndex)
        self.fileComboBox = self.createComboBox('file')

        srcLabel = QtWidgets.QLabel("压缩or解压:")
        #dstLabel = QtWidgets.QLabel("目标语言:")
        docLabel = QtWidgets.QLabel("选择文档:")
        self.filesFoundLabel = QtWidgets.QLabel()

        self.logPlainText = QtWidgets.QPlainTextEdit()
        self.logPlainText.setReadOnly(True)


        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.transButton)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.addWidget(srcLabel, 0, 0)
        mainLayout.addWidget(self.lang_srcComboBox, 0, 1, 1, 2)
        #mainLayout.addWidget(dstLabel, 1, 0)
        #mainLayout.addWidget(self.lang_dstComboBox, 1, 1, 1, 2)
        #mainLayout.addWidget(docLabel, 2, 0)
        mainLayout.addWidget(self.fileComboBox, 2, 1)
        mainLayout.addWidget(self.browseButton, 2, 2)
        # mainLayout.addWidget(self.filesTable, 3, 0, 1, 3)
        mainLayout.addWidget(self.logPlainText, 3, 0, 1, 3)
        mainLayout.addWidget(self.filesFoundLabel, 4, 0)
        mainLayout.addLayout(buttonsLayout, 5, 0, 1, 3)
        self.setLayout(mainLayout)

        app_icon = QIcon()#icon = https://imgur.com/NV7Ugfd
        icon_path = resource_path('icon.png')
        app_icon.addFile(icon_path, QSize(16, 16))
        app_icon.addFile(icon_path, QSize(24, 24))
        app_icon.addFile(icon_path, QSize(32, 32))
        app_icon.addFile(icon_path, QSize(48, 48))
        app_icon.addFile(icon_path, QSize(256, 256))
        self.setWindowIcon(app_icon)

        self.setWindowTitle("Python压缩-猿人学公众号测试用")
        self.resize(600, 400)

        # translate
        self.logger = LogHandler()
        self.logger.show.connect(self.onLog)
        zip_console.g_log = self.logger
        self.task = ZipTask()
        self.task.done.connect(self.onLog)


    def compress_procedure(self):
        dialog = FileDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            pass
        sfile = dialog.selectedFiles()
        print('select compress file:',sfile)

        if sfile:
            self.logPlainText.clear()
            msg = '选择了要压缩的文件: <b>{}</b>'.format(sfile)
            self.logger.show.emit(msg)
            if self.fileComboBox.findText(sfile) == -1:
                self.fileComboBox.addItem(sfile)

            self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(sfile))
    
    def uncompress_procedure(self):
        sfile, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择文件",
            QtCore.QDir.currentPath(),
            "(*.zip *.rar)",
        )
        print(sfile)
        if sfile:
            self.logPlainText.clear()
            msg = '选择了要解压的文件: <b>{}</b>'.format(sfile)
            self.logger.show.emit(msg)
            if self.fileComboBox.findText(sfile) == -1:
                self.fileComboBox.addItem(sfile)

            self.fileComboBox.setCurrentIndex(self.fileComboBox.findText(sfile))

    def browse(self):
        lang_src_select = self.lang_srcComboBox.currentText()
        print('lang_src_select:', lang_src_select)
        if '压缩' == lang_src_select:
            self.compress_procedure()
            self._flg = 1
        else:
            self.uncompress_procedure()
            self._flg = 2

    def onLog(self, msg):
        self.logPlainText.appendHtml(msg)

    def translate(self):
        fileName = self.fileComboBox.currentText()
        if not fileName:
            self.logger.show.emit('请先选择要压缩或解压的文件')
            return
        print(fileName)
        self.logger.show.emit('开始执行：{}'.format(fileName))
        self.task.set_attr(fileName,self._flg)
        self.task.start()

    def createButton(self, text, member):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, btype=''):
        comboBox = QtWidgets.QComboBox(self)
        if btype != 'file':
            comboBox.setEditable(True)
            comboBox.addItems(self.langlist)
        comboBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Preferred)
        return comboBox


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
