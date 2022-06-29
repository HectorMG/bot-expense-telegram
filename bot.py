#########################################################

from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    
#########################################################


@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    bot.send_message(
        message.chat.id,
        logic.get_welcome_message(bot.get_me()),
        parse_mode="Markdown")
    
    bot.send_message(
        message.chat.id,
        logic.get_help_message(),
        parse_mode="Markdown")
    
    bot.send_message(
        message.chat.id,
        message.from_user,
        parse_mode="Markdown")
    
    logic.register_account(message.from_user.id)

#########################################################

@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(
        message.chat.id,
        logic.get_help_message(),
        parse_mode="Markdown") 

#########################################################

@bot.message_handler(commands=['about'])
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    bot.send_message(
        message.chat.id,
        logic.get_about_this(config.VERSION), 
        parse_mode="Markdown")

#########################################################

@bot.message_handler(regexp=r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$")
def on_earn_money(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    parts = re.match(
            r"^(gane|gané|g) ([+-]?([0-9]*[.])?[0-9]+)$",
            message.text,
            flags=re.IGNORECASE)
    
    # print (parts.groups())
    amount = float(parts[2])
    
    control = logic.earn_money (message.from_user.id, amount)
    bot.reply_to(
        message,
        f"\U0001F4B0 ¡Dinero ganado!: {amount}" if control == True
        else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta /start y vuelve a intentarlo")

#########################################################

@bot.message_handler(regexp=r"^(gaste|gasté|gg) ([+-]?([0-9]*[.])?[0-9]+)$")
def on_spend_money(message):
    pass

#########################################################

@bot.message_handler(regexp=r"^(listar ganancias|lg) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_earnings(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    parts = re.match(
        r"^(listar ganancias|lg) en ([0-9]{1,2}) de ([0-9]{4})$",
        message.text,
        flags=re.IGNORECASE)

    month = int(parts[2])
    year = int(parts[3])
    
    if month < 1 or month > 12:
        bot.reply_to(message, f"Error, mes inválido: {month}")
        return
    
    if year < 1990 or year > 2050:
        bot.reply_to(message, f"Error, año inválido: {year}")
        return
    
    earnings = logic.list_earnings(message.from_user.id, month, year)
    
    text = ""
    total = 0
    
    if not earnings:
        text = f"\U0001F633 No tienes ganancias registradas en {month}/{year}"
    else:
        text = "``` Listado de ganancias:\n\n"
        
    for e in earnings:
        total += e.amount
        text += f"| {e.id} | ${e.amount} | ({e.when.strftime('%d/%m/%Y -%H:%M')}) |\n"
        
    text += f"\nTOTAL = ${total}"
    text += "```"
        
    bot.reply_to(message, text, parse_mode="Markdown")

#########################################################

@bot.message_handler(regexp=r"^(listar gastos|lgg) en ([0-9]{1,2}) de ([0-9]{4})$")
def on_list_spendings(message):
    pass

#########################################################

@bot.message_handler(regexp=r"^(obtener saldo|s)$")
def on_get_balance(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    balance = logic.get_balance (message.from_user.id)
    text = "\U0000274C Aún no tienes una cuenta asociada, ejecuta /start para arreglarlo."
    
    if balance != None:
        text = f"Tu saldo actual es ${balance}"
        
    bot.reply_to(message, text)

#########################################################

@bot.message_handler(regexp=r"^(remover|r) (ganancia|g|gasto|gg) ([0-9]+)$")
def on_remove_record(message):
    pass

#########################################################

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    
    response = logic.get_fallback_message(message.text)
    bot.reply_to(message, response)

#########################################################

if __name__ == '__main__':
    bot.polling(timeout=20)
    
#########################################################