import csv
from unittest import result
import requests
import json
import re
import os
import yaml



def post_from_csv(address: str, csv_input: str, main_topic: str):
    obj_list = []
    result_list = []
    # define pattern to remove strange characters
    pattern = r'[^A-Za-z0-9 ]+'
    base_dict = {"type": main_topic}

    with open(csv_input) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            obj_list.append(row)
    csv_file.close()

    main_row = obj_list[0]  # row
    type_row = obj_list[1]
    for title, el_type in zip(main_row, type_row):
        if title == 'id':
            base_dict[title] = ''
        else:
            base_dict[title] = {'type': el_type}


    obj_list = obj_list[2:]
    url = address


    for i, obj in enumerate(obj_list):
        for j, desc in enumerate(obj):
            # id case
            if j == 0:
                # Clean possible past values
                base_dict['id'] = ''
                id = 'urn:ngsi-ld:' + main_topic + ':' + desc.replace(" ", "")
                base_dict['id'] = id
            else:
                # Clean possible past values
                base_dict[main_row[j]]['value'] = ''

                # if not Relationship type all is well
                if not base_dict[main_row[j]]['type'] == 'Relationship':
                    if base_dict[main_row[j]]['type'] == 'Integer' or base_dict[main_row[j]]['type'] == 'Boolean':
                        base_dict[main_row[j]]['value'] = int(desc)
                    elif base_dict[main_row[j]]['type'] == 'Float':
                        base_dict[main_row[j]]['value'] = float(desc)
                    else:
                        base_dict[main_row[j]]['value'] = desc
                else:
                    # remove ref prefix
                    rel_topic = main_row[j][3:]
                    base_dict[main_row[j]]['value'] = 'urn:ngsi-ld:' + rel_topic + ':' + desc.replace(" ", "")

        print()
        payload = json.dumps(base_dict)
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        result_list.append(requests.post(url, data=payload, headers=headers))
    return result_list

def post_empty_entities(address):
    pose_dict = {
        'id': 'urn:ngsi-ld:RobotPose',
        'type': 'Pose',
        'x': {'type': 'Float', 'value': 0.0},
        'y': {'type': 'Float', 'value': 0.0},
        'z': {'type': 'Float', 'value': 0.0},
        'qx': {'type': 'Float', 'value': 0.0},
        'qy': {'type': 'Float', 'value': 0.0},
        'qz': {'type': 'Float', 'value': 0.0},
        'qw': {'type': 'Float', 'value': 0.0},
     }

    pose_dict = {
        'id': 'urn:ngsi-ld:RobotPose',
        'type': 'Pose',
        'position': {'type': 'position', 'value': [0.0, 0.0, 0.0]},
        'orientation': {'type': 'quaternion', 'value': [0.0, 0.0, 0.0]},
     }
     

    payload = json.dumps(pose_dict)
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    return requests.post(address, data=payload, headers=headers)

if __name__ == '__main__':
  with open('config.yml') as f:
       data = yaml.load(f, Loader=yaml.FullLoader)
     
  main_topic_list = ['Component', 'Step', 'Macrostep', 'UseCase']
  print("Loading on process data on fiware")
  print("*********************************")
  for main_topic in main_topic_list:
        r_list = post_from_csv(data['entities_address'], os.path.join(data['data_path'], main_topic + '.csv'), main_topic)
        is_ok = True
        for r in r_list:
            if not r.ok:
                print(main_topic.strip(), "was not uploaded successfully, check the connection to fiware and if an existing entity is already present")
                is_ok = False
        if is_ok:
            print(main_topic.strip(), "was uploaded successfully")
    
            
  
  print("*********************************")
  print("Loading empty robot pose on fiware ")
  print("*********************************")
  r = post_empty_entities(data['entities_address'])
  if r.ok:
    print("Robot pose was uploaded successfully")
  else:
    print("Robot pose was not uploaded successfully, check the connection to fiware and if an existing entity is already present")
  print("*********************************")
