import os
import re
import xml.dom.minidom
import xml.etree.ElementTree as ET
import logging
import posixpath


class JenkinsParameters:
    def __init__(self, config_path):
        if not config_path.endswith('xml'):
            pass
        else:
            self.config_path = config_path
            self.root = ET.parse(config_path)
            self.params = self.root.findall("properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions")

    def add_param(self, parameter):
        for child in self.root.iter('parameterDefinitions'):
            child.append(parameter)

    @staticmethod
    def add_param_to_tree(root, parameter):
        for child in root.iter('parameterDefinitions'):
            child.append(parameter)

    @staticmethod
    def create_parameter(param_type, name, description, param_value):
        """Create new Jenkins parameter

        :param param_type: Type of parameter (String, Boolean, Choice)
        :param name: Name of parameter
        :param description: Parameter description
        :param param_value: For String and Boolean parameter it's defaultValue, for choice parameter it's a list of choices.
        """

        def get_parameter_definition(param):
            return 'hudson.model.' + param + 'ParameterDefinition'

        def create_choice_parameter():
            choices = ET.Element('choices', {'class': 'java.util.Arrays$ArrayList'})
            a = ET.Element('a', {'class': 'string-array'})
            for val in param_value:
                element = ET.Element('string')
                element.text = val
                a.append(element)
            choices.append(a)
            parent_element.append(choices)

        parent_element = ET.Element(get_parameter_definition(param_type))
        name_el = ET.Element('name')
        name_el.text = name
        desc = ET.Element('description')
        desc.text = description
        parent_element.append(name_el)
        parent_element.append(desc)
        if param_type == 'Choice':
            create_choice_parameter()
        else:
            default_val = ET.Element('defaultValue')
            default_val.text = param_value
            parent_element.append(default_val)
        return parent_element

    def set_param_default_value(self, name, new_default_value):
        """Changes parameter default value

        :param name: Parameter name in Jenkins
        :param new_default_value: Default value of Jenkins Parameter. Can be empty string.

        """
        for child in self.root.iter('parameterDefinitions'):
            for child2 in child:
                found_match = False
                for child3 in child2:
                    try:
                        if child3.tag == 'name' and (child3.text == name or child3.attrib['name'] == name):
                            found_match = True
                    except KeyError:
                        continue
                if found_match:
                    for child3 in child2:
                        if child3.tag == 'defaultValue':
                            child3.text = new_default_value

    @staticmethod
    def is_maven_set_property_line(line):
        return not re.match('^mvn.*\\\\$', line) and re.match('^\s*["]?\w*-D.*\w*$', line)

    def add_mvn_property_to_bash_script(self, mvn_property, prop_value):
        """Adds maven property to bash script

        :param mvn_property: str property -Dsome.maven.property=${example}
        :param prop_value: str property value"""

        if self.is_mvn_property_in_bash_script(prop_value):
            logging.debug('{} is already defined in {} config file. Mvn property not added.'
                          .format(prop_value, self.config_path))
            return

        for shell in self.root.iter('hudson.tasks.Shell'):
            for command in shell:
                new_cmd = ''
                for line in command.text.splitlines():
                    if self.is_maven_set_property_line(line) \
                            and not re.match('.*\\\\$', line):
                        new_cmd += line + ' \\\n'
                        new_cmd += mvn_property + '\n'
                    else:
                        new_cmd += line + '\n'
                print('\nShell script after changes \n-------------------\n' + new_cmd)
                command.text = new_cmd

    def read_mvn_property_from_bash_script(self, parameter_name):
        """Traverse jenkins job shell script lines, looking for line
        that contains mvn property assignment to bash variable with 'parameter name'.
        Please note that this method will work only if bash shell contains command:
        'mvn compile \
           -Dsome.property=${EXAMPLE} \
           -Dother.property=${EXAMPLE2}'

        :param parameter_name: Name of jenkins parameter used to assign mvn property
        """

        def remove_escape_line(mvn_property):
            if re.match('.*\\\\$', mvn_property):
                return mvn_property.replace('\\', '')
            return mvn_property

        for shell in self.root.iter('hudson.tasks.Shell'):
            for command in shell:
                for line in command.text.splitlines():
                    if self.is_maven_set_property_line(line) and re.match('.*=\\$\\{' + parameter_name + '\\}.*', line):
                        return remove_escape_line(line)
        raise MavenPropertyNotFoundException("Could not find maven property for {} parameter".format(parameter_name))

    def is_mvn_property_in_bash_script(self, parameter_name):
        for shell in self.root.iter('hudson.tasks.Shell'):
            for command in shell:
                for line in command.text.splitlines():
                    if self.is_maven_set_property_line(line) and re.match('.*=\\$\\{' + parameter_name + '\\}.*', line):
                        return True
        return False

    def write(self, target_path='.', override_config=False):
        if override_config:
            target_path = self.config_path

        self.root.write(target_path)
        content = xml.dom.minidom.parse(open(target_path, 'r')).toprettyxml()
        file = open(target_path, 'w')
        content_no_whitespace = ''
        for elem in filter(lambda x: not re.match(r'^\s*$', x), content.splitlines()):
            content_no_whitespace += elem + '\n'
        file.write(content_no_whitespace)
        file.close()

    @staticmethod
    def write_xml_tree(root, target_path):
        root.write(target_path)
        content = xml.dom.minidom.parse(open(target_path, 'r')).toprettyxml()
        file = open(target_path, 'w')
        content_no_whitespace = ''
        for elem in filter(lambda x: not re.match(r'^\s*$', x), content.splitlines()):
            content_no_whitespace += elem + '\n'
        file.write(content_no_whitespace)
        file.close()

    def read_all_configs(self, root_dir):
        """Returns dictionary of all jenkins jobs in *search_path*

        :param root_dir: Absolute path to the top of job search

        Key is directory name and value is absolute path to this directory.
        """
        tuples = []
        result = {}

        if root_dir is None or root_dir == '':
            return tuples
        else:
            print(root_dir)

        for dirPath, subdirList, fileList in os.walk(root_dir):
            for subdir in subdirList:
                if subdir != 'jobs' and subdir != 'builds' and subdir != 'workflow' and not re.match('\d+', subdir) \
                        and not subdir.startswith(".") and not subdir.endswith('Build'):
                    for file in os.listdir(os.path.join(dirPath, subdir)):
                        if file == 'config.xml':
                            tuples.append((subdir, os.path.join(os.path.join(dirPath, subdir), file)))
        for tup in tuples:
            result[tup[0]] = tup[1]
        return result

    def add_params(self, config_paths, params, mvn_property):
        """
        Modifies config.xml files at given paths list

        :param config_paths:  dictionary of paths to Jenkins job config file (config.xml)
        :param params: List of Parameters to add to each job config
        :param mvn_property: List of mvn_property tuples (key, value) example ('-dsome.dd, 'value')
        """
        for config_path in config_paths.values():
            jenkins_param = JenkinsParameters(config_path)
            for name, param in params.items():
                jenkins_param.add_param(param)
                if mvn_property.__len__() > 0:
                    for prop in mvn_property:
                        jenkins_param.add_mvn_property_to_bash_script('\t' + prop[0] + '=' + prop[1] + '\n', prop[1])
            jenkins_param.write(override_config=True)

    def read_config_file(self, path):
        return open(path).read()

    def copy_configs(self, config_paths, target_dir='./jobs_copy', deep_copy=True):
        """Creates deep copy of given configs paths. Directory structure is
        recreated on local system.

        Returns Dictionary {job_name: pathToConfig}

        :param config_paths: List of all config paths to copy
        :param target_dir: Root directory where structure copy will be created
               system open. It will be used to read local or remote file content
        :param deep_copy: If true complete directory structure will be recreated,
                          otherwise only job name directory will be created
        """
        copy_paths = {}

        def remove_root_path(path):
            """Remove root directory from given path. Returns path (windows/linux)
             depending on the system running app.

            :param path: Linux format path
            """

            def create_path(root_dir):
                result_path = ''
                root_dir_reached = False
                for directory in path.split(posixpath.sep):
                    if directory == root_dir:
                        root_dir_reached = True
                    if root_dir_reached:
                        result_path += directory + os.path.sep
                return result_path, root_dir_reached

            result, root_reached = create_path('.jenkins' if path.__contains__('.jenkins') else 'jenkins')
            if not root_reached:
                return create_path('jobs')[0]
            return result

        for config_path in config_paths:
            dir_path, config_file = os.path.split(config_path)
            if not deep_copy:
                dir_path = os.path.split(dir_path)[1]
            else:
                dir_path = remove_root_path(dir_path)
            copy_dir_path = os.path.join(target_dir, dir_path)
            copy_file_path = os.path.join(copy_dir_path, config_file)
            if not os.path.exists(copy_dir_path):
                # creates directory tree
                os.makedirs(copy_dir_path)
            src_file = self.read_config_file(config_path)
            target_file = open(copy_file_path, 'w', encoding='utf-8')
            target_file.write(src_file)
            copy_paths[os.path.split(dir_path)[1]] = copy_file_path
        return copy_paths

    def read_parameter_by_name(self, name):
        result = {}
        for child in self.root.iter('parameterDefinitions'):
            for child2 in child:
                found_match = False
                for child3 in child2:
                    try:
                        if child3.tag == 'name' and (child3.text == name or child3.attrib['name'] == name):
                            found_match = True
                    except KeyError:
                        continue
                if found_match:
                    for child3 in child2:
                        if child.tag != name:
                            result[child3.tag] = child3.text
        return result

    def read_job_all_parameters(self, config_path):
        """Reads job all parameters and returns tuple containing
        two dictionaries, where key is parameter name.

        First element is
        a dictionary containing all fields of parameter.

        Second element is dictionary of XML elements, to
        be used to add them in different jobs"""
        result = {}
        xml_elements = {}
        root = ET.parse(config_path)
        for child in root.iter('parameterDefinitions'):
            for child2 in child:
                temp = {}
                for child3 in child2:
                    try:
                        temp[child3.tag] = child3.text
                    except KeyError:
                        continue
                result[temp['name']] = temp
                xml_elements[temp['name']] = child2
        return result, xml_elements

    def import_job_parameters(self, new_parameters, config_paths, with_mvn_params=False, src_config_path=''):
        """Adds parameters to parameterDefinitions xml tree.
        If parameter already exists, override existing. Overrides existing
        config.xml files with updated versions.

        :param src_config_path: path to config.xml file of src job
        :param config_paths: List of config.xml file locations
        :param new_parameters: tuple, where second element is
                a dictionary of xml elements (representing jenkins parameters)
        :param with_mvn_params: If true mvn parameters from bash script will be copied if don't
                don't exists in target job
        """

        def get_child_name(child_element):
            for child_2 in child_element:
                if child_2.tag == 'name':
                    return child_2.text

        for config_path in config_paths:
            root = ET.parse(config_path)
            for child in root.iter('parameterDefinitions'):
                # Remove already existing parameters
                elements_to_remove = []
                for child2 in child:
                    try:
                        if new_parameters.__contains__(get_child_name(child2)):
                            elements_to_remove.append(child2)
                    except KeyError:
                        pass
                for param in elements_to_remove:
                    child.remove(param)

            for new_parameter in new_parameters.values():
                JenkinsParameters.add_param_to_tree(root, new_parameter)

            # Adds mvn parameter job bash script
            if with_mvn_params:
                params = JenkinsParameters(config_path)
                params.root = root
                mvn_parameters_to_add = []
                for new_parameter_name in new_parameters.keys():
                    mvn_param = JenkinsParameters(src_config_path). \
                        read_mvn_property_from_bash_script(new_parameter_name)
                    mvn_parameters_to_add.append((new_parameter_name, mvn_param))
                for new_parameter in mvn_parameters_to_add:
                    params.add_mvn_property_to_bash_script(new_parameter[1], new_parameter[0])
            # Save changes
            JenkinsParameters.write_xml_tree(root, config_path)


def read_job_config(config_path):
    tree = ET.parse(config_path)
    params = tree.findall("properties/hudson.model.ParametersDefinitionProperty/parameterDefinitions")

    for param in params:
        for child in param:
            if child.tag == 'hudson.model.ChoiceParameterDefinition':
                strings = child.findall('choices/a/string')
                for string in strings:
                    print(string.text)
            else:
                print(child.find('name').text)
                print(child.find('defaultValue').text)


class MavenPropertyNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
