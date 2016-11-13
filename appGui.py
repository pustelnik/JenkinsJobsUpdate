# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jenkins_job_editor.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import re
import sys
import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import configView
import parametersView
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


class FilterLineEdit(QtGui.QLineEdit):
    """Class used for filtering jobs list view model on
    copy parameters tab."""
    def __init__(self, parent, is_src_filter, *__args):
        super().__init__(*__args)
        self.parent = parent
        self.is_src_filter = is_src_filter
        self.src_jobs_copy = []
        self.target_jobs_copy = []

    def mousePressEvent(self, QMouseEvent):
        super().mousePressEvent(QMouseEvent)
        self.clear_text()

    def keyReleaseEvent(self, QKeyEvent):
        super().keyReleaseEvent(QKeyEvent)
        if self.is_src_filter:
            self.filter_src_jobs()
        else:
            self.filter_target_jobs()

    def clear_text(self):
        if self.is_src_filter and self.parent.src_job_filter.text().startswith('source filter'):
            self.parent.src_job_filter.setText('')
        elif self.parent.target_job_filter.text().startswith('target filter'):
            self.parent.target_job_filter.setText('')

    def filter_src_jobs(self):
        self._filter_model(self.parent.src_job_list_view.model(), self.parent.src_job_filter.text())

    def filter_target_jobs(self):
        self._filter_model(self.parent.target_jobs_list_view.model(), self.parent.target_job_filter.text())

    def _filter_model(self, model: QStandardItemModel, regex):
        self._restore_copy(model, self.get_model_copy(model))
        for row in range(model.rowCount(), -1, -1):
            item = model.item(row)
            if item is not None and not re.match(regex.startswith('^') if '' else '.*' + regex.lower() + '.*',
                                                 item.text().lower()):
                model.removeRow(row)

    def get_model_copy(self, model):
        if self.is_src_filter and self.src_jobs_copy.__len__() == 0:
            self.src_jobs_copy = self._copy_model_items(model)
        elif self.target_jobs_copy.__len__() == 0:
            self.target_jobs_copy = self._copy_model_items(model)
        if self.is_src_filter:
            return self.src_jobs_copy
        else:
            return self.target_jobs_copy

    @staticmethod
    def _copy_model_items(model):
        temp = []
        for row in range(model.rowCount()):
            item = model.item(row)
            temp.append(item.text())
        return temp

    @staticmethod
    def _restore_copy(model: QStandardItemModel, copy):
        for row in range(model.rowCount(), -1, -1):
            model.removeRow(row)
        for job_name in copy:
            item = QStandardItem()
            item.setCheckable(False)
            item.setText(job_name)
            model.appendRow(item)


