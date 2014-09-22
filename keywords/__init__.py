__author__ = 'lina'

from configParser.propertyConfig import PropertyConfig
from fileDiff.filediff import FileDiff
from configParser.jsonConfig import JsonConfig
from fileParser.fileParse import FileParse


class LogKeywords(PropertyConfig,
                  FileDiff,
                  JsonConfig,
                  FileParse):

    pass

