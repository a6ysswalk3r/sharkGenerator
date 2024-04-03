from string import ascii_uppercase, ascii_lowercase, digits, punctuation
from configparser import ConfigParser
import secrets

# Функция генерации самого пароля
def generatePasswd(lenPasswd, rndmAllSimbols):
    
    passwd = ""
    for i in range(0, lenPasswd):
        passwd += secrets.choice(rndmAllSimbols)
    return passwd


def addConstsOfModuleString(config):
    
    config.read("config.ini")
    # Cоздаю словарь с цифровыми значениями, они пригодятся в дальнейшем для создания строки с символами для пароля
    dictChars = {
        "0": ascii_uppercase,
        "1": ascii_lowercase,
        "2": digits,
        "3": punctuation
    }
    
    # Создаём строку символов для генерации пароля по настройкам, которые задал пользователь
    allSimbols = ""
    n = 0
    for i in config["passwd_chars"].values():
        if i == "True":
            allSimbols += dictChars[str(n)]
        n += 1

    return allSimbols

# Функция, которая возвращает криптографически безопасную строку из всех символов
def getSecretString(lenPasswd):
    config = ConfigParser()    
    config.read("config.ini")

    allSimbols = addConstsOfModuleString(config)

    # Далее создаю строку со случайными позициями символов из массива выше. Короче говоря, делаю безопасную строку
    # из символов
    rndmAllSimbols = []
    for i in range(0, len(allSimbols)):
        rndmAllSimbols.append(secrets.choice(allSimbols)) 
    else:
        return generatePasswd(lenPasswd, rndmAllSimbols) # Возвращаю безопасную строку
