#-*- encoding:utf8 -*-
__author__ = 'lina'

import ConfigParser


class PropertyConfig():

    def set_property(self, key, value, file_name):
        """配置system.properties文件, 设置某一项的值

        参数：
        key

        value

        file_name: properties文件的路径

        """
        self._add_section(file_name)

        c = ConfigParser.ConfigParser()
        c.optionxform = str
        c.read(file_name)

        c.set("default", key, value)
        c.write(open(file_name, "w"))

        self._clear_section(file_name)

    def clear_property(self, key, file_name):
        """配置system.properties文件, 清除某一项

        参数：
        key

        file_name: properties文件的路径

        """

        self._add_section(file_name)

        c = ConfigParser.ConfigParser()
        c.optionxform = str
        c.read(file_name)

        c.remove_option("default", key)
        c.write(open(file_name, "w"))

        self._clear_section(file_name)

    def _add_section(self, file_name, section="[default]"):

        conf_list = open(file_name).read().split("\n")
        conf_list.insert(0, section)
        fp = open(file_name, "w")
        fp.write("\n".join(conf_list))
        fp.close()

    def _clear_section(self, file_name):

        conf_list = open(file_name).read().split("\n")
        conf_list.pop(0)
        fp = open(file_name, "w")
        fp.write("\n".join(conf_list))
        fp.close()


