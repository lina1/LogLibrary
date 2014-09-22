#-*- encoding:utf-8 -*-
__author__ = 'lina'

import gzip
import filecmp
from filecmp import dircmp
import os
import shutil


class FileDiff():

    def __init__(self):
        pass

    def _block(self, file, size=65536):
        while True:
            nb = file.read(size)
            if not nb:
                break
            yield nb

    def _get_gz_file_line_number(self, file):
        """Return the line number of .gz file"""

        with gzip.open(file) as f:
            return sum(line.count("\n") for line in self._block(f))

    def _get_file_line_number(self, file):

        with open(file) as f:
            return sum(line.count("\n") for line in self._block(f))

    def _divide_file_by_hash(self, file_path, target_dir, split_number):
        file_handler = open(file_path)
        for log in file_handler:
            log_info = log.strip("\n")

            log_hash = hash(log_info)
            hash_value = log_hash % split_number
            file = open(target_dir + "\\file_" + str(hash_value) + ".txt", "a+")
            file.write(str(log_hash) + "\n")

            file.close()
        file_handler.close()

    def _generate_file_hash_to_set(self, file_name):
        hash_set = set()
        f = open(file_name)
        for line in open(file_name):
            line = f.readline()
            hash_set.add(line)

        return hash_set

    def _make_dir(self, dir):
        if not os.path.exists(dir):
            os.mkdir(dir)

    def _remove_dir(self, dir):
        if os.path.exists(dir):
            shutil.rmtree(dir)

    def file_cmp(self, base_file, new_file):

        if filecmp.cmp(base_file, new_file, False):
            return True

        else:
            base_line_number = self._get_file_line_number(base_file)
            new_line_number = self._get_file_line_number(new_file)

            if base_line_number != new_line_number:
                print "Different line number!!!"
                return False

            else:
                try:

                    base_dir = "../../resources/base/"
                    new_dir = "../../resources/new/"
                    self._make_dir(base_dir)
                    self._make_dir(new_dir)

                    self._divide_file_by_hash(base_file, base_dir, 20)
                    self._divide_file_by_hash(new_file, new_dir, 20)
                    dcmp = dircmp(base_dir, new_dir)
                    left_only = dcmp.left_only
                    right_only = dcmp.right_only
                    diff_files = dcmp.diff_files

                    if left_only or right_only:
                        return False
                    if diff_files:
                        for name in diff_files:
                            file1 = base_dir + name
                            file2 = new_dir + name
                            set1 = self._generate_file_hash_to_set(file1)
                            set2 = self._generate_file_hash_to_set(file2)

                            if set1 == set2:
                                return True
                            else:
                                return False
                    return True
                finally:
                    self._remove_dir(base_dir)
                    self._remove_dir(new_dir)

    def gz_file_cmp(self, base_gz_file, new_gz_file):

        try:

            base_file = self._gz_file_unzip(base_gz_file)
            # print "*"*20
            #
            # print os.getcwd()
            #
            # print base_file

            new_file = self._gz_file_unzip(new_gz_file)

            return self.file_cmp(base_file, new_file)
        finally:
            os.remove(base_file)
            os.remove(new_file)

    def _gz_file_unzip(self, gz_file):

        unzip_file_name = gz_file.replace(".gz","")

        file_path = "../../resources/tmp/"

        file_name = file_path + unzip_file_name[-10:-1]
        print "#"*20
        # print os.getcwd()
        # print file_name
        print gz_file
        g_file = gzip.open(gz_file)

        self._make_dir(file_path)
        open(file_name, "w+").write(g_file.read())
        g_file.close()

        return file_name

    def dest_dir_cmp(self, base_dest_dir, new_dest_dir):
        dcmp = dircmp(base_dest_dir, new_dest_dir)

        left_only = dcmp.left_only
        right_only = dcmp.right_only
        diff_files = dcmp.diff_files

        if left_only or right_only:
            return False
        if diff_files:
            for name in diff_files:
                base_file = base_dest_dir + name
                new_file = new_dest_dir + name
                return self.gz_file_cmp(base_file, new_file)
        return True

