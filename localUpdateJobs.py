import os
import re
import xml.dom.minidom
import xml.etree.ElementTree as ET

jenkins_jobs_path = "/home/jakubp/.jenkins/jobs"


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

    def add_mvn_property_to_bash_script(self, mvn_property, prop_value):
        """Adds maven property to bash script

        :param mvn_property: str property -Dsome.maven.property
        :param prop_value: str property value"""
        for shell in self.root.iter('hudson.tasks.Shell'):
            for command in shell:
                new_cmd = ''
                for line in command.text.splitlines():
                    if not re.match('^mvn.*\\\\$', line) and re.match('^\s*-D.*\s*$', line) \
                            and not re.match('.*\\\\$', line):
                        new_cmd += line + ' \\\n'
                        new_cmd += '\t' + mvn_property + '=' + prop_value + '\n'
                    else:
                        new_cmd += line + '\n'
                print('\nShell script after changes \n-------------------\n' + new_cmd)

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
                if subdir != 'jobs' and subdir != 'builds' and subdir != 'workflow' and not re.match('\d+', subdir)\
                        and not subdir.startswith(".") and not subdir.endswith('Build'):
                    for file in os.listdir(os.path.join(dirPath, subdir)):
                        if file == 'config.xml':
                            tuples.append((subdir, os.path.join(os.path.join(dirPath, subdir), file)))
        for tup in tuples:
            result[tup[0]] = tup[1]
        return result

    def modify_params(self, config_paths, params, mvn_property):
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
                        jenkins_param.add_mvn_property_to_bash_script(prop[0], prop[1])
            jenkins_param.write(override_config=True)

    def read_config_file(self, path):
        return open(path).read()


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
