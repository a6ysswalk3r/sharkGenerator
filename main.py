from libs import generatePassword
from configparser import ConfigParser
import time

def viewSettings(config):

    config.read("config.ini")

    view = ""
    for i in config["passwd_chars"]:
        if config["passwd_chars"][i] == "True":
            view += "• " + i + ": 🗹\n"
        else:
            view += "• " + i + ": ☒\n" 
    return view

def changeSettings(cfg):
    
    print("\n[!] Настройки символов из которых будет сгенерирован пароль")
    
    settingsList = ["upper", "lower", "digits", "puncts"]
    print(viewSettings(cfg))
    while True:
        print("1 - верхний регистр, 2 - нижний регистр, 3 - цифры, 4 - спец символы и любое положительное число - для выхода")
        choiceForChange = input("\nВвод: ")
        if choiceForChange.isdigit():
            if 0 < int(choiceForChange) < 5:
                
                config.read("config.ini")
                temp = config["passwd_chars"][settingsList[int(choiceForChange) - 1]]
                config["passwd_chars"][settingsList[int(choiceForChange) - 1]] = "False" if temp == "True" else "True"
                
                with open ("config.ini", "w") as cfgFile:
                    config.write(cfgFile)
                
                print(viewSettings(cfg))

            else:
                return "settings"
        else:
            print("[!!] Неверное значение! Список из доступных команд ниже:")
                
def main(choice, config):
    
    # Если функция получила число, значит это длинна и её нужно записать в config файлы
    if choice.isdigit():
        if int(choice) >= 4 and int(choice) <= 128:
            config.read("config.ini")
            config["settings"]["len"] = choice

            with open("config.ini", "w") as configF:
                config.write(configF)
            print("[!] Изменения сохранены!")
        else:
            return "falseLen"
    elif choice.lower() == "g":
        if len(generatePassword.addConstsOfModuleString(config)) > 0:
            config.read("config.ini")
            newPasswd = generatePassword.getSecretString(int(config["settings"]["len"]))
            print("[!] Новый пароль: " + newPasswd)
        else:
            return "noneSimbols"
    elif choice.lower() == "q":
        return "exit"
    elif choice.lower() == "s":
        return changeSettings(config)
    else:
        return "false"
    
    return "completed"

def start():    
    dictExceptMessages = {
        "falseLen": "\n[!!] Генерируемый пароль может быть длиной только от 4 до 128 символов!",
        "exit": "\n[!] Программа успешно завершена :)",
        "false": "\n[!] Неверный ввод!",
        "settings": "\n[!] Изменения сохранены!",
        "completed": 0,
        "noneSimbols": "\n[!] Генерация невозможна в настройках в генерацию не включён хотя бы один список символов!",
        "isunknown": "\n[!] Возникла неизвестная ошибка!",
        "fnotfound": "\n[!] Файл конфигурации повреждён или не найден!"
    }

    print("\n[!] Введите s - настройки, q - выход, g - генерация или", end=' ')
    print("любое неотрицательное число для определения длины генерируемого пароля")

    try:
        response = main(input("Ввод: "), config)
        if response != "false" and response != "exit" and response != "completed":
            print(dictExceptMessages[response])
        elif response == "false":
            print(dictExceptMessages[response])
        elif response == "completed":
            pass
        else:
            return dictExceptMessages[response]
    except KeyError:
        return dictExceptMessages["isunknown"]
    except FileNotFoundError:
        return dictExceptMessages["fnotfound"]

    time.sleep(0.5)
    return start()

config = ConfigParser()
logo = """ 
        ▄████████    ▄██████▄  
    ███    ███   ███    ███ 
    ███    █▀    ███    █▀  
    ███         ▄███        
    ▀███████████ ▀▀███ ████▄  
            ███   ███    ███ 
    ▄█    ███   ███    ███ 
    ▄████████▀    ████████▀  
                            
    """
print(logo + "— — SharkGenerator — —\n\t\t\t\t.by dap0pe", "\n")
print(start())
