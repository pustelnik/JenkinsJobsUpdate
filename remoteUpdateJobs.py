import posixpath
import re
import logging

from paramiko.client import *

import localUpdateJobs


class SSHConnection:
    def __init__(self):
        client = SSHClient()
        self.client = client

    def connect(self, host, usr, pwd):
        """Establishes remote connection to host via SSH

        :param host: remote host
        :param usr: remote user
        :param pwd: remote password
        """
        self.client.get_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(host, username=usr, password=pwd)

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)

        def has_error():
            if stderr.read().__len__() > 0:
                return True
            return False

        if not has_error():
            output = ''
            for line in stdout:
                output += line
            return output
        else:
            raise self.RemoteCmdError(stderr.read(), "Error occurred during execution of command")

    def sftp(self):
        return self.client.open_sftp()

    class RemoteCmdError(Exception):

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message


class RemoteJenkinsParameters(localUpdateJobs.JenkinsParameters):
    def __init__(self, host, usr, pwd, config_path, root_dir='.'):
        super().__init__(config_path)
        self.ssh = SSHConnection()
        self.ssh.connect(host, usr, pwd)
        self.sftp_client = self.ssh.sftp()
        self.root_dir = root_dir

    def add_params(self, config_paths, param_list, mvn_property):
        """Make a local copy of all remote configs. Adds/modifies parameters and mvn
        properties on local copy. Finally remote configs are overwritten by local
         files.

         :param config_paths: dictionary of config paths, where key is folder name and value is absolute path.
         Takes keys only.
         :param param_list: List of Parameters to add to each job config
         :param mvn_property: List of mvn_property tuples (key, value) example ('-dsome.dd, 'value')
         """
        local_config_paths = self.copy_configs(config_paths.values(), deep_copy=False)
        selected_local_config_paths = self.filter_selected_local_config_paths(config_paths, local_config_paths)
        super().add_params(selected_local_config_paths, param_list, mvn_property)
        self.override_remote_config(config_paths, local_config_paths)

    @staticmethod
    def filter_selected_local_config_paths(config_paths, local_config_paths):
        """Returns local config paths dictionary {jobName: config_path} using
        keys (jobNames(folder names)) to create new Dictionary

        :param config_paths: Dictionary with remote paths to config files
        :param local_config_paths: Dictionary with local copy of config paths"""
        selected_local_config_paths = {}
        for directory_name in config_paths.keys():
            selected_local_config_paths[directory_name] = local_config_paths[directory_name]
        return selected_local_config_paths

    def override_remote_config(self, config_paths, local_config_paths):
        """Overrides all remote configs at given paths with configuration files
        stored locally (copied to local using copy_configs method)

        :param config_paths: Dictionary {jobName: config_path} pointing to remote config.xml file locations
        :param local_config_paths: Dictionary {jobName: config_path} pointing to local config.xml file locations
        """
        for key in local_config_paths.keys():
            self.sftp_client.open(config_paths[key], 'w').write(open(local_config_paths[key]).read())

    def import_job_parameters(self, new_parameters, config_paths, with_mvn_params=False, src_config_path=''):
        local_config_paths = self.copy_configs(config_paths.values(), deep_copy=False)
        selected_local_config_paths = self.filter_selected_local_config_paths(config_paths, local_config_paths)
        super().import_job_parameters(new_parameters, selected_local_config_paths.values(), with_mvn_params)
        self.override_remote_config(config_paths, local_config_paths)

    def read_job_all_parameters(self, config_path):
        local_config_path_copy = self.copy_configs([config_path], deep_copy=False)
        return super().read_job_all_parameters(list(local_config_path_copy.values())[0])

    def read_all_configs(self, root_dir):
        """Returns parameters dictionary where key is job name
        and value is full path to config

        :param root_dir: root path for searching jobs

        """
        config_paths = {}

        def push_config(path): config_paths[posixpath.split(path)[1]] = posixpath.join(path, 'config.xml')

        [push_config(path) for path in self._read_all_paths(root_dir)]
        return config_paths

    def _read_all_paths(self, root_dir):
        result = []
        self.sftp_client.listdir(root_dir)

        def is_jenkins_folder(path):
            has_jobs_folder = False
            has_folder_config = False
            if path.endswith('xml'):
                logging.debug("wrong check at {}".format(path))
                return False
            for subdir in self.sftp_client.listdir(path):
                if not has_jobs_folder and subdir == 'jobs':
                    has_jobs_folder = True
                if not has_folder_config and subdir == 'config.xml':
                    has_folder_config = True
            folder = has_folder_config and has_jobs_folder
            if folder:
                logging.debug("{}    is folder".format(path))  # TODO mark path as directory in search result list
            return folder

        for child in self.sftp_client.listdir(root_dir):
            if is_jenkins_folder(root_dir) and child == 'config.xml':
                continue
            if child == "jobs":
                result.extend(self._read_all_paths(posixpath.join(root_dir, child)))
                continue
            elif child == 'builds' \
                    or child.endswith('Build') \
                    or child.startswith(".") \
                    or re.match('^\s\\\\..*$', child) \
                    or child == 'lastStable' \
                    or child == 'lastSuccessful' \
                    or child == 'nextBuildNumber':
                continue
            elif is_jenkins_folder(posixpath.join(root_dir, child)):
                result.extend(self._read_all_paths(posixpath.join(root_dir, child)))
                continue
            else:
                result.append(posixpath.join(root_dir, child))
        return result

    def read_config_file(self, path):
        temp = self.sftp_client.open(path)
        result = ''
        for line in temp:
            result += line
        return result
