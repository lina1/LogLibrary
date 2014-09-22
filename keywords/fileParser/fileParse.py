#-*- encoding:utf8 -*-
__author__ = 'lina'

import os
import time
from robot.api import logger


class FileParse():

    log_list = ["APACHE",
                "FTP"]

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

                logger.info("Check the file category...")
                self._check_file_cate(file, cate)

                logger.info("Check the machine name if it is localhost.localdomain ...")
                second_part = file_s[1]
                machine_name = second_part[-21:len(second_part)]
                self._check_machine_name(file, machine_name)

                logger.info("Check the timestamp and random number...")
                ctime = second_part[0:-21]
                self._check_is_digit(file, ctime)

                logger.info("Check the priority if it is a number...")
                priority = file_s[2].split(".")[0]
                self._check_is_digit(file, priority)

                logger.info("Check the file if it is a gz file...")
                file_format = file_s[2].split(".")[1]
                self._check_file_extension(file, file_format)
        return True

    def check_file_name_format_by_channel(self, dest_dir):
        """检查按channel打包的文件显示格式是否正确"""

        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_s = file.split("_")
                cate = file_s[0]

                logger.info("Check the file category...")
                self._check_file_cate(file, cate)

                machine_and_time = file_s[1].split("-")

                second_part = machine_and_time[0]

                logger.info("Check the machine name if it is localhost.localdomain ...")
                machine_name = second_part[-21:len(second_part)]
                self._check_machine_name(file, machine_name)

                logger.info("Check the timestamp and random number...")
                ctime = second_part[0:-21]
                self._check_is_digit(file, ctime)
                time_str = machine_and_time[1]

                logger.info("Check the date if it is valid...")
                self._is_valid_date(file, time_str)

                logger.info("Check the customer id...")
                self._check_is_digit(file, file_s[2])

                self._check_is_digit(file, file_s[3])

                logger.info("Check the priority if it is a number...")
                priority = file_s[4].split(".")[0]
                self._check_is_digit(file, priority)

                logger.info("Check the file if it is a gz file...")
                file_format = file_s[4].split(".")[1]
                self._check_file_extension(file, file_format)

        return True

    def check_file_name_format_by_customer(self, dest_dir):
        """检查按customer打包的文件显示格式是否正确"""

        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_s = file.split("_")
                cate = file_s[0]

                logger.info("Check the file category...")
                self._check_file_cate(file, cate)

                logger.info("Check the machine name if it is localhost.localdomain ...")
                second_part = file_s[1]
                machine_name = second_part[-21:len(second_part)]
                self._check_machine_name(file, machine_name)

                logger.info("Check the timestamp and random number...")
                ctime = second_part[0:-21]
                self._check_is_digit(file, ctime)

                self._check_is_digit(file, file_s[2])

                logger.info("Check the priority if it is a number...")
                priority = file_s[3].split(".")[0]
                self._check_is_digit(file, priority)

                logger.info("Check the file if it is a gz file...")
                file_format = file_s[3].split(".")[1]
                self._check_file_extension(file, file_format)
        return True

    def _is_valid_date(self, file, str):
        """Check if string is a valid date format"""
        try:
            time.strptime(str, "%Y%m%d")
            return True
        except:
            raise StandardError(file + ": " + str + " : is not a valid time string!!!")

    def _check_file_extension(self, file, file_format):
        """Check the file if it is a gz file"""
        if not file_format == "gz":
            raise StandardError(file + ": " + file_format + " is not a gz file!!!")

    def _check_is_digit(self, file, str):
        """Check if string is a digital"""
        if not str.isdigit():
            raise StandardError(file + ": " + str + ": is not a number!!!")

    def _check_machine_name(self, file, machine_name):
        """Check the machine name"""
        if machine_name != 'localhost.localdomain':
            raise StandardError(file + ": " + machine_name + ": the machine name is wrong!!!")

    def _check_file_cate(self, file, cate):
        """Check if the file category is in the format list"""
        if cate not in self.log_list:
            raise StandardError(file + ": " + cate + " is not in the format list!!!")


