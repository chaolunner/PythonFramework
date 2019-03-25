import os
import shutil

from typing import TypeVar
from typing import Union

AnyStr = TypeVar('AnyStr', bytes, str)


class OSUtility:
    app_path = os.path.abspath(os.path.join(os.getcwd(), "..\\.."))
    cur_path = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def create(path: str, s: Union[bytes, bytearray]) -> int:
        """
        'path': local path of dir/file
        """
        file_path = OSUtility.app_path + '\\' + path
        dirs_path = os.path.split(file_path)[0]
        if os.path.exists(dirs_path) is False:
            os.makedirs(dirs_path)

        if os.path.isdir(file_path) is False:
            with open(file_path, 'wb') as f:
                return f.write(s)
        return None

    @staticmethod
    def exists(path: str) -> bool:
        """
        'path': local path of dir/file
        """
        file_path = OSUtility.app_path + '\\' + path
        return os.path.exists(file_path)

    @staticmethod
    def open(path: str) -> AnyStr:
        """
        'path': local path of file
        """
        file_path = OSUtility.app_path + '\\' + path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            return None

    @staticmethod
    def remove(path: str) -> bool:
        """
        'path': local path of file
        """
        file_path = OSUtility.app_path + '\\' + path
        if os.path.exists(file_path) and os.path.isfile(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def removedirs(path: str) -> bool:
        """
        'path': local path of dir
        """
        dir_path = OSUtility.app_path + '\\' + path
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            return True
        return False