class Ui_TabWidget(object):
    def setupUi(self, Ui_TabWidget):
        Ui_TabWidget.setObjectName(_fromUtf8("Ui_TabWidget"))
        Ui_TabWidget.setEnabled(True)
        Ui_TabWidget.resize(511, 742)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Ui_TabWidget.sizePolicy().hasHeightForWidth())
        Ui_TabWidget.setSizePolicy(sizePolicy)
        Ui_TabWidget.setMinimumSize(QtCore.QSize(400, 700))
        Ui_TabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.jobs_select_tab = QtGui.QWidget()
        self.jobs_select_tab.setObjectName(_fromUtf8("jobs_select_tab"))
        self.gridLayout = QtGui.QGridLayout(self.jobs_select_tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_16 = QtGui.QLabel(self.jobs_select_tab)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_4.addWidget(self.label_16)
        self.line_3 = QtGui.QFrame(self.jobs_select_tab)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.verticalLayout_4.addWidget(self.line_3)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        self.formLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_15 = QtGui.QLabel(self.jobs_select_tab)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_15)
        self.remoteConfigCheckBox_2 = QtGui.QCheckBox(self.jobs_select_tab)
        self.remoteConfigCheckBox_2.setChecked(True)
        self.remoteConfigCheckBox_2.setObjectName(_fromUtf8("remoteConfigCheckBox_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.remoteConfigCheckBox_2)
        self.label_12 = QtGui.QLabel(self.jobs_select_tab)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_12)
        self.lineEdit_5 = QtGui.QLineEdit(self.jobs_select_tab)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_13 = QtGui.QLabel(self.jobs_select_tab)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_13)
        self.lineEdit_6 = QtGui.QLineEdit(self.jobs_select_tab)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_14 = QtGui.QLabel(self.jobs_select_tab)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_14)
        self.lineEdit_7 = QtGui.QLineEdit(self.jobs_select_tab)
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_7)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.line_4 = QtGui.QFrame(self.jobs_select_tab)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.verticalLayout_4.addWidget(self.line_4)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.gridLayout_3.setContentsMargins(5, -1, -1, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_4 = QtGui.QLabel(self.jobs_select_tab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 4, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.saveBtn = QtGui.QPushButton(self.jobs_select_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(126)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveBtn.sizePolicy().hasHeightForWidth())
        self.saveBtn.setSizePolicy(sizePolicy)
        self.saveBtn.setMaximumSize(QtCore.QSize(126, 38))
        self.saveBtn.setToolTip(_fromUtf8(""))
        self.saveBtn.setAutoDefault(False)
        self.saveBtn.setDefault(False)
        self.saveBtn.setFlat(False)
        self.saveBtn.setObjectName(_fromUtf8("saveBtn"))
        self.horizontalLayout_7.addWidget(self.saveBtn)
        self.pushButton_3 = QtGui.QPushButton(self.jobs_select_tab)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_7.addWidget(self.pushButton_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 8, 0, 1, 1)
        self.jobsSearchResults = QtGui.QListView(self.jobs_select_tab)
        self.jobsSearchResults.setObjectName(_fromUtf8("jobsSearchResults"))
        self.gridLayout_3.addWidget(self.jobsSearchResults, 5, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.jobs_select_tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 2, 1)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.lineEdit_2 = QtGui.QLineEdit(self.jobs_select_tab)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.verticalLayout_8.addWidget(self.lineEdit_2)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.findJobsBtn = QtGui.QPushButton(self.jobs_select_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(126)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findJobsBtn.sizePolicy().hasHeightForWidth())
        self.findJobsBtn.setSizePolicy(sizePolicy)
        self.findJobsBtn.setMaximumSize(QtCore.QSize(126, 38))
        self.findJobsBtn.setBaseSize(QtCore.QSize(126, 38))
        self.findJobsBtn.setObjectName(_fromUtf8("findJobsBtn"))
        self.horizontalLayout_9.addWidget(self.findJobsBtn)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.gridLayout_3.addLayout(self.verticalLayout_8, 2, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout_4.setStretch(4, 50)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        Ui_TabWidget.addTab(self.jobs_select_tab, _fromUtf8(""))
        self.parameters_tab = QtGui.QWidget()
        self.parameters_tab.setObjectName(_fromUtf8("parameters_tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.parameters_tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_5 = QtGui.QLabel(self.parameters_tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.stringRadioBtn = QtGui.QRadioButton(self.parameters_tab)
        self.stringRadioBtn.setObjectName(_fromUtf8("stringRadioBtn"))
        self.verticalLayout.addWidget(self.stringRadioBtn)
        self.booleanRadioBtn = QtGui.QRadioButton(self.parameters_tab)
        self.booleanRadioBtn.setObjectName(_fromUtf8("booleanRadioBtn"))
        self.verticalLayout.addWidget(self.booleanRadioBtn)
        self.choiceRadioBtn = QtGui.QRadioButton(self.parameters_tab)
        self.choiceRadioBtn.setObjectName(_fromUtf8("choiceRadioBtn"))
        self.verticalLayout.addWidget(self.choiceRadioBtn)
        self.line = QtGui.QFrame(self.parameters_tab)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_10 = QtGui.QLabel(self.parameters_tab)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_3.addWidget(self.label_10)
        self.paramNameText = QtGui.QLineEdit(self.parameters_tab)
        self.paramNameText.setObjectName(_fromUtf8("paramNameText"))
        self.verticalLayout_3.addWidget(self.paramNameText)
        self.label = QtGui.QLabel(self.parameters_tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.descriptionText = QtGui.QLineEdit(self.parameters_tab)
        self.descriptionText.setObjectName(_fromUtf8("descriptionText"))
        self.verticalLayout_3.addWidget(self.descriptionText)
        self.label_8 = QtGui.QLabel(self.parameters_tab)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.mvnParamEdit = QtGui.QLineEdit(self.parameters_tab)
        self.mvnParamEdit.setObjectName(_fromUtf8("mvnParamEdit"))
        self.verticalLayout_3.addWidget(self.mvnParamEdit)
        self.defValLabel = QtGui.QLabel(self.parameters_tab)
        self.defValLabel.setObjectName(_fromUtf8("defValLabel"))
        self.verticalLayout_3.addWidget(self.defValLabel)
        self.defValEdit = QtGui.QTextEdit(self.parameters_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.defValEdit.sizePolicy().hasHeightForWidth())
        self.defValEdit.setSizePolicy(sizePolicy)
        self.defValEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.defValEdit.setObjectName(_fromUtf8("defValEdit"))
        self.verticalLayout_3.addWidget(self.defValEdit)
        self.addParamBtn = QtGui.QPushButton(self.parameters_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addParamBtn.sizePolicy().hasHeightForWidth())
        self.addParamBtn.setSizePolicy(sizePolicy)
        self.addParamBtn.setObjectName(_fromUtf8("addParamBtn"))
        self.verticalLayout_3.addWidget(self.addParamBtn)
        self.label_9 = QtGui.QLabel(self.parameters_tab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_3.addWidget(self.label_9)
        self.notSavedParamList = QtGui.QListView(self.parameters_tab)
        self.notSavedParamList.setMaximumSize(QtCore.QSize(16777215, 600))
        self.notSavedParamList.setObjectName(_fromUtf8("notSavedParamList"))
        self.verticalLayout_3.addWidget(self.notSavedParamList)
        self.buttonBox = QtGui.QDialogButtonBox(self.parameters_tab)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Discard | QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.line_2 = QtGui.QFrame(self.parameters_tab)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        Ui_TabWidget.addTab(self.parameters_tab, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tab)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_6.addWidget(self.label_2)
        self.src_job_list_view = QtGui.QListView(self.tab)
        self.src_job_list_view.setObjectName(_fromUtf8("src_job_list_view"))
        self.verticalLayout_6.addWidget(self.src_job_list_view)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.src_job_filter = FilterLineEdit(self, True, self.tab)
        self.src_job_filter.setObjectName(_fromUtf8("src_job_filter"))
        self.horizontalLayout_6.addWidget(self.src_job_filter)
        self.find_parameters_btn = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.find_parameters_btn.sizePolicy().hasHeightForWidth())
        self.find_parameters_btn.setSizePolicy(sizePolicy)
        self.find_parameters_btn.setObjectName(_fromUtf8("find_parameters_btn"))
        self.horizontalLayout_6.addWidget(self.find_parameters_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_6.addWidget(self.label_6)
        self.target_jobs_list_view = QtGui.QListView(self.tab)
        self.target_jobs_list_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.target_jobs_list_view.setObjectName(_fromUtf8("target_jobs_list_view"))
        self.verticalLayout_6.addWidget(self.target_jobs_list_view)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.target_job_filter = FilterLineEdit(self, False, self.tab)
        self.target_job_filter.setObjectName(_fromUtf8("target_job_filter"))
        self.horizontalLayout_5.addWidget(self.target_job_filter)
        spacerItem2 = QtGui.QSpacerItem(140, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_6.addWidget(self.label_7)
        self.listView = QtGui.QListView(self.tab)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.verticalLayout_6.addWidget(self.listView)
        self.copy_mvn_parameter_check_box = QtGui.QCheckBox(self.tab)
        self.copy_mvn_parameter_check_box.setObjectName(_fromUtf8("copy_mvn_parameter_check_box"))
        self.verticalLayout_6.addWidget(self.copy_mvn_parameter_check_box)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.preview_parameters_btn = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_parameters_btn.sizePolicy().hasHeightForWidth())
        self.preview_parameters_btn.setSizePolicy(sizePolicy)
        self.preview_parameters_btn.setObjectName(_fromUtf8("preview_parameters_btn"))
        self.horizontalLayout.addWidget(self.preview_parameters_btn)
        self.copy_parameters_btn = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_parameters_btn.sizePolicy().hasHeightForWidth())
        self.copy_parameters_btn.setSizePolicy(sizePolicy)
        self.copy_parameters_btn.setObjectName(_fromUtf8("copy_parameters_btn"))
        self.horizontalLayout.addWidget(self.copy_parameters_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.gridLayout_5.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        Ui_TabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_11 = QtGui.QLabel(self.tab_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.verticalLayout_7.addWidget(self.label_11)
        self.line_5 = QtGui.QFrame(self.tab_2)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName(_fromUtf8("line_5"))
        self.verticalLayout_7.addWidget(self.line_5)
        self.backup_selection_radio_btn = QtGui.QRadioButton(self.tab_2)
        self.backup_selection_radio_btn.setObjectName(_fromUtf8("backup_selection_radio_btn"))
        self.verticalLayout_7.addWidget(self.backup_selection_radio_btn)
        self.backup_all_radio_btn = QtGui.QRadioButton(self.tab_2)
        self.backup_all_radio_btn.setObjectName(_fromUtf8("backup_all_radio_btn"))
        self.verticalLayout_7.addWidget(self.backup_all_radio_btn)
        spacerItem4 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem4)
        self.label_17 = QtGui.QLabel(self.tab_2)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.verticalLayout_7.addWidget(self.label_17)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.backup_file_path = QtGui.QLineEdit(self.tab_2)
        self.backup_file_path.setObjectName(_fromUtf8("backup_file_path"))
        self.horizontalLayout_2.addWidget(self.backup_file_path)
        self.open_file_peeker_btn = QtGui.QPushButton(self.tab_2)
        self.open_file_peeker_btn.setObjectName(_fromUtf8("open_file_peeker_btn"))
        self.horizontalLayout_2.addWidget(self.open_file_peeker_btn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.label_18 = QtGui.QLabel(self.tab_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_7.addWidget(self.label_18)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.jenkins_home_line_edit = QtGui.QLineEdit(self.tab_2)
        self.jenkins_home_line_edit.setObjectName(_fromUtf8("jenkins_home_line_edit"))
        self.horizontalLayout_4.addWidget(self.jenkins_home_line_edit)
        self.recover_config_btn = QtGui.QPushButton(self.tab_2)
        self.recover_config_btn.setObjectName(_fromUtf8("recover_config_btn"))
        self.horizontalLayout_4.addWidget(self.recover_config_btn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem5)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.save_backup_btn = QtGui.QPushButton(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_backup_btn.sizePolicy().hasHeightForWidth())
        self.save_backup_btn.setSizePolicy(sizePolicy)
        self.save_backup_btn.setMaximumSize(QtCore.QSize(84, 38))
        self.save_backup_btn.setObjectName(_fromUtf8("save_backup_btn"))
        self.horizontalLayout_3.addWidget(self.save_backup_btn)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.gridLayout_6.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        Ui_TabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(Ui_TabWidget)
        Ui_TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Ui_TabWidget)

    def retranslateUi(self, Ui_TabWidget):
        Ui_TabWidget.setWindowTitle(_translate("Ui_TabWidget", "Jenkins jobs editor", None))
        self.label_16.setText(_translate("Ui_TabWidget", "Configuration", None))
        self.label_15.setText(_translate("Ui_TabWidget", "Remote jenkins", None))
        self.remoteConfigCheckBox_2.setText(_translate("Ui_TabWidget", "enabled", None))
        self.label_12.setText(_translate("Ui_TabWidget", "host", None))
        self.label_13.setText(_translate("Ui_TabWidget", "username", None))
        self.label_14.setText(_translate("Ui_TabWidget", "password", None))
        self.label_4.setText(_translate("Ui_TabWidget", "Search results", None))
        self.saveBtn.setText(_translate("Ui_TabWidget", "Save selection", None))
        self.pushButton_3.setText(_translate("Ui_TabWidget", "Preview config", None))
        self.label_3.setText(_translate("Ui_TabWidget", "Jenkins jobs root", None))
        self.findJobsBtn.setText(_translate("Ui_TabWidget", "Find jobs", None))
        Ui_TabWidget.setTabText(Ui_TabWidget.indexOf(self.jobs_select_tab),
                                _translate("Ui_TabWidget", "Jobs selection", None))
        self.label_5.setText(_translate("Ui_TabWidget", "Parameter type", None))
        self.stringRadioBtn.setText(_translate("Ui_TabWidget", "String", None))
        self.booleanRadioBtn.setText(_translate("Ui_TabWidget", "Boolean", None))
        self.choiceRadioBtn.setText(_translate("Ui_TabWidget", "Choice", None))
        self.label_10.setText(_translate("Ui_TabWidget", "Parameter name", None))
        self.label.setText(_translate("Ui_TabWidget", "Description", None))
        self.label_8.setText(_translate("Ui_TabWidget", "Maven parameter (key=value)", None))
        self.defValLabel.setText(_translate("Ui_TabWidget", "Default value", None))
        self.addParamBtn.setText(_translate("Ui_TabWidget", "Add parameter", None))
        self.label_9.setText(_translate("Ui_TabWidget", "Not saved parameters", None))
        Ui_TabWidget.setTabText(Ui_TabWidget.indexOf(self.parameters_tab),
                                _translate("Ui_TabWidget", "Add Parameters", None))
        self.label_2.setText(_translate("Ui_TabWidget", "Source job", None))
        self.src_job_filter.setText(_translate("Ui_TabWidget", "source filter...", None))
        self.find_parameters_btn.setText(_translate("Ui_TabWidget", "Find parameters", None))
        self.label_6.setText(_translate("Ui_TabWidget", "Target jobs", None))
        self.target_job_filter.setText(_translate("Ui_TabWidget", "target filter...", None))
        self.label_7.setText(_translate("Ui_TabWidget", "Parameters to copy", None))
        self.copy_mvn_parameter_check_box.setText(
            _translate("Ui_TabWidget", "Copy maven parameter to bash script", None))
        self.preview_parameters_btn.setText(_translate("Ui_TabWidget", "Preview", None))
        self.copy_parameters_btn.setText(_translate("Ui_TabWidget", "Copy", None))
        Ui_TabWidget.setTabText(Ui_TabWidget.indexOf(self.tab), _translate("Ui_TabWidget", "Copy Parameters", None))
        self.label_11.setText(_translate("Ui_TabWidget", "Backup configuration", None))
        self.backup_selection_radio_btn.setText(_translate("Ui_TabWidget", "Backup selected jobs only", None))
        self.backup_all_radio_btn.setText(_translate("Ui_TabWidget", "Backup all jobs", None))
        self.label_17.setText(_translate("Ui_TabWidget", "Backup location", None))
        self.open_file_peeker_btn.setText(_translate("Ui_TabWidget", "Open", None))
        self.label_18.setText(_translate("Ui_TabWidget", "Jenkins home (.jenkins)", None))
        self.recover_config_btn.setText(_translate("Ui_TabWidget", "Recover", None))
        self.save_backup_btn.setText(_translate("Ui_TabWidget", "Save", None))
        Ui_TabWidget.setTabText(Ui_TabWidget.indexOf(self.tab_2), _translate("Ui_TabWidget", "Backup", None))


class JenkinsUpdateJobsGui(QTabWidget, Ui_TabWidget):
    def __init__(self, tab_widget):
        super().__init__()
        super().setupUi(tab_widget)
        logging.basicConfig(level=logging.DEBUG)
        self.current_job_search_result_data = None
        self.current_parameter_data = None
        self.job_parameters_all = None
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
            if self.config is not None and self.config.__contains__(config_name) \
                    and not is_blank(self.config[config_name]):
                line_edit.setText(self.config[config_name])

        set_config('search_path', self.lineEdit_2)
        set_config('remote_host', self.lineEdit_5)
        set_config('remote_usr', self.lineEdit_6)

        #  Search results button clicked
        self.findJobsBtn.clicked.connect(self.start_searching_jobs_list)
        self.jobsSearchResults.clicked.connect(self.jobs_search_result_list_clicked)
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
        # Sets of push buttons actions for Copy parameters tab
        self.preview_parameters_btn.clicked.connect(self.preview_parmaters)
        self.src_job_list_view.clicked.connect(self.parameters_list_clicked)
        self.find_parameters_btn.clicked.connect(self.find_parameters_to_copy)
        self.copy_parameters_btn.clicked.connect(self.copy_parameters)
        # backup buttons actions
        self.open_file_peeker_btn.clicked.connect(self.show_file_dialog)
        self.save_backup_btn.clicked.connect(self.backup)
        self.recover_config_btn.clicked.connect(self.restore_backup)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def parameters_list_clicked(self, index):
        self.current_parameter_data = index.data()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def jobs_search_result_list_clicked(self, index):
        self.current_job_search_result_data = index.data()

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
        resultModel = QStandardItemModel(self.jobsSearchResults)
        src_job_list_model = QStandardItemModel(self.src_job_list_view)
        target_job_list_model = QStandardItemModel(self.target_jobs_list_view)

        def create_model_list(result_model, temp_results, checkable=True):
            for job in sorted(temp_results.keys()):
                item = QStandardItem(job)
                item.setCheckable(checkable)
                result_model.appendRow(item)

        self.tempResults = temp_results
        create_model_list(resultModel, temp_results)
        create_model_list(src_job_list_model, temp_results, checkable=False)
        create_model_list(target_job_list_model, temp_results)
        self.jobsSearchResults.setModel(resultModel)
        # Sets model (search results) to list views in copy parameters tab
        self.src_job_list_view.setModel(src_job_list_model)
        self.target_jobs_list_view.setModel(target_job_list_model)

    def show_error_message(self, message):
        """Displays critilal QMessageBox with message. Raises JenkinsJobEditorGuiException.

         :param message: error to be displayed and raised in exception
         """
        QtGui.QMessageBox.critical(self, "Warning!", message, QtGui.QMessageBox.Ok)
        raise JenkinsJobEditorGuiException(message)

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
            self.show_error_message("Find something before viewing")
        if self.current_job_search_result_data is None:
            self.show_error_message("Select something before viewing")
        else:
            reader = configView.Ui_Form()
            popup_window = QDialog()
            reader.setupUi(popup_window)
            reader.viewTextBrowser.setText(self.jenkins_params.read_config_file(
                self.tempResults[self.current_job_search_result_data]))
            popup_window.setWindowModality(Qt.ApplicationModal)
            popup_window.show()
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
        self.jenkins_params.add_params(self._get_selected_jobs(), self.params, self.mvn_params)
        self.show_info_message("Successfully added all parameters to selected jobs")

    def _get_selected_jobs(self):
        paths = {}
        for job in self.jobs:
            paths[job] = self.tempResults[job]
        if paths.__len__() == 0:
            message = "There are no jobs selected. Cannot save parameters!"
            self.show_error_message(message)
            raise NoJobsSelectedToBackupException(message)
        return paths

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

    def preview_parmaters(self):
        model = self.src_job_list_view.model()
        if model is None or model.rowCount() == 0:
            self.show_error_message("Select something before viewing")
            return
        else:
            item = self.current_parameter_data
            param_view = parametersView.Ui_Parameters_preview()
            popup_window = QDialog()
            param_view.setupUi(popup_window)

            parameters = self.jenkins_params.read_job_all_parameters(self.tempResults[item])[0]
            parameters_model = QStandardItemModel(param_view.parameters_list_tree_view)
            for k, v in parameters.items():
                item_key = QStandardItem(k)
                item_key.setCheckable(False)
                items = []
                for key, value in v.items():
                    if key == 'name':
                        continue
                    field_name = QStandardItem(key)
                    field_name.setCheckable(False)
                    field_value = QStandardItem(value)
                    field_value.setCheckable(False)
                    field_name.appendColumn([field_value])
                    items.append(field_name)
                item_key.appendColumn(items)
                parameters_model.appendRow(item_key)
            param_view.parameters_list_tree_view.setModel(parameters_model)
            popup_window.setWindowModality(Qt.ApplicationModal)
            popup_window.exec_()

    def find_parameters_to_copy(self):
        model = self.src_job_list_view.model()
        if model is None or model.rowCount() == 0:
            self.show_error_message("Select something before viewing")
            return

        item = self.current_parameter_data
        self.job_parameters_all = self.jenkins_params.read_job_all_parameters(self.tempResults[item])
        model = QStandardItemModel(self.listView)
        for key in sorted(self.job_parameters_all[1].keys()):
            item = QStandardItem(key)
            item.setCheckable(True)
            model.appendRow(item)
        self.listView.setModel(model)

    def copy_parameters(self):
        src_model = self.src_job_list_view.model()
        target_model = self.target_jobs_list_view.model()
        parameters_model = self.listView.model()
        copy_mvn_parameter = self.copy_mvn_parameter_check_box.isChecked()

        def get_src_job_config_path():
            return self.tempResults[self.current_parameter_data]

        def get_parameters_to_copy():
            temp = {}
            for p_row in range(parameters_model.rowCount()):
                p_item = parameters_model.item(p_row)
                if p_item.checkState() == QtCore.Qt.Checked:
                    temp[p_item.text()] = True
            return {k: v for k, v in self.job_parameters_all[1].items() if temp.__contains__(k)}

        def get_target_jobs_config_paths():
            temp = {}
            for p_row in range(target_model.rowCount()):
                p_item = target_model.item(p_row)
                if p_item.checkState() == QtCore.Qt.Checked:
                    temp[p_item.text()] = (self.tempResults[p_item.text()])
            return temp

        if src_model is None or src_model.rowCount() == 0 or target_model is None or target_model.rowCount() == 0:
            self.show_error_message("Select something before viewing")
            return

        src_parameters = get_parameters_to_copy()
        for row in range(target_model.rowCount()):
            item = target_model.item(row)
            if item.checkState() == QtCore.Qt.Checked:
                try:
                    self.jenkins_params.import_job_parameters(src_parameters, get_target_jobs_config_paths(),
                                                              with_mvn_params=copy_mvn_parameter,
                                                              src_config_path=get_src_job_config_path())
                except Exception as err:
                    self.show_error_message(str(err))
        self.show_info_message("Parameters copied successfully")

    @staticmethod
    def _read_config_from_file():
        try:
            config_file = open('default.cfg')
            configs = {}
            for line in config_file:
                key, value = line.split('=')
                configs[key] = value.strip()
            return configs
        except FileNotFoundError as err:
            logging.debug(err)
        except ValueError as err:
            logging.debug("Invalid file format. {}".format(err))

    def show_file_dialog(self):
        file_path = QtGui.QFileDialog.getExistingDirectory(self)
        self.backup_file_path.setText(file_path)

    def backup(self):
        if self.backup_all_radio_btn.isChecked():
            config_paths = self.tempResults.values()
        else:
            config_paths = self._get_selected_jobs().values()
        backup_path = self.backup_file_path.text()
        if backup_path == '' or not os.path.exists(backup_path):
            self.show_error_message("{} is not valid backup path!".format(backup_path))

        self.jenkins_params.copy_configs(config_paths, target_dir=backup_path)
        self.show_info_message("Created backup at {} succeeded".format(backup_path))

    def restore_backup(self):
        self.show_error_message('Not implemented!')  # TODO don't work remotely
        backup_src = self.backup_file_path.text()
        backup_target = self.jenkins_home_line_edit.text()
        if backup_src == '' or not os.path.exists(backup_src):
            self.show_error_message('{} is not valid backup source!'.format(backup_src))
        if backup_target == '':
            self.show_error_message('{} is not valid backup target path!'.format(backup_target))
        config_paths = localUpdateJobs.JenkinsParameters(backup_src).read_all_configs(backup_src).values()
        self.jenkins_params.copy_configs(config_paths, target_dir=backup_target)


class JenkinsJobEditorGuiException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidRemoteCredentialsException(JenkinsJobEditorGuiException):
    def __init__(self, message):
        super().__init__(message)


class NoJobsSelectedToBackupException(JenkinsJobEditorGuiException):
    def __init__(self, message):
        super().__init__(message)


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
        except paramiko.ssh_exception.AuthenticationException as err:
            logging.debug(err)
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), str(err))
        except Exception as err:
            logging.debug(err)
            self.emit(SIGNAL('show_error_message(PyQt_PyObject)'), str(err))

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
