from num2words import num2words


def convert_to_rubles(num):
    # Разделяем число на рубли и копейки
    rubles = int(num)  # Целая часть (рубли)
    kopecks = round((num - rubles) * 100)  # Дробная часть (копейки)

    # Преобразуем рубли в текст
    rubles_text = num2words(rubles, lang='ru').replace('-', ' ').replace('  ', ' ')

    # Делаем первую букву заглавной
    rubles_text = rubles_text.capitalize()

    # Форматируем копейки как 00, если их нет
    kopecks_text = f"{kopecks:02}"

    # Формируем окончательную строку
    rubles_word = 'рублей' if rubles != 1 else 'рубль'
    kopecks_word = 'копеек' if kopecks != 1 else 'копейка'

    # Возвращаем итоговую строку
    return f"{rubles_text} {rubles_word} {kopecks_text} {kopecks_word}"


def calculate_vat(amount_without_vat, vat_rate=20):

    vat_amount = (amount_without_vat * vat_rate) / 100

    return vat_amount

