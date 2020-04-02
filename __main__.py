from idiot import Idiot

try:
    i = Idiot(6)
    i.user_step()
except Exception as e:
    print('[Ошибка]', e)
    i.save_data()
    exit(i.__EX_SOFTWARE__)