import telepot
import time
from telepot.loop import MessageLoop
import RPi.GPIO as gp


gp.setwarnings(False)
gp.setmode(gp.BOARD)


Led_pin = 7
gp.setup(Led_pin, gp.OUT)


token = '7499977661:AAFQV2pTO8Zbwl_S9y9BBbyISC7YVxnGg1o'
bot = telepot.Bot(token)
print(bot.getMe())

def led_blink(message):
    chat_id = message['chat']['id']
    cmd = message['text']
    print(f'Command received: {cmd}')

    if 'on' in cmd:
        gp.output(Led_pin, True)
        msg = "LED is turned on"
    elif 'off' in cmd:
        gp.output(Led_pin, False)
        msg = "LED is turned off"
    else:
        msg = "Invalid command, please send 'on' or 'off'"

    bot.sendMessage(chat_id, msg)

# Set up the message loop
MessageLoop(bot, led_blink).run_as_thread()
print("Listening for messages...")

try:
    while True:
        time.sleep(3)
except KeyboardInterrupt:
    print("Program stopped by user")
finally:
    gp.cleanup()
