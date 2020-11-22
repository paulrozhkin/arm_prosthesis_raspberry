'''
    interacting with the display
'''
def send_to_display():
    display_command = [123, 0xFFFF, 0xFFFF]
    print("display : ", display_command)