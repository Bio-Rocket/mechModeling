import json

'''LoadJson(path)
    Summary:
        Loads a json file into a python dictionary.

    Arguments:
        path:
            The absolute file path of the .json file to load. 

    Returns:
        contents:
            Python dictionary containing the information in the .json file
'''
def LoadJson(path):
    with open(path) as file:
        contents = json.load(file)

    file.close()

    return contents