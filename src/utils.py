import hashlib


class Singleton:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self


def generate_uuid(data):
    """
    Emote UUID generator by name, author, description.
    """
    # f50ec0b7-f960-400d-91f0-c42a6d44e3d0
    #
    string = '0123456789abcdef'
    unic = data['name'].lower() + data['author'].lower() + data['description'].lower()
    unic = unic.replace(' ', '')
    uuid = sum([ord(x) for x in hashlib.md5(unic.encode()).hexdigest()])
    bighash = 89809223 + uuid
    uuid = ''.join([string[x] if x < len(string) else string[x - 16] for x in [bighash % i for i in range(1, 33)]])
    uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

    return uuid