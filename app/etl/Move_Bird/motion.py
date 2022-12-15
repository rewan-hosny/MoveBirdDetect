import os
import re


class ClsMotion (object):
    def __init__(self):
        pass

    def process_frames(self, framesPath):
        frames = os.listdir (framesPath)  # A list of the Labeling
        # seconds = []  # A list of the Seconds
        dict_frame_time = {}  # dict of second as a key and pose as a value
        # Extract the second from the img_name
        for fileName in frames:
            frame_second = re.findall (r'\d+', fileName)  # list of one element i.e. ['0001'])
            # fill file name without time for all frames
            frame_time = float (frame_second[0])
            dict_frame_time[frame_time] = os.path.splitext (fileName)[0].replace (frame_second[0], '')
            '''x = (fileName.split(".", 1)[1])
        statusOfHeads.append(x.split('_', 1)[0])
        res = list(map(int, frame_second))
        seconds.append(res)
        '''
        # self.get_pose(dict_frame_time)
        # self.get_motion_per_time(dict_frame_time)
        return self.get_motion_per_time (dict_frame_time)

    def get_motion_per_time(self, dict_frame_time):
        pose_change = False
        '''
https://stackoverflow.com/questions/36184371/iterate-over-a-dict-except-for-x-item-items
for key,value in (i for i in columns.items() if not i==('key_x',value_x)):
    do something
https://stackoverflow.com/questions/65975676/is-it-possible-to-iterate-through-all-of-a-dictionarys-keys-except-a-specific-s
for key in set(dictionary) - set([1, 2, 3]):
    print(key)    
        '''

        head = 0
        leg = 1
        wing = 2
        tail = 3
        center = 0
        right = 1
        left = 2
        none = -1
        down = 0
        up = 1
        off = 0
        on = 1

        # shrf=5
        result = {}

        dict_pose_change = {head: False, leg: False, wing: False, tail: False}
        dict_pose_startTime = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        dict_pose_endTime = {head: 0.0, leg: 0.0, wing: 0.0, tail: 0.0}
        list_of_sorted_keys = list (sorted (dict_frame_time))
        # print(dict_frame_time)
        for index, cur_time in enumerate (sorted (dict_frame_time)):
            if len (dict_frame_time) - index == 1:
                break
            else:
                result[cur_time] = {}
                frame_curr = dict_frame_time[cur_time]
                time_next = list_of_sorted_keys[index + 1]
                frame_next = dict_frame_time[time_next]
                # print((frame_curr , frame_next))
                birds_curr = self.get_pose (frame_curr)
                birds_next = self.get_pose (frame_next)
                # if there is a diff create a new obj that contain a time
                # print((birds_next, birds_curr))
                diff = self.get_difference (birds_curr, birds_next)
                # print(diff)

                if diff != None:
                    for birdPart in diff.keys ():
                        if not dict_pose_change[birdPart]:
                            dict_pose_startTime[birdPart] = time_next
                            dict_pose_change[birdPart] = True
                        else:
                            dict_pose_endTime[birdPart] = time_next
                            dict_pose_change[birdPart] = False
                            delta = dict_pose_endTime[birdPart] - dict_pose_startTime[birdPart]
                            # obj = ((dict_pose_startTime[birdPart], delta), birdPart)
                            result[cur_time][birdPart] = (dict_pose_startTime[birdPart], delta)

                            # print(obj)
                            # changes_arr.append(obj)

                    # if(shrf>0):
                    #     if(result[cur_time]!={}):
                    #         print('5555555555555555555555555555')
                    #         print(cur_time)
                    #         print(result[cur_time])
                    #         print('55555555555555555555555555555')
                    #         shrf=shrf-1

        # print(result[1])
        return result

    def get_difference(self, first_dict, second_dict):
        '''
        i.e. [{head:right , leg:up, tail:left , wing:on }]
        i.e. [{head:left , leg:down, tail:left , wing:on }]
        result will be   [{head:left , leg:down}]
        :param first_dict:
        :param second_dict:
        :return: dict of the differences like [{head:left , leg:down}]
        '''
        try:
            first_dict = set (first_dict.items ())
            second_dict = set (second_dict.items ())
            return dict (first_dict - second_dict)
        except:
            pass

    # def json_evaluate(self, json_file):
    #     #evaluated_json_file = json.loads(json_file)
    #     with open(json_file, 'r') as f:
    #         json_text = f.read()
    #
    #     # Decode the JSON string into a Python dictionary.
    #     esra_dict = json.loads(json_text)
    #

    def get_pose(self, file_name):
        '''
        a dict for each bird in the frame
        if a frame contain one bird then the list contain one dict
        i.e. [{head:right , leg:up, tail:left , wing:on }]
        Parameters:
        fileName_withoutTime_withoutExt: fileName withoutTime withoutExt
        Returns:
        listOfDict : return List of Dict
        '''

        head = 0
        leg = 1
        wing = 2
        tail = 3
        center = 0
        right = 1
        left = 2
        none = -1
        down = 0
        up = 1
        off = 0
        on = 1

        # if we take just one name
        try:
            file_name_trimmed = file_name.replace ('.', ':').replace ('_', ',').lower ()
            file_name_trimmed = ('{%s}' % file_name_trimmed)
            file_name_trimmed = eval (file_name_trimmed)
            return file_name_trimmed
        except:
            pass
