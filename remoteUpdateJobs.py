from paramiko.client import *
from paramiko.sftp_client import *
import re
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

    def modify_params(self, config_paths, param_list, mvn_property):
        """Make a local copy of all remote configs. Adds/modifies parameters and mvn
        properties on local copy. Finally remote configs are overwritten by local
         files.

         :param config_paths: dictionary of config paths, where key is folder name and value is absolute path.
         Takes keys only.
         :param param_list: List of Parameters to add to each job config
         :param mvn_property: List of mvn_property tuples (key, value) example ('-dsome.dd, 'value')
         """
        local_config_paths = self._copy_configs_to_local(config_paths.values())
        selected_local_config_paths = {}
        for directory_name in config_paths.keys():
            selected_local_config_paths[directory_name] = local_config_paths[directory_name]

        super().modify_params(selected_local_config_paths, param_list, mvn_property)

        for key in local_config_paths.keys():
            self.sftp_client.open(config_paths[key], 'w').write(open(local_config_paths[key]).read())

    def _copy_configs_to_local(self, config_paths):
        copy_paths = {}

        for config_path in config_paths:
            config = self.read_config_file(config_path)
            config_copy_dir_path = './jobs_copy/' + os.path.split(os.path.split(config_path)[0])[1]
            if not os.path.exists('./jobs_copy'):
                os.mkdir('./jobs_copy')
            if not os.path.exists(config_copy_dir_path):
                os.mkdir(config_copy_dir_path)
            config_copy_file_path = os.path.join(config_copy_dir_path, 'config.xml')
            config_copy = open(config_copy_file_path, 'w')
            config_copy.write(config)
            copy_paths[os.path.split(os.path.split(config_path)[0])[1]] = config_copy_file_path
        return copy_paths

    def read_all_configs(self, root_dir):
        """Returns parameters dictionary where key is job name
        and value is full path to config

        :param root_dir: root path for searching jobs

        """
        config_paths = {}

        def push_config(path): config_paths[os.path.split(path)[1]] = os.path.join(path, 'config.xml')

        [push_config(path) for path in self._read_all_paths(root_dir)]
        return config_paths

    def _read_all_paths(self, root_dir):
        result = []

        self.sftp_client.listdir(root_dir)

        def is_dir(path, what):
            for subdir in self.sftp_client.listdir(path):
                if subdir == what:
                    return True
            return False

        for child in self.sftp_client.listdir(root_dir):
            if child == "jobs" or is_dir(os.path.join(root_dir, child), 'jobs'):
                result.extend(self._read_all_paths(os.path.join(root_dir, child)))
            elif child == 'builds' or child.endswith('Build') or child.startswith(".") \
                    or re.match('^\s\\\\..*$', child):
                continue
            elif is_dir(os.path.join(root_dir, child), 'config.xml'):
                result.append(os.path.join(root_dir, child))
        return result

    def read_config_file(self, path):
        temp = self.sftp_client.open(path)
        result = ''
        for line in temp:
            result += line
        return result
