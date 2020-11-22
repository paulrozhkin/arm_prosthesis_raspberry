import random
'''
mocks instead of real interfaces
'''
def ADC_MOCK():
    return random.randint(0, 65535)

def SPI_TELEMETRY_REQUEST_MOCK():
    A = 0
    B = random.randint(0, 65535)
    C = random.randint(0, 65535)
    D = random.randint(0, 65535)
    E = random.randint(0, 65535)
    F = random.randint(0, 65535)
    G = random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)
    I = random.randint(0, 65535)
    J = random.randint(0, 65535)
    K = random.randint(0, 65535)
    L = random.randint(0, 65535)
    M = random.randint(0, 65535)
    N = random.randint(0, 65535)
    O = random.randint(0, 65535)
    P = random.randint(0, 65535)

    telemetry_request = [A, B, C, D, E, F, G, CRC8, I, J, K, L, M, N, O, P]
    return telemetry_request

def SPI_SET_POSITION_ANSWER_MOCK():
    A = random.randint(0, 65535)
    B = random.randint(0, 65535)
    C = random.randint(0, 65535)
    D = random.randint(0, 65535)
    E = random.randint(0, 65535)
    F = random.randint(0, 65535)
    G = random.randint(0, 65535)
    H = random.randint(0, 65535)
    I = 1
    CurrentRegime = random.randint(0, 3)
    PointerFingerPosition = random.randint(0, 65535)
    MiddleFingerPosition = random.randint(0, 65535)
    RingFinderPosition = random.randint(0, 65535)
    LittleFingerPosition = random.randint(0, 65535)
    ThumbFingerPosition = random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)

    answer = [A, B, C, D, E, F, G, H, I, CurrentRegime,
               PointerFingerPosition, MiddleFingerPosition, RingFinderPosition,
               LittleFingerPosition, ThumbFingerPosition, CRC8]
    return answer

def SPI_MOCK(spi_request):
    if spi_request[0] == 0:
        return SPI_TELEMETRY_REQUEST_MOCK()
    else:
        return SPI_SET_POSITION_ANSWER_MOCK()

def SPI_SET_POSITION_REQUEST(action):
    A = 1
    B = random.randint(0, 65535)
    PointerFingerPosition = action.PointerFingerPosition    #random.randint(0, 65535)
    MiddleFingerPosition = action.MiddleFingerPosition  #random.randint(0, 65535)
    RingFinderPosition = action.RingFinderPosition  #random.randint(0, 65535)
    LittleFingerPosition = action.LittleFingerPosition  #random.randint(0, 65535)
    ThumbFingerPosition = action.ThumbFingerPosition    #random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)
    I = random.randint(0, 65535)
    G = random.randint(0, 65535)
    K = random.randint(0, 65535)
    L = random.randint(0, 65535)
    M = random.randint(0, 65535)
    N = random.randint(0, 65535)
    O = random.randint(0, 65535)
    P = random.randint(0, 65535)
    request = [A, B, PointerFingerPosition, MiddleFingerPosition, RingFinderPosition,
               LittleFingerPosition, ThumbFingerPosition, CRC8, I, G, K, L, M, N, O, P]
    return request

