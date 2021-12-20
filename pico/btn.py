"""A simple program that connects the explorer buttons to a callback.

It uses a simple outer-loop to act on button presses and enact a de-bounce,
keeping the callback (ISR) short and simple.
"""

# pylint: disable=import-error, global-statement

from machine import Pin  # type: ignore
import utime  # type: ignore

# A global boolean variable,
# one for each explorer button.
_BTN_A_REQUEST: bool = False
_BTN_B_REQUEST: bool = False
_BTN_X_REQUEST: bool = False
_BTN_Y_REQUEST: bool = False


def _btn_callback(pin):
    """The button callback (ISR).

    Here we set the corresponding button request
    variable based on the given Pin identity.
    It's up to an 'outer loop' to run the actions
    for the button.
    """
    global _BTN_A_REQUEST
    global _BTN_B_REQUEST
    global _BTN_X_REQUEST
    global _BTN_Y_REQUEST

    # What GPIO pin is this?
    # We have to interrogate the string representation!
    # The string representation will be...
    #   "Pin(12, [...])"
    # ...so we just look from the 5th character (index 4)
    # and split at the comma...
    pin_id: int = int(str(pin)[4:-1].split(',')[0])  # pylint: disable=use-maxsplit-arg
    if pin_id == 12:
        _BTN_A_REQUEST = True
    elif pin_id == 13:
        _BTN_B_REQUEST = True
    elif pin_id == 14:
        _BTN_X_REQUEST = True
    elif pin_id == 15:
        _BTN_Y_REQUEST = True


def _btn():
    """The 'main loop'.

    We connect all the buttons to the callback
    and then enter an infinite-loop,
    watching the 'request' variables. For each one set
    we print a message and then (after a delay) reset the request.
    """
    global _BTN_A_REQUEST
    global _BTN_B_REQUEST
    global _BTN_X_REQUEST
    global _BTN_Y_REQUEST

    # Register each of the explorer buttons.
    # Pressing any of them runs the btn_callback() function.
    print('Registering buttons...')

    btn_a: Pin = Pin(12, Pin.IN, Pin.PULL_UP)
    btn_a.irq(trigger=Pin.IRQ_FALLING, handler=_btn_callback)

    btn_b: Pin = Pin(13, Pin.IN, Pin.PULL_UP)
    btn_b.irq(trigger=Pin.IRQ_FALLING, handler=_btn_callback)

    btn_x: Pin = Pin(14, Pin.IN, Pin.PULL_UP)
    btn_x.irq(trigger=Pin.IRQ_FALLING, handler=_btn_callback)

    btn_y: Pin = Pin(15, Pin.IN, Pin.PULL_UP)
    btn_y.irq(trigger=Pin.IRQ_FALLING, handler=_btn_callback)

    print('Registered')

    # Now just monitor the request variable for each button.
    # If it's set then act on it (here we just print the button's name)
    # then, after a short delay (to also de-bounce the button),
    # clear the request.

    print('Listening...')

    while True:

        # Flags, set if we've seen the request for a button.
        # This is used to reset the request after a short delay
        seen_a: bool = False
        seen_b: bool = False
        seen_x: bool = False
        seen_y: bool = False
        # Has any button been pressed?
        # Start each new set of actions with a delimiter ('-').
        if _BTN_A_REQUEST or _BTN_B_REQUEST or _BTN_X_REQUEST or _BTN_Y_REQUEST:
            print('-')
        # Act on each button
        if _BTN_A_REQUEST:
            print('A')
            seen_a = True
        if _BTN_B_REQUEST:
            print('B')
            seen_b = True
        if _BTN_X_REQUEST:
            print('X')
            seen_x = True
        if _BTN_Y_REQUEST:
            print('Y')
            seen_y = True

        # De-bounce delay
        utime.sleep_ms(1000)

        # Reset any button we've seen.
        # And print a symbol indicating button hadling is complete.
        if seen_a:
            _BTN_A_REQUEST = False
        if seen_b:
            _BTN_B_REQUEST = False
        if seen_x:
            _BTN_X_REQUEST = False
        if seen_y:
            _BTN_Y_REQUEST = False
        if seen_a or seen_b or seen_x or seen_y:
            print('*')


if __name__ == '__main__':
    _btn()
