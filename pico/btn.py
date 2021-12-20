"""A simple program that connects the explorer buttons to a callback.
It uses a sinple outer-loop to act on button presses and enact a debounce,
This keeps the callcak (ISR) short and simple.
"""

from machine import Pin
import utime

# A global boolean variable,
# one for each explorer button.
btn_a_request = False
btn_b_request = False
btn_x_request = False
btn_y_request = False


def btn_callback(pin):
    """The button callback (ISR).

    Here we set the corresponding button request
    variable based on the given Pin identity.
    It's up to an 'outer loop' to run the actions
    for the button.
    """
    global btn_a_request
    global btn_b_request
    global btn_x_request
    global btn_y_request

    # What GPIO pin is this?
    # We have to interrogate the string representation!
    pin_id = int(str(pin)[4:-1].split(',')[0])
    if pin_id == 12:
        btn_a_request = True
    elif pin_id == 13:
        btn_b_request = True
    elif pin_id == 14:
        btn_x_request = True
    elif pin_id == 15:
        btn_y_request = True


def btn():
    global btn_a_request
    global btn_b_request
    global btn_x_request
    global btn_y_request

    # Register each of the explorer buttons.
    # Pressing any of them runs the btn_callback() function.
    print('Registering buttons...')

    btn_a = Pin(12, Pin.IN, Pin.PULL_UP)
    btn_a.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

    btn_b = Pin(13, Pin.IN, Pin.PULL_UP)
    btn_b.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

    btn_x = Pin(14, Pin.IN, Pin.PULL_UP)
    btn_x.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

    btn_y = Pin(15, Pin.IN, Pin.PULL_UP)
    btn_y.irq(trigger=Pin.IRQ_FALLING, handler=btn_callback)

    print('Registered')

    # Now just monitor the request variable for each button.
    # If it's set then act on it (here we just print the button's name)
    # then, after a short delay (to also de-bounce the button),
    # clear the request.
    
    print('Listening...')

    while True:
    
        # Flags, set if we've seen the request for a button.
        # This is used to reset the request after a short delay
        seen_a = False
        seen_b = False
        seen_x = False
        seen_y = False
        # Has any button been pressed?
        # Start each new set of actions with a delimiter ('-').
        if btn_a_request or btn_b_request or btn_x_request or btn_y_request:
            print('-')
        # Act on each button
        if btn_a_request:
            print('A')
            seen_a = True
        if btn_b_request:
            print('B')
            seen_b = True
        if btn_x_request:
            print('X')
            seen_x = True
        if btn_y_request:
            print('Y')
            seen_y = True

        # De-bounce delay
        utime.sleep_ms(1000)
        
        # Reset any button we've seen.
        # And print a symbol indicating button hadling is complete.
        if seen_a:
            btn_a_request = False
        if seen_b:
            btn_b_request = False
        if seen_x:
            btn_x_request = False
        if seen_y:
            btn_y_request = False
        if seen_a or seen_b or seen_x or seen_y:
            print('*')


if __name__ == '__main__':
    btn()
