__author__ = 'lina'

import json
import demjson


class JsonConfig():

    def insert_json(self, base_json_file, to_file):

        base_json = json.load(file(base_json_file))

        if isinstance(base_json, dict):

            channel_id = base_json["channel_id"]

            to_json_list = json.load(file(to_file))

            for item in to_json_list:
                if item["channel_id"] == channel_id:
                    to_json_list.remove(item)
                    break
            to_json_list.append(base_json)

            demjson.encode_to_file(to_file, to_json_list, overwrite=True)

    def remove_json_by_channel_id(self, channel_id, to_file):

        to_json_list = json.load(file(to_file))

        for item in to_json_list:
            if item["channel_id"] == channel_id:
                to_json_list.remove(item)
                break

        demjson.encode_to_file(to_file, to_json_list, overwrite=True)

    def remove_json(self, base_json_file, to_file):

        base_json = json.load(file(base_json_file))

        if isinstance(base_json, dict):

            to_json_list = json.load(file(to_file))

            for item in to_json_list:
                if item == base_json:
                    to_json_list.remove(item)
                    break

            demjson.encode_to_file(to_file, to_json_list, overwrite=True)





    # def insert_json(self, json):


# v = json.load(file("E:\\robotframework\\resources\\adam_channels.conf"))
# print type(v)
# jc = JsonConfig()
# jc.remove_json_by_channel_id("24711", "E:\\robotframework\\resources\\adam_channels.conf")
# jc.remove_json("E:\\robotframework\\basic.json","E:\\robotframework\\resources\\adam_channels.conf")
# jc.insert_json("E:\\robotframework\\basic.json","E:\\robotframework\\resources\\adam_channels.conf")