#-*- encoding:utf8 -*-
__author__ = 'lina'

import os


class FileParse():

    log_list = ["APACHE", "FTP"]

    def __init__(self):

        pass

    def get_log_cate_number(self, dest_dir):
        """返回某目录下日志格式的种类"""
        file_set = set()

        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                log_cate = file.split("_")[0]
                file_set.add(log_cate)
        return file_set.__len__()

    def check_file_name_format_by_priority(self, dest_dir):
        """检查按priority打包的文件显示格式是否正确"""

        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_s = file.split("_")
                cate = file_s[0]

                if cate not in self.log_list:
                    raise StandardError(file + ": " + cate + " is not in the format list!!!")

                second_part = file_s[1]
                machine_name = second_part[-21:len(second_part)]
                if machine_name != 'localhost.localdomain':
                    raise StandardError(file + ": " + machine_name + ": the machine name is wrong!!!")

                ctime = second_part[0:-21]
                if not ctime.isdigit():
                    raise StandardError(file + ": " + ctime + ": the timestamp is wrong!!!")

                priority = file_s[2].split(".")[0]
                if not priority.isdigit():
                    raise StandardError(file + ": " + priority + ": the priority is not a number!!!")

                file_format = file_s[2].split(".")[1]
                if not file_format == "gz":
                    raise StandardError(file + ": " + file_format + " is not a gz file!!!")
        return True

    def check_file_name_format_by_channel(self, dest_dir):
        """检查按channel打包的文件显示格式是否正确"""

        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_s = file.split("_")
                cate = file_s[0]

                if cate not in self.log_list:
                    raise StandardError(file + ": " + cate + " is not in the format list!!!")

                second_part = file_s[1]
                machine_name = second_part[-21:len(second_part)]
                if machine_name != 'localhost.localdomain':
                    raise StandardError(file + ": " + machine_name + ": the machine name is wrong!!!")

                ctime = second_part[0:-21]
                if not ctime.isdigit():
                    raise StandardError(file + ": " + ctime + ": the timestamp is wrong!!!")

                if not (file_s[2].isdigit() or file_s[3].isdigit()):
                    raise StandardError(file + ": the customer id is wrong!!!")

                priority = file_s[4].split(".")[0]
                if not priority.isdigit():
                    raise StandardError(file + ": " + priority + ": the priority is not a number!!!")

                file_format = file_s[4].split(".")[1]
                if not file_format == "gz":
                    raise StandardError(file + ": " + file_format + " is not a gz file!!!")
        return True


# fp = FileParse()
# print fp.check_file_name_format_by_channel("E:\\testdata")

