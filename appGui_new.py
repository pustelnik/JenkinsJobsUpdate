# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jenkins_job_editor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import re
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import configView
import localUpdateJobs
import remoteUpdateJobs
import logging
import paramiko

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
    def setupUi(self, TabWidget):
        TabWidget.setObjectName(_fromUtf8("TabWidget"))
        TabWidget.resize(552, 792)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TabWidget.sizePolicy().hasHeightForWidth())
        TabWidget.setSizePolicy(sizePolicy)
        self.jobs_select_tab = QtGui.QWidget()
        self.jobs_select_tab.setObjectName(_fromUtf8("jobs_select_tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.jobs_select_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 541, 751))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_16 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_4.addWidget(self.label_16)
        self.line_3 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_4.addWidget(self.line_3)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        self.formLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_15 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_15)
        self.remoteConfigCheckBox_2 = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.remoteConfigCheckBox_2.setChecked(True)
        self.remoteConfigCheckBox_2.setObjectName(_fromUtf8("remoteConfigCheckBox_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.remoteConfigCheckBox_2)
        self.label_12 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_5 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_13 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_13)
        self.lineEdit_6 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_14 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_14)
        self.lineEdit_7 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_7)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.line_4 = QtGui.QFrame(self.verticalLayoutWidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout_4.addWidget(self.line_4)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_3.setContentsMargins(5, -1, -1, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 3, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.saveBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout_7.addWidget(self.saveBtn)
        self.pushButton_3 = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_7.addWidget(self.pushButton_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 7, 0, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout_3.addWidget(self.lineEdit_2, 2, 0, 1, 1)
        self.findJobsBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.findJobsBtn.setObjectName(_fromUtf8("findJobsBtn"))
        self.gridLayout_3.addWidget(self.findJobsBtn, 2, 1, 1, 1)
        self.jobsSearchResults = QtGui.QListView(self.verticalLayoutWidget)
        self.jobsSearchResults.setObjectName(_fromUtf8("listView_2"))
        self.gridLayout_3.addWidget(self.jobsSearchResults, 4, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 2, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout_4.setStretch(4, 50)
        self.jobsSearchResults.raise_()
        self.verticalLayoutWidget.raise_()
        TabWidget.addTab(self.jobs_select_tab, _fromUtf8(""))
        self.parameters_tab = QtGui.QWidget()
        self.parameters_tab.setObjectName(_fromUtf8("parameters_tab"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.parameters_tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 10, 531, 741))
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
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.paramNameText = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.paramNameText.setObjectName(_fromUtf8("paramNameText"))
        self.verticalLayout_3.addWidget(self.paramNameText)
        self.label = QtGui.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.descriptionText = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.descriptionText.setObjectName(_fromUtf8("descriptionText"))
        self.verticalLayout_3.addWidget(self.descriptionText)
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
        self.notSavedParamList.setMaximumSize(QtCore.QSize(16777215, 600))
        self.notSavedParamList.setObjectName(_fromUtf8("notSavedParamList"))
        self.verticalLayout_3.addWidget(self.notSavedParamList)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget_2)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Discard | QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        TabWidget.addTab(self.parameters_tab, _fromUtf8(""))

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        TabWidget.setWindowTitle(_translate("TabWidget", "Jenkins jobs editor", None))
        self.label_16.setText(_translate("TabWidget", "Configuration", None))
        self.label_15.setText(_translate("TabWidget", "Remote jenkins", None))
        self.remoteConfigCheckBox_2.setText(_translate("TabWidget", "enabled", None))
        self.label_12.setText(_translate("TabWidget", "host", None))
        self.label_13.setText(_translate("TabWidget", "username", None))
        self.label_14.setText(_translate("TabWidget", "password", None))
        self.label_4.setText(_translate("TabWidget", "Search results", None))
        self.saveBtn.setText(_translate("TabWidget", "Save selection", None))
        self.pushButton_3.setText(_translate("TabWidget", "Preview config", None))
        self.findJobsBtn.setText(_translate("TabWidget", "Find jobs", None))
        self.label_3.setText(_translate("TabWidget", "Jenkins jobs root", None))
        TabWidget.setTabText(TabWidget.indexOf(self.jobs_select_tab), _translate("TabWidget", "Jobs selection", None))
        self.label_5.setText(_translate("TabWidget", "Parameter type", None))
        self.stringRadioBtn.setText(_translate("TabWidget", "String", None))
        self.booleanRadioBtn.setText(_translate("TabWidget", "Boolean", None))
        self.choiceRadioBtn.setText(_translate("TabWidget", "Choice", None))
        self.label_10.setText(_translate("TabWidget", "Parameter name", None))
        self.label.setText(_translate("TabWidget", "Description", None))
        self.label_8.setText(_translate("TabWidget", "Maven parameter (key=value)", None))
        self.defValLabel.setText(_translate("TabWidget", "Default value", None))
        self.addParamBtn.setText(_translate("TabWidget", "Add parameter", None))
        self.label_9.setText(_translate("TabWidget", "Not saved parameters", None))
        TabWidget.setTabText(TabWidget.indexOf(self.parameters_tab), _translate("TabWidget", "Parameters", None))


class JenkinsUpdateJobsGui(QTabWidget, Ui_TabWidget):
    def __init__(self, tab_widget):
        super().__init__()
        super().setupUi(tab_widget)
        logging.basicConfig(level=logging.INFO)
        self.params = {}
        self.jobs = []
        self.mvn_params = []
        self.tempResults = {}
        self.remote = True
        self.remote_instance_created = False
        self.jenkins_params = None
        self.notSavedParamList.setModel(QStandardItemModel(self.notSavedParamList))
        self.config = self._read_config_from_file()

        def set_config(config_name, line_edit):
            if self.config.__contains__(config_name) and not is_blank(self.config[config_name]):
                line_edit.setText(self.config[config_name])

        set_config('search_path', self.lineEdit_2)
        set_config('remote_host', self.lineEdit_5)
        set_config('remote_usr', self.lineEdit_6)

        #  Search results button clicked
        self.findJobsBtn.clicked.connect(self.start_searching_jobs_list)
        #  Save selection button clicked
        self.saveBtn.clicked.connect(self.add_jobs_to_list)
        #  Preview config
        self.pushButton_3.clicked.connect(self.preview_config)
        #  Add parameter to list
        self.addParamBtn.clicked.connect(self.add_parameter_to_list)
        self.buttonBox.rejected.connect(self.remove_parameters)
        self.buttonBox.accepted.connect(self.save_parameters)
        #  Sets remote configuration flag
        self.lineEdit_7.setEchoMode(QLineEdit.Password)
        self.remoteConfigCheckBox_2.clicked.connect(self.is_remote)

    def start_searching_jobs_list(self):
        host = self.lineEdit_5.text()
        usr = self.lineEdit_6.text()
        pwd = self.lineEdit_7.text()
        self.search_path = self.lineEdit_2.text()
        self.search_thread = JobSearchThread(self.search_path, self.remote, self.jenkins_params, host, usr, pwd)
        self.connect(self.search_thread, SIGNAL('create_jenkins_params_instance(PyQt_PyObject)'),
                     self.create_jenkins_params_instance)
        self.connect(self.search_thread, SIGNAL('add_jobs_temp_search_results(PyQt_PyObject)'),
                     self.add_jobs_temp_search_results)
        self.connect(self.search_thread, SIGNAL('show_error_message(PyQt_PyObject)'), self.show_error_message)
        self.connect(self.search_thread, SIGNAL('finished()'), self.job_search_finished)
        self.search_thread.start()
        self.findJobsBtn.setEnabled(False)

    def is_remote(self):
        if self.remoteConfigCheckBox_2.isChecked():
            self.remote = True
        else:
            self.remote = False

    def job_search_finished(self):
        self.findJobsBtn.setEnabled(True)

    def create_jenkins_params_instance(self, jenkins_params):
        self.jenkins_params = jenkins_params

    def add_jobs_temp_search_results(self, temp_results):
        model = QStandardItemModel(self.jobsSearchResults)
        self.tempResults = temp_results
        for job in temp_results.keys():
            item = QStandardItem(job)
            item.setCheckable(True)
            model.appendRow(item)
        self.jobsSearchResults.setModel(model)

    def show_error_message(self, message):
        QtGui.QMessageBox.critical(self, "Warning!", message, QtGui.QMessageBox.Ok)

    def show_info_message(self, message):
        QtGui.QMessageBox.information(self, "Info!", message, QtGui.QMessageBox.Ok)

    def add_jobs_to_list(self):
        """Adds selected jobs to list"""
        model = self.jobsSearchResults.model()
        if model is None or model.rowCount() == 0:
            self.show_error_message("Select something before saving")
        else:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == QtCore.Qt.Checked:
                    self.jobs.append(item.text())

    def preview_config(self):
        model = self.jobsSearchResults.model()
        if model is None or model.rowCount() == 0:
            self.show_error_message("Select something before viewing")
        # elif model.rowCount() >= 2:
        #     #  TODO change Checked to Selected
        #     self.display_warn_message("Only one config at a time can be viewed")
        else:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == QtCore.Qt.Checked:
                    reader = configView.Ui_Form()
                    popup_window = QDialog()
                    reader.setupUi(popup_window)
                    reader.viewTextBrowser.setText(
                        self.jenkins_params.read_config_file(self.tempResults[item.text()]))
                    popup_window.setWindowModality(Qt.ApplicationModal)
                    popup_window.exec_()

    def add_parameter_to_list(self):
        name = self.paramNameText.text()
        description = self.descriptionText.text()
        default_val = self.defValEdit.toPlainText()
        mvn_param = self.mvnParamEdit.text()
        param_type = ''

        def is_param_on_list(par):
            for key in self.params.keys():
                if key == par:
                    return True
            return False

        if is_blank(name) or is_blank(default_val):
            self.show_error_message("Name and default value cannot be empty!")
            return
        if is_param_on_list(name):
            self.show_error_message("Param with name " + name + " is already on the list!")
            return
        if not is_blank(mvn_param) and not re.match('^\s=\s$', mvn_param):
            self.show_error_message('Maven param must be in format key=value!')
            return

        # param type selection
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
        paths = {}
        for job in self.jobs:
            paths[job] = self.tempResults[job]
        self.jenkins_params.modify_params(paths, self.params, self.mvn_params)
        self.show_info_message("Successfully added all parameters to selected jobs")

    def remove_parameters(self):
        model = self.notSavedParamList.model()

        if model is None or model.rowCount() == 0:
            self.show_error_message("Nothing to remove")
        else:
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.checkState() == QtCore.Qt.Checked:
                    self.params.pop(item.text())
                    model.removeRow(row)

    @staticmethod
    def _read_config_from_file():
        config_file = open('default.cfg')
        configs = {}
        for line in config_file:
            key, value = line.split('=')
            configs[key] = value.strip()
        return configs


class InvalidRemoteCredentialsException(Exception):
    def __init__(self, message):
        self.message = message


class JobSearchThread(QThread):
    def __init__(self, search_path, remote, jenkins_params, host, usr, pwd):
        super().__init__()
        self.jenkins_params = None
        self.remote = remote
        self.jenkins_params = jenkins_params
        self.host = host
        self.usr = usr
        self.pwd = pwd
        self.search_path = search_path
        self.remote_instance_created = False

    def create_remote_params_instance(self, host, usr, pwd):
        if self.remote_instance_created:
            return
        if is_blank(host) or is_blank(usr) or is_blank(pwd):
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), "Hostname, username or password cannot be empty!")
            raise InvalidRemoteCredentialsException('Hostname, username or password is empty')
        else:
            return remoteUpdateJobs.RemoteJenkinsParameters(host, usr, pwd, self.search_path)

    def fill_search_result(self):
        search_path = self.search_path
        try:
            if self.remote:
                self.jenkins_params = self.create_remote_params_instance(self.host, self.usr, self.pwd)
            else:
                self.jenkins_params = localUpdateJobs.JenkinsParameters(search_path)
                self.remote_instance_created = True
            # emits jenkins_params instance to main thread
            self.emit(SIGNAL('create_jenkins_params_instance(PyQt_PyObject)'), self.jenkins_params)

            jobs_list = self.jenkins_params.read_all_configs(search_path)
            # emits complete job search dictionary to main thread
            self.emit(SIGNAL('add_jobs_temp_search_results(PyQt_PyObject)'), jobs_list)
        except InvalidRemoteCredentialsException as credErr:
            logging.debug(credErr)
        except FileNotFoundError as err:
            logging.debug(err)
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), "File not found at " + search_path)
        except TimeoutError as err:
            logging.debug(err)
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), err.strerror)
        except paramiko.ssh_exception.NoValidConnectionsError as err:
            logging.debug(err)
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), err.strerror)

    def run(self):
        self.fill_search_result()


def is_blank(arg):
    return arg.__len__() == 0


if __name__ == '__main__':
    app = QApplication([])
    window = QTabWidget()
    foo = JenkinsUpdateJobsGui(window)
    window.show()
    sys.exit(app.exec_())
