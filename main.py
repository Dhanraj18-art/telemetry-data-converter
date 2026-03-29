import json
import unittest
import datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    locationParts = jsonObject['location'].split("/")

    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

    return result


def convertFromFormat2(jsonObject):
    date = datetime.datetime.strptime(jsonObject['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    timestamp = int(date.timestamp() * 1000)

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['location']['country'],
            'city': jsonObject['location']['city'],
            'area': jsonObject['location']['area'],
            'factory': jsonObject['location']['factory'],
            'section': jsonObject['location']['section']
        },
        'data': jsonObject['data']
    }

    return result


def main(jsonObject):
    if(jsonObject.get('device') == None):
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult)


if __name__ == '__main__':
    unittest.main()