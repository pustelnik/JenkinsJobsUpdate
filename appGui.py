# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jenkins_job_editor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
import re
import localUpdateJobs
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

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


class Ui_TabWidget(object):
    def __init__(self):
        self.params = {}
        self.jobs = []
        self.mvn_params = []
        self.tempResults = {}

    def setupUi(self, TabWidget):
        TabWidget.setObjectName(_fromUtf8("TabWidget"))
        TabWidget.resize(544, 758)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TabWidget.sizePolicy().hasHeightForWidth())
        TabWidget.setSizePolicy(sizePolicy)
        self.jobs_select_tab = QtGui.QWidget()
        self.jobs_select_tab.setObjectName(_fromUtf8("jobs_select_tab"))
        self.gridLayoutWidget = QtGui.QWidget(self.jobs_select_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 531, 711))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_3.setContentsMargins(5, -1, -1, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.saveBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.gridLayout_3.addWidget(self.saveBtn, 4, 0, 1, 1)
        self.findJobsBtn = QtGui.QPushButton(self.gridLayoutWidget)
        self.findJobsBtn.setObjectName(_fromUtf8("findJobsBtn"))
        self.gridLayout_3.addWidget(self.findJobsBtn, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_3.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.jobsSearchResults = QtGui.QListView(self.gridLayoutWidget)
        self.jobsSearchResults.setObjectName(_fromUtf8("listView_2"))
        self.gridLayout_3.addWidget(self.jobsSearchResults, 3, 0, 1, 1)
        self.gridLayout_3.setRowStretch(4, 1)
        TabWidget.addTab(self.jobs_select_tab, _fromUtf8(""))
        self.parameters_tab = QtGui.QWidget()
        self.parameters_tab.setObjectName(_fromUtf8("parameters_tab"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.parameters_tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 531, 851))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.stringRadioBtn = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.stringRadioBtn.setObjectName(_fromUtf8("stringRadioBtn"))
        self.verticalLayout.addWidget(self.stringRadioBtn)
        self.booleanRadioBtn = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.booleanRadioBtn.setObjectName(_fromUtf8("booleanRadioBtn"))
        self.verticalLayout.addWidget(self.booleanRadioBtn)
        self.choiceRadioBtn = QtGui.QRadioButton(self.verticalLayoutWidget_2)
        self.choiceRadioBtn.setObjectName(_fromUtf8("choiceRadioBtn"))
        self.verticalLayout.addWidget(self.choiceRadioBtn)
        self.line = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 150)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.paramNameText = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.paramNameText.setObjectName(_fromUtf8("paramNameText"))
        self.verticalLayout_3.addWidget(self.paramNameText)
        self.label_8 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.mvnParamEdit = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.mvnParamEdit.setObjectName(_fromUtf8("mvnParamEdit"))
        self.verticalLayout_3.addWidget(self.mvnParamEdit)
        self.defValLabel = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.defValLabel.setObjectName(_fromUtf8("defValLabel"))
        self.verticalLayout_3.addWidget(self.defValLabel)
        self.defValEdit = QtGui.QTextEdit(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defValEdit.sizePolicy().hasHeightForWidth())
        self.defValEdit.setSizePolicy(sizePolicy)
        self.defValEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.defValEdit.setObjectName(_fromUtf8("defValEdit"))
        self.verticalLayout_3.addWidget(self.defValEdit)
        self.addParamBtn = QtGui.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addParamBtn.sizePolicy().hasHeightForWidth())
        self.addParamBtn.setSizePolicy(sizePolicy)
        self.addParamBtn.setObjectName(_fromUtf8("addParamBtn"))
        self.verticalLayout_3.addWidget(self.addParamBtn)
        self.label_9 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_3.addWidget(self.label_9)
        self.notSavedParamList = QtGui.QListView(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notSavedParamList.sizePolicy().hasHeightForWidth())
        self.notSavedParamList.setSizePolicy(sizePolicy)
        self.notSavedParamList.setMaximumSize(QtCore.QSize(16777215, 600))
        self.notSavedParamList.setObjectName(_fromUtf8("notSavedParamList"))
        self.verticalLayout_3.addWidget(self.notSavedParamList)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget_2)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.choiceRadioBtn.raise_()
        self.verticalLayoutWidget_2.raise_()
        TabWidget.addTab(self.parameters_tab, _fromUtf8(""))

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)
        self.notSavedParamList.setModel(QStandardItemModel(self.notSavedParamList))

        self.lineEdit_2.setText('/home/jakubp/.jenkins/jobs')
        #  Search results button clicked
        self.findJobsBtn.clicked.connect(self.fill_search_result)
        #  Save selection button clicked
        self.saveBtn.clicked.connect(self.add_jobs_to_list)
        #  Add parameter to list
        self.addParamBtn.clicked.connect(self.add_parameter_to_list)

        self.buttonBox.rejected.connect(self.remove_parameters)
        self.buttonBox.accepted.connect(self.save_parameters)

    def retranslateUi(self, TabWidget):
        TabWidget.setWindowTitle(_translate("TabWidget", "Jenkins jobs editor", None))
        self.saveBtn.setText(_translate("TabWidget", "Save selection", None))
        self.findJobsBtn.setText(_translate("TabWidget", "Find jobs", None))
        self.label_3.setText(_translate("TabWidget", "Jenkins jobs root", None))
        self.label_4.setText(_translate("TabWidget", "Search results", None))
        TabWidget.setTabText(TabWidget.indexOf(self.jobs_select_tab), _translate("TabWidget", "Jobs selection", None))
        self.label_5.setText(_translate("TabWidget", "Parameter type", None))
        self.stringRadioBtn.setText(_translate("TabWidget", "String", None))
        self.booleanRadioBtn.setText(_translate("TabWidget", "Boolean", None))
        self.choiceRadioBtn.setText(_translate("TabWidget", "Choice", None))
        self.label_10.setText(_translate("TabWidget", "Parameter name", None))
        self.label_8.setText(_translate("TabWidget", "Maven parameter (key=value)", None))
        self.defValLabel.setText(_translate("TabWidget", "Default value", None))
        self.addParamBtn.setText(_translate("TabWidget", "Add parameter", None))
        self.label_9.setText(_translate("TabWidget", "Not saved parameters", None))
        TabWidget.setTabText(TabWidget.indexOf(self.parameters_tab), _translate("TabWidget", "Parameters", None))
        TabWidget.setCurrentIndex(0)

    def fill_search_result(self):
        search_path = self.lineEdit_2.text()
        model = QStandardItemModel(self.jobsSearchResults)
        jobs_list = localUpdateJobs.jobs_list(search_path)
        self.tempResults = jobs_list
        print(jobs_list.__len__())
        for job in jobs_list:
            print(job)
            item = QStandardItem(job)
            item.setCheckable(True)
            model.appendRow(item)
        self.jobsSearchResults.setModel(model)

    def add_jobs_to_list(self):
        """Adds selected jobs to list"""
        model = self.jobsSearchResults.model()
        if model is None or model.rowCount() == 0:
            self.display_warn_message("Select something before saving")
        else:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == QtCore.Qt.Checked:
                    self.jobs.append(item.text())

    def add_parameter_to_list(self):
        name = self.paramNameText.text()
        description = ''  # TODO add this to UI
        default_val = self.defValEdit.toPlainText()
        mvn_param = self.mvnParamEdit.text()
        param_type = ''

        def is_blank(arg):
            return arg.__len__() == 0

        def is_param_on_list(par):
            for key in self.params.keys():
                if key == par:
                    return True
            return False

        if is_blank(name) or is_blank(default_val):
            self.display_warn_message("Name and default value cannot be empty!")
            return
        if is_param_on_list(name):
            self.display_warn_message("Param with name " + name + " is already on the list!")
            return
        if not is_blank(mvn_param) and not re.match('^\s=\s$', mvn_param):
            self.display_warn_message('Maven param must be in format key=value!')
            return

        #  param type selection
        if self.stringRadioBtn.isChecked():
            param_type = 'String'
        elif self.booleanRadioBtn.isChecked():
            param_type = 'Boolean'
        elif self.choiceRadioBtn.isChecked():
            param_type = 'Choice'

        param = localUpdateJobs.JenkinsParameters.create_parameter(param_type, name, description, default_val)
        self.params[name] = param
        if not is_blank(mvn_param):
            split = mvn_param.split('=')
            self.mvn_params.append((split[0], split[1]))
        model = self.notSavedParamList.model()
        item = QStandardItem(name)
        item.setCheckable(True)
        model.appendRow(item)

    def save_parameters(self):
        paths = []
        for job in self.jobs:
            paths.append(self.tempResults[job])
        print(paths)
        localUpdateJobs.modify_params(paths, self.params, self.mvn_params)

    def remove_parameters(self):
        model = self.notSavedParamList.model()

        if model is None or model.rowCount() == 0:
            self.display_warn_message("Nothing to remove")
        else:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == QtCore.Qt.Checked:
                    self.params.pop(item.text())
                    model.removeRow(row)

    def display_warn_message(self, text):
        message = QMessageBox()
        message.setIcon(QMessageBox.Warning)
        message.setText(text)
        message.setWindowTitle("warning")
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()


if __name__ == '__main__':
    app = QApplication([])
    foo = Ui_TabWidget()
    window = QTabWidget()
    foo.setupUi(window)
    window.show()
    sys.exit(app.exec_())
