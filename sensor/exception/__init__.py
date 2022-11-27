import sys

'''
Exception is name of parent class of Sensor Exception
Sensor_Exception is inheriting parent class Exception
'''
class Sensor_Exception(Exception):

    def __init__(self, error_msg, error_detail: sys) -> None:
        '''super refers to parent classs, here we are passing error_msg to the init of parent class'''
        super().__init__(error_msg)
        self.error_msg = error_message_detail(error_msg, error_detail = error_detail)

    def __str__(self) -> str:
        return self.error_msg


def error_message_detail(error, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        lineNumber = exc_tb.tb_lineno
        error_msg = f"Error occured in python script name [{filename}] line number [{lineNumber}] error message [{str(error)}]\n"

        return error_msg