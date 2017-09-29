'''
class related to doctors
'''
from database import Database
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

def get_doctors(_db: Database):
    '''
    Return buttons
    '''
    doctors = _db.get_doctors()
    options = [InlineKeyboardButton(
        text='{} {}'.format(doctor['first_name'], doctor['last_name']),
        callback_data='doctor_{}'.format(doctor['id'])
    ) for doctor in doctors]
    print(options)
    if doctors:
        return InlineKeyboardMarkup(
            inline_keyboard=[[doctor] for doctor in options]
        )
    return None
