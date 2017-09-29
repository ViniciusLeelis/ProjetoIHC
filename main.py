'''
Entry-point do bot. Para executá-lo use
python <token de api>
'''
import sys
import time
import telepot
import doctors
from database import Database
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def handle(msg):
    '''
    Handles the incoming messages.
    '''
    flavor = telepot.flavor(msg)

    if flavor == 'chat':
        # pylint: disable=W0612
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            BOT.sendMessage(
                chat_id,
                'What do you want to do?',
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text='Schedule an appointment 🗓️',
                        callback_data='schedule_appointment'
                    ),
                    InlineKeyboardButton(
                        text='Cancel an appointment ❌',
                        callback_data='cancel_appointment'
                    )
                ]])
            )
    elif flavor == 'callback_query':
        # pylint: disable=W0612
        msg_id, chat_id, text = telepot.glance(msg, flavor=flavor)
        if text == 'schedule_appointment':
            doctor_options = doctors.get_doctors(BOT_DATABASE)
            if doctor_options is not None:
                BOT.sendMessage(
                    chat_id,
                    'These are the available doctors:',
                    reply_markup=doctor_options
                )
            else:
                BOT.sendMessage(chat_id, 'No doctors were found, sorry!')
        elif text == 'cancel_appointment':
            # show user's current appointments
            pass
        elif text.startswith('remove_appointment_'):
            # cancel user's appointment
            pass

BOT_DATABASE = Database()
API_TOKEN = '423201815:AAGYwsTIK6j8PNDalJitnL1BMpPWY2R_83M'#sys.argv[1]
BOT = telepot.Bot(API_TOKEN)
MessageLoop(BOT, handle).run_as_thread()
print('Working...')

while 1:
    time.sleep(10)
