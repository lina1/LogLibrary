#-*- encoding:utf-8 -*-
__author__ = 'lina'

import gzip
import filecmp
from filecmp import dircmp
import os
import shutil
from keywords.exceptions import FileNotSameError


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
        """Return the line number of a file"""
        with open(file) as f:
            return sum(line.count("\n") for line in self._block(f))

    def _divide_file_by_hash(self, file_path, target_dir, split_number=20):
        """Divide a file by hash.

        Args:

            file_path: the file needed to be divided.

            target_dir: a directory used to save the divided files.

            split_number: how many files should the file need to be divided to.

        """
        file_handler = open(file_path)
        for log in file_handler:
            log_info = log.strip("\n")

            log_hash = hash(log_info)
            hash_value = log_hash % split_number
            file = open(target_dir + os.sep + "file_" + str(hash_value) + ".txt", "a+")
            file.write(str(log_hash) + "\n")

            file.close()
        file_handler.close()

    def _generate_file_hash_to_set(self, file_name):
        """Read hash value from the file and generate them into a set.

        Args:

            file_name: the file contains the hash values.

        Return:

            A set which contains the hash value.
        """
        hash_set = set()
        f = open(file_name)
        for line in open(file_name):
            line = f.readline()
            hash_set.add(line)

        return hash_set

    def _make_dir(self, dir):
        """Create a dir if it does not exist."""
        if not os.path.exists(dir):
            os.mkdir(dir)

    def _remove_dir(self, dir):
        """Remove a dir if it exists."""
        if os.path.exists(dir):
            shutil.rmtree(dir)

    def file_cmp(self, base_file, new_file):
        """Compare if two files are the same, regardless of the line number."""
        if filecmp.cmp(base_file, new_file, False):
            return True

        else:
            base_line_number = self._get_file_line_number(base_file)
            new_line_number = self._get_file_line_number(new_file)

            if base_line_number != new_line_number:

                raise FileNotSameError(base_file + " and " + new_file + " has different line numbers!!!")

            else:

                pwd_dir = os.getcwd()

                sep = os.sep

                base_dir = pwd_dir + sep + "base" + sep
                new_dir = pwd_dir + sep + "new" + sep

                try:

                    self._make_dir(base_dir)
                    self._make_dir(new_dir)

                    self._divide_file_by_hash(base_file, base_dir)
                    self._divide_file_by_hash(new_file, new_dir)
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
                                pass
                            else:
                                if set1-set2:
                                    print set1-set2
                                else:
                                    print set2-set1

                                raise FileNotSameError(base_file + " and " + new_file + " are not the same!!!")
                    return True
                finally:
                    self._remove_dir(base_dir)
                    self._remove_dir(new_dir)

    def gz_file_cmp(self, base_gz_file, new_gz_file):
        """Compare two .gz file if they are the same."""

        base_file = self._gz_file_unzip(base_gz_file)

        new_file = self._gz_file_unzip(new_gz_file)
        try:

            return self.file_cmp(base_file, new_file)

        finally:
            os.remove(base_file)
            os.remove(new_file)

    def _gz_file_unzip(self, gz_file):
        """Unzip a gz file.

        Args:

            gz_file: the file needed to be unziped.

        """

        unzip_file_name = gz_file.replace(".gz", "")

        file_path = os.getcwd() + os.sep + "tmp"

        file_name = file_path + unzip_file_name[-10:-1]

        g_file = gzip.open(gz_file)

        self._make_dir(file_path)
        open(file_name, "w+").write(g_file.read())
        g_file.close()

        return file_name

    def dest_dir_cmp(self, base_dest_dir, new_dest_dir):
        """Compare two directory"""
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



