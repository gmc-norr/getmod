# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(364, 192)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.header_frame = QFrame(Dialog)
        self.header_frame.setObjectName(u"header_frame")
        self.horizontalLayout_2 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.button_title_icon = QPushButton(self.header_frame)
        self.button_title_icon.setObjectName(u"button_title_icon")
        self.button_title_icon.setMaximumSize(QSize(30, 16777215))
        self.button_title_icon.setFlat(True)

        self.horizontalLayout_2.addWidget(self.button_title_icon)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.label_title = QLabel(self.header_frame)
        self.label_title.setObjectName(u"label_title")

        self.horizontalLayout_2.addWidget(self.label_title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.minimize_window_button = QPushButton(self.header_frame)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        self.minimize_window_button.setMaximumSize(QSize(30, 16777215))
        self.minimize_window_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.minimize_window_button)


        self.verticalLayout_2.addWidget(self.header_frame)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(9, 9, 9, 9)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_lport = QLineEdit(Dialog)
        self.lineEdit_lport.setObjectName(u"lineEdit_lport")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_lport)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_rport = QLineEdit(Dialog)
        self.lineEdit_rport.setObjectName(u"lineEdit_rport")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_rport)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_apikey = QLineEdit(Dialog)
        self.lineEdit_apikey.setObjectName(u"lineEdit_apikey")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_apikey)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.lineEdit_iid = QLineEdit(Dialog)
        self.lineEdit_iid.setObjectName(u"lineEdit_iid")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_iid)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(9, 9, 9, 9)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_3.addWidget(self.buttonBox)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.verticalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.button_title_icon.setText("")
        self.label_title.setText(QCoreApplication.translate("Dialog", u"GetMod - get request modifier", None))
        self.minimize_window_button.setText(QCoreApplication.translate("Dialog", u"[_]", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"LISTEN PORT", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"RELAY PORT", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"APIKEY", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"INSTITUTION ID  ", None))
    # retranslateUi

