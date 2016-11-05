# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parametersViewer.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Parameters_preview(QtGui.QDialog):
    def setupUi(self, Parameters_preview):
        self.form = Parameters_preview
        Parameters_preview.setObjectName(_fromUtf8("Parameters_preview"))
        Parameters_preview.resize(489, 492)
        self.current_parameter_index = None
        self.gridLayout = QtGui.QGridLayout(Parameters_preview)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Parameters_preview)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.parameters_list_tree_view = QtGui.QTreeView(Parameters_preview)
        self.parameters_list_tree_view.setAnimated(True)
        self.parameters_list_tree_view.setObjectName(_fromUtf8("parameters_list_tree_view"))
        self.parameters_list_tree_view.header().setVisible(False)
        self.verticalLayout.addWidget(self.parameters_list_tree_view)
        self.parameters_preview_btns = QtGui.QDialogButtonBox(Parameters_preview)
        self.parameters_preview_btns.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.parameters_preview_btns.setObjectName(_fromUtf8("parameters_preview_btns"))
        self.verticalLayout.addWidget(self.parameters_preview_btns)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Parameters_preview)
        QtCore.QMetaObject.connectSlotsByName(Parameters_preview)
        self.parameters_preview_btns.clicked.connect(self.close_window)

    def retranslateUi(self, Parameters_preview):
        Parameters_preview.setWindowTitle(_translate("Parameters_preview", "Parameters", None))
        self.label.setText(_translate("Parameters_preview", "Job parameters", None))

    def close_window(self):
        self.form.close()
