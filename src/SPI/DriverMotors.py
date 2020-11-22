from resources.Mocks import *
from resources.DataStructures import GestureAction

''' 
    interacting with Driver Motors
'''
def get_telemetry(target):
    global driver_state
    if target == "SPI":
        request = SPI_TELEMETRY_REQUEST_MOCK()
        telemetry = SPI_MOCK(request)
        print("TELEMETRY: ", telemetry)
        driver_state = telemetry
    return driver_state

def get_SPI_answer():
    set_position_request = SPI_SET_POSITION_REQUEST(GestureAction(0, 0, 0, 0, 0, 0))
    spi_answer = SPI_MOCK(set_position_request)
    print("SPI_ANSWER: ", spi_answer)

def SPI_send_set_position_request(action):
    request = SPI_SET_POSITION_REQUEST(action)
    print("Set Pos Request: ", request)
