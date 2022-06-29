import database.db as db
from models.Account import Account
from models.Earning import Earning
from models.Spending import Spending
from datetime import datetime
from sqlalchemy import extract

def get_about_this(VERSION):
    response = (
        f"Simple Expenses Bot (pyTelegramBot) v{VERSION}"
        "\n\n"
        "Desarrollado por Héctor Martínez <hector.martinezg@autonoma.edu.co>"
    )
    return response

def get_help_message ():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n"
        "*gane|gané|g {cantidad}* - Registra un saldo positivo\n"
        "*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n"
        "*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
        "*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes/año\n"
        "*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
        "*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
        "*listar cuentas|lc* - Lista las cuentas registradas (sóloadmin)\n"
    )
    return response

def get_welcome_message(bot_data):
    response = (
        f"Hola, soy *{bot_data.first_name}* "
        f"también conocido como *{bot_data.username}*.\n\n"
        "¡Estoy aquí para ayudarte a registrar tus gastos!"
    )
    return response

def register_account(user_id):
    account = db.session.query(Account).get(user_id)
    
    db.session.commit()
    
    if account == None:
        account = Account(user_id, 0)
        db.session.add(account)
        db.session.commit()
        return True
    
    return False

def get_balance (user_id):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    
    if not account:
        return None
    
    return account.balance

def earn_money (user_id, amount):
    if amount <= 0:
        return False
    
    control = update_account (user_id, amount)
    
    if not control:
        return False
    
    earn = Earning(
            amount,
            datetime.now(),
            user_id)
    
    db.session.add(earn)
    db.session.commit()
    
    return True

def update_account (user_id, amount):
    account = db.session.query(Account).get(user_id)
    db.session.commit()
    
    if not account:
        return False
    
    account.balance = account.balance + amount
    db.session.commit()
    
    return True

def list_earnings (user_id, month, year):
    earnings = db.session.query(
        Earning
    ).filter_by(
        accounts_id=user_id
    ).filter(
        extract('month', Earning.when) == month
    ).filter(
        extract('year', Earning.when) == year
    ).all()
    
    db.session.commit()
    
    return earnings