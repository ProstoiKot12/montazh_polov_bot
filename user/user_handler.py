import math
from datetime import datetime
import os
import re

from aiogram import Bot
from dotenv import load_dotenv

from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from user.user_keyboards import (specify_phone_kb, main_menu_call_kb, choices_material_kb, choices_height_kb,
                                 choices_freight_elevator_kb, choices_zapil_kb, choices_sealing_kb,
                                 floor_type_kb, iam_in_city_kb, choices_material_panel_kb, choices_mdf_par_panel_kb,
                                 choices_dur_par_panel_kb, choices_height_alum_kb, choices_color_kb,
                                 choices_consumables_kb, choices_pan_shpon_height_kb)
from request.sql_request import insert_into_user_table
from request.google_request import insert_new
from utils.text import *


class Form(StatesGroup):
    start_of_recording_count = State()
    start_of_recording_height = State()
    start_of_recording_material = State()
    start_of_recording_zapil_quantity_v = State()
    start_of_recording_zapil_quantity_k = State()
    start_of_recording_zapil_quantity_m = State()
    start_of_recording_sealing_up = State()
    start_of_recording_sealing_uniq = State()
    start_of_recording_freight_elevator = State()
    start_of_recording_address = State()
    start_of_recording_phone = State()
    start_of_recording_date = State()
    start_of_recording_comment = State()
    start_of_recording_name = State()
    start_of_recording_floor_type = State()
    start_of_recording_range = State()
    start_of_recording_recognize_us = State()


async def start_handler(message: Message, bot: Bot):
    photo = FSInputFile("files/main_menu_photo.jpg")
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=start_text,
                         reply_markup=main_menu_call_kb)


async def start_of_recording_name(message: Message, state: FSMContext):
    name_pattern = re.compile(r'^\w+\s\w+$')  # Регулярное выражение для формата "Слово слово"

    if name_pattern.match(message.text):
        await state.update_data(name=message.text)
        await message.answer('Выберите <b>тип</b>', reply_markup=floor_type_kb)
        await state.set_state(Form.start_of_recording_floor_type)
    else:
        await message.answer('Введите имя и фамилию')


async def start_of_recording_floor_type(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    last_check = 'Осталось 13 пункта'

    if call.data == 'plintus_type':
        await state.update_data(floor_type='Плинтус')
    elif call.data == 'panel_type':
        await state.update_data(floor_type='Панели')
    data = await state.get_data()

    if data['floor_type'] == 'Панели':
        last_check = 'Осталось 10 пунктов'
    await call.message.answer('Введите <b>кол-во метров</b>\n\n'
                             f'{last_check}')
    await state.set_state(Form.start_of_recording_count)


async def start_of_recording_count(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    data = await state.get_data()

    if message.text.isdigit():
        if data['floor_type'] == 'Панели':
                await message.answer('Выберите <b>материал</b>\n\n'
                             'осталось 9 пунктов', reply_markup=choices_material_panel_kb)
                await state.set_state(Form.start_of_recording_material)
        else:
            await message.answer('Выберите <b>материал</b>\n\n'
                             'осталось 12 пунктов', reply_markup=choices_material_kb)
            await state.set_state(Form.start_of_recording_material)
    else:
        await message.answer('Введите цифры')


async def start_of_recording_material_call(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer('')
    data = await state.get_data()

    text = ''

    if data['floor_type'] == 'Панели':
        if call.data == "mdf_choices":
            text = "МДФ"

            await call.message.answer('Выберите <b>параметр</b>\n\n'
                             'осталось 8 пунктов', reply_markup=choices_mdf_par_panel_kb)

        elif call.data == 'duropolimer_choices':
            text = "Дюрополимер"

            await call.message.answer('Выберите <b>параметр</b>\n\n'
                             'осталось 8 пунктов', reply_markup=choices_dur_par_panel_kb)

        await state.update_data(material=text)

    else:
        if call.data == "mdf_choices":
            text = "МДФ"
            await call.message.answer('Выберите <b>цвет</b>\n'
                                      '*Если выберите текстурированные то клиент покупает акриловый герметик в цвет плинтуса самостоятельно\n\n'
                             'осталось 12 пунктов', reply_markup=choices_color_kb)
        elif call.data == 'duropolimer_choices':
            text = "Дюрополимер"
            await call.message.answer('Выберите <b>высоту</b> цена за ед.\n\n'
                             'осталось 11 пунктов', reply_markup=choices_height_kb)
        elif call.data == 'shadow_choices':
            await state.update_data(height='Теневые плинтуса')
            text = "Теневые плинтуса"
            photo_zapil_k = FSInputFile("files/zapil_k.jpg")
            photo_zapil_m = FSInputFile("files/zapil_m.jpg")
            photo_zapil_v = FSInputFile("files/zapil_v.jpg")

            await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_k, caption="Запил <b>конверт</b>")
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_v, caption="Запил <b>выворотка</b>")
            await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_m,
                                 caption="Запил <b>для дверей скрытого монтажа</b>")

            await call.message.answer('Выберите <b>запил</b>\n\n'
                                      'осталось 10 пунктов', reply_markup=choices_zapil_kb)

        elif call.data == 'shopinrovan_choices':
            text = "Шпонированные"
            await call.message.answer('Выберите <b>высоту</b> цена за ед.\n\n'
                             'осталось 11 пунктов', reply_markup=choices_pan_shpon_height_kb)
        elif call.data == 'alum_choices':
            text = 'Алюминиевые'
            await call.message.answer('Выберите <b>высоту</b> цена за ед.\n\n'
                             'осталось 8 пунктов', reply_markup=choices_height_alum_kb)

        await state.update_data(material=text)

        await state.set_state(Form.start_of_recording_height)


async def mdf_choices_color_call(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    mdf_color = ''

    if call.data == 'mdf_choices_color_white':
        mdf_color = 'Белый'
    elif call.data == 'mdf_choices_color_tekstur':
        mdf_color = 'Текстурированный'

    await state.update_data(mdf_color=mdf_color)
    await call.message.answer('Выберите <b>высоту</b> цена за ед.\n\n'
                             'осталось 11 пунктов', reply_markup=choices_height_kb)


async def start_of_recording_height_call(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer('')

    await state.update_data(height=call.data)

    photo_zapil_k = FSInputFile("files/zapil_k.jpg")
    photo_zapil_m = FSInputFile("files/zapil_m.jpg")
    photo_zapil_v = FSInputFile("files/zapil_v.jpg")

    await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_k, caption="Запил <b>конверт</b>")
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_v, caption="Запил <b>выворотка</b>")
    await bot.send_photo(chat_id=call.message.chat.id, photo=photo_zapil_m, caption="Запил <b>для дверей скрытого монтажа</b>")

    await call.message.answer('Выберите <b>запил</b>\n\n'
                             'осталось 10 пунктов', reply_markup=choices_zapil_kb)
    await state.set_state(Form.start_of_recording_zapil_quantity_v)


async def start_of_recording_zapil_quantity_v(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    if call.data == 'zapil_k':
        await state.update_data(zapil_quantity_v='0')
        await state.update_data(zapil_quantity_m='0')
        await state.update_data(zapil_quantity_k=None)

        await call.message.answer('Введите <b>кол-во запилов конверт</b> 250₽ за шт')
        await state.set_state(Form.start_of_recording_zapil_quantity_k)
    elif call.data == 'zapil_v':
        await state.update_data(zapil_quantity_k='0')
        await state.update_data(zapil_quantity_m='0')
        await state.update_data(zapil_quantity_v=None)

        await call.message.answer('Введите <b>кол-во запилов выворотка</b> 190 за шт')
        await state.set_state(Form.start_of_recording_zapil_quantity_k)
    elif call.data == 'zapil_m':
        await state.update_data(zapil_quantity_v='0')
        await state.update_data(zapil_quantity_k='0')
        await state.update_data(zapil_quantity_m=None)

        await call.message.answer('Введите <b>для дверей скрытого монтажа</b> 250₽ за шт')
        await state.set_state(Form.start_of_recording_zapil_quantity_k)
    elif call.data == 'zapil_master':
        await state.update_data(zapil_quantity_k='Выберу с мастером')
        await state.update_data(zapil_quantity_v='Выберу с мастером')
        await state.update_data(zapil_quantity_m='Выберу с мастером')
        await call.message.answer('Выберите <b>тип гермитизации</b>\n\n'
                             'осталось 9 пунктов', reply_markup=choices_sealing_kb)
        await state.set_state(Form.start_of_recording_sealing_up)


async def start_of_recording_zapil_quantity_k(message: Message, state: FSMContext):
    if message.text.strip().isdigit():
        data = await state.get_data()

        if data['zapil_quantity_v'] == '0' and data['zapil_quantity_m'] == '0':
            await state.update_data(zapil_quantity_k=message.text.strip())
        elif data['zapil_quantity_k'] == '0' and data['zapil_quantity_m'] == '0':
            await state.update_data(zapil_quantity_v=message.text.strip())
        elif data['zapil_quantity_k'] == '0' and data['zapil_quantity_v'] == '0':
            await state.update_data(zapil_quantity_m=message.text.strip())
        await message.answer('Выберите <b>тип гермитизации</b>\n\n'
                             'осталось 9 пунктов', reply_markup=choices_sealing_kb)
    else:
        await message.answer('Введите только цифры')


async def start_of_recording_sealing_call(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    if call.data == "sealing_up":
        await call.message.answer("Введите кол-во <b>гермитизации по верху</b>")
        await state.update_data(sealing_uniq="0")
        await state.set_state(Form.start_of_recording_sealing_up)
    elif call.data == "sealing_uniq":
        await call.message.answer('Введите <b>отдельно герметизацию соединения</b> 50₽ штука')
        await state.update_data(sealing_up="0")
        await state.set_state(Form.start_of_recording_sealing_uniq)
    elif call.data == 'sealing_master':
        await state.update_data(sealing_up="Выберу с мастером")
        await state.update_data(sealing_uniq="Выберу с мастером")
        await call.message.answer('Есть ли <b>грузовой лифт?</b>\n'
                                  '*если нет то +1500₽\n\n'
                             'осталось 8 пунктов', reply_markup=choices_freight_elevator_kb)
        await state.set_state(Form.start_of_recording_freight_elevator)


async def start_of_recording_sealing_up(message: Message, state: FSMContext):
    if message.text.strip().isdigit():
        if message.text.strip() == "0":
            await message.answer('Введите <b>отдельно герметизацию соединения</b> 50₽ штука')
            await state.update_data(sealing_up=message.text.strip())
            await state.set_state(Form.start_of_recording_sealing_uniq)
        else:
            await state.update_data(sealing_up=message.text.strip())
            await state.update_data(sealing_uniq="0")
            await message.answer('Есть ли <b>грузовой лифт?</b>\n'
                                 '*если нет то +1500₽\n\n'
                             'осталось 7 пунктов', reply_markup=choices_freight_elevator_kb)
            await state.set_state(Form.start_of_recording_freight_elevator)
    else:
        await message.answer('Введите только цифры')


async def start_of_recording_sealing_uniq(message: Message, state: FSMContext):
    if message.text.strip().isdigit():
        await state.update_data(sealing_uniq=message.text.strip())
        await message.answer('Есть ли <b>грузовой лифт?</b>\n'
                             '*если нет то +1500₽\n\n'
                             'осталось 7 пунктов', reply_markup=choices_freight_elevator_kb)
        await state.set_state(Form.start_of_recording_freight_elevator)
    else:
        await message.answer('Введите только цифры')


async def start_of_recording_sealing_uniq_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    data = await state.get_data()

    if data['material'] == 'Алюминиевые':
        await state.update_data(height=call.data)
        await call.message.answer('Есть ли <b>грузовой лифт?</b>\n'
                                  '*если нет то +1500₽\n\n'
                                  'Осталось 7 пунктов', reply_markup=choices_freight_elevator_kb)
        await state.set_state(Form.start_of_recording_freight_elevator)
    else:
        await state.update_data(material_par=call.data)
        await call.message.answer('Есть ли <b>грузовой лифт?</b>\n'
                                '*если нет то +1500₽\n\n'
                                  'Осталось 7 пунктов', reply_markup=choices_freight_elevator_kb)
        await state.set_state(Form.start_of_recording_freight_elevator)


async def start_of_recording_freight_elevator_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    result = ''
    if call.data == "yes_freight_elevator":
        result = 'Да'
    elif call.data == "no_freight_elevator":
        result = 'Нет'
    await state.update_data(freight_elevator=result)
    await call.message.answer('Нужны ли <b>расходные материалы</b>\n'
                              '*Материалы на весь объем: клей основной, двухкомпонентный клей, акриловая шпаклевка\n'
                              '*За каждые 10 погонных метров 1000 рублей\n\n'
                              'Осталось 6 пунктов', reply_markup=choices_consumables_kb)
    await state.set_state(Form.start_of_recording_range)


async def start_of_recording_consumables_callback(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    result = ''

    if call.data == 'choices_consumables_yes':
        result = 'Да'
    elif call.data == 'choices_consumables_no':
        result = 'Нет'

    await state.update_data(consumables=result)
    await call.message.answer('Введите свой <b>адрес</b>\n\n'
                              'Осталось 5 пунктов')
    await state.set_state(Form.start_of_recording_range)


async def start_of_recording_range(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer('Введите на сколько километров вы за чертой города или если вы в одном '
                              'из ниже перечисленных районов то выберите его\n'
                              'Каждые 10 км + 500 рублей\n\n'
                              'Мурино, Девяткино, Новоселье, Кудрово - 500 р\n'
                              'Пушкин, Павловск, Петергоф, Красное село - 800 р\n\n'
                         'Осталось 4 пункта', reply_markup=iam_in_city_kb)
    await state.set_state(Form.start_of_recording_address)


async def start_of_recording_address(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(range=message.text)
        await message.answer('Укажите свой <b>номер телефона</b> нажав на кнопку снизу или введя его',
                             reply_markup=specify_phone_kb)
        await state.set_state(Form.start_of_recording_phone)
    else:
        await message.answer('Введите на сколько километров вы за чертой города\n\n', reply_markup=iam_in_city_kb)


async def start_of_recording_address_call(call: CallbackQuery, state: FSMContext):
    await call.answer('')
    if call.data == 'iam_in_city':
        await state.update_data(range='0')
    elif call.data == 'murino':
        await state.update_data(range='Мурино')
    elif call.data == 'devyatkino':
        await state.update_data(range='Девяткино')
    elif call.data == 'novoselye':
        await state.update_data(range='Новоселье')
    elif call.data == 'kudrovo':
        await state.update_data(range='Кудрово')
    elif call.data == 'pushkin':
        await state.update_data(range='Пушкин')
    elif call.data == 'pavlovsk':
        await state.update_data(range='Павловск')
    elif call.data == 'petergof':
        await state.update_data(range='Петергоф')
    elif call.data == 'red_village':
        await state.update_data(range='Красное село')

    await call.message.answer('Укажите свой <b>номер телефона</b> нажав на кнопку снизу или введя его\n\n'
                              'Осталось 3 пункта',
                         reply_markup=specify_phone_kb)
    await state.set_state(Form.start_of_recording_phone)


async def start_of_recording_phone(message: Message, state: FSMContext):
    try:
        await state.update_data(phone=message.contact.phone_number)

        await message.answer('Откуда вы о нас узнали\n\n'
                             'Осталось 2 пункта', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Form.start_of_recording_recognize_us)
    except:
        pattern = re.compile(r'^\+\d{11}$')
        if pattern.match(message.text.strip()):
            await state.update_data(phone=message.text.strip())
            await message.answer('Откуда вы о нас узнали\n\n'
                             'Осталось 2 пункта', reply_markup=ReplyKeyboardRemove())
            await state.set_state(Form.start_of_recording_recognize_us)
        else:
            await message.answer('Введите номер в формате +71234567890')


async def start_of_recording_recognize_us(message: Message, state: FSMContext):
    await state.update_data(recognize_us=message.text)
    data = await state.get_data()
    await message.answer('Введите <b>комментарий</b>\n\n'
                         'Остался 1 пункт')
    await state.set_state(Form.start_of_recording_comment)


async def start_of_recording_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text.strip())

    await message.answer('Введите <b>дату</b> в формате <b>ГГГГ-ММ-ДД</b>\n\n'
                         'Это последний пункт')
    await state.set_state(Form.start_of_recording_date)


async def start_of_recording_date(message: Message, state: FSMContext, bot: Bot):
    load_dotenv()
    date_str = message.text.strip()

    mdf_color = 'Нету'

    data = await state.get_data()

    name = data["name"]
    range_s = data["range"]
    material = data['material']
    floor_type = data["floor_type"]
    count = data["count"]
    freight_elevator = data["freight_elevator"]
    consumables = data["consumables"]
    address = data["address"]
    phone = data["phone"]
    comment = data["comment"]
    recognize_us = data["recognize_us"]

    count_google = f"Кол-во метров: {count}"
    floor_type_google = f"Тип: {floor_type}"
    freight_elevator_google = f"Есть ли грузовой лифт: {freight_elevator}"
    consumables_g = f"Расходные материалы: {consumables}"
    material_google = f"Материал: {material}"
    address_google = f"Адрес: {address}"
    phone_google = f"Телефон: {phone}"
    comment_google = f"Комментарий: {comment}"
    user_id_google = f"User_id: {message.from_user.id}"
    name_google = f"Имя: {name}"
    recognize_us_google = f"Откуда о нас узнали: {recognize_us}"

    user_name = message.from_user.username

    if user_name is None:
        user_name = phone

    if data['floor_type'] == 'Панели':

        material_par = data["material_par"]

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            await message.answer('Некорректный формат даты. Введите дату в формате ГГГГ-ММ-ДД.')
            return

        height_price = 0

        range_price = 0

        if range_s == '0':
            range_price = 0
        elif range_s == 'Мурино' or range_s == 'Девяткино' or range_s == 'Новоселье' or range_s == 'Кудрово':
            range_price = 500
        elif range_s == 'Пушкин' or range_s == 'Павловск' or range_s == 'Петергоф' or range_s == 'Красное село':
            range_price = 800
        else:
            range_s = math.ceil(int(range_s) / 10) * 10
            c = range_s // 10
            range_price = c * 500

        freight_elevator_price = "0"

        if freight_elevator == "Нет":
            freight_elevator_price = 1500

        if material_par == '50_mdf':
            height_price = 350
            material_par = 'До 50 мм МДФ'
        elif material_par == '100_mdf':
            height_price = 400
            material_par = 'До 100 мм МДФ'
        elif material_par == '240_mdf':
            height_price = 500
            material_par = 'До 240 мм МДФ'
        elif material_par == '50_dur':
            height_price = 400
            material_par = 'До 50 мм Дюрополимер'
        elif material_par == '100_dur':
            height_price = 450
            material_par = 'До 100 мм Дюрополимер'
        elif material_par == '240_dur':
            height_price = 550
            material_par = 'До 240 мм Дюрополимер'
        # count_s = 0
        # if material == 'Шпонированные':
        #     for row in range(int(count)):
        #         count_s += row

        price = (int(count) * height_price + int(freight_elevator_price) + range_price)

        if consumables == 'Да':
            consumables_metres = math.ceil(int(count) / 10)
            price += 1000 * consumables_metres


        if price < 5500:
            price = 5500

        height_google = f"Параметр: {material_par}"
        zapil_quantity_v_google = f"Запил выворотка: {0}"
        zapil_quantity_k_google = f"Запил конверт: {0}"
        zapil_quantity_m_google = f"Запил для дверей скрытого монтажа: {0}"
        sealing_uniq_google = f"Отдельная герметизация соединения: {0}"
        sealing_up_google = f"Герметизиция по верху: {0}"
        mdf_color_g = f"Цвет: {mdf_color}"
        material_sign = 'Панели'

        await insert_new(count_google, height_google, material_google, address_google, phone_google, date,
                         zapil_quantity_v_google, zapil_quantity_k_google,
                         zapil_quantity_m_google, freight_elevator_google, sealing_uniq_google, sealing_up_google,
                         user_id_google, comment_google, name_google, floor_type_google, recognize_us_google,
                         consumables_g, mdf_color_g, material_sign)

        message_text = (f'Отлично, <b>{name}</b>, вы записаны на <b>{date}</b>\n\n'
                        f"<b>Цена</b>: {price} рублей\n"
                        f"<b>Дата</b>: {date}\n"
                        f"<b>Кол-во метров</b>: {count}\n"
                        f"<b>Тип</b>: {floor_type}\n"
                        f"<b>Параметр</b>: {material_par}\n"
                        f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                        f"<b>Расходные материалы</b>: {consumables}\n"
                        f"<b>Материал:</b> {material}\n"
                        f"<b>Адрес</b>: <code>{address}</code>\n"
                        f"<b>Номер</b>: <code>{phone}</code>\n"
                        f"<b>Откуда о нас узнали</b>: {recognize_us}\n"
                        f"<b>Комментарий</b>: <b>{comment}</b>\n\n"
                        f'*ждите подтверждение вашей записи\n'
                        f'*расходные материалы в виде клея в стоимость монтажа не входят\n'
                        f'*в минимальный заказ входит монтаж плинтуса со всеми углами\n\n'
                        f'После получения заказа мы с Вами связемся для подтвержения!'
                        f' Либо можете уточнить у нас по номеру телефона +79045150339\n')
        if price == 5500:
            message_text = f"{message_text} *минимальная сумма заказа от 5500 рублей"

        await message.answer(message_text)

        await bot.send_message(chat_id=os.getenv("CHAT_ID"), text="<b>Новая заявка</b>\n\n"
                                                                  f"<b>Имя</b>: {name}\n"
                                                                  f"<b>Цена</b>: {price} рублей\n"
                                                                  f"<b>Дата</b>: {date}\n"
                                                                  f"<b>Кол-во метров</b>: {count}\n"
                                                                  f"<b>Тип</b>: {floor_type}\n"
                                                                  f"<b>Параметр</b>: {material_par}\n"
                                                                  f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                                                                  f"<b>Расходные материалы</b>: {consumables}\n"
                                                                  f"<b>Материал:</b> {material}\n"
                                                                  f"<b>Адрес</b>: <code>{address}</code>\n"
                                                                  f"<b>Номер</b>: <code>{phone}</code>\n"
                                                                  f"<b>Откуда о нас узнали</b>: {recognize_us}"
                                                                  f"<b>User name</b>: <a href='https://t.me/{user_name}'>{user_name}</a>\n"
                                                                  f"<b>Комментарий</b>: <b>{comment}</b>\n")
    elif data['material'] == 'Алюминиевые':

        height = data["height"]

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            await message.answer('Некорректный формат даты. Введите дату в формате ГГГГ-ММ-ДД.')
            return

        height_price = 0

        if height == "80_alum":
            height_price = 500
        elif height == "100_alum":
            height_price = 700

        if range_s == '0':
            range_price = 0
        elif range_s == 'Мурино' or range_s == 'Девяткино' or range_s == 'Новоселье' or range_s == 'Кудрово':
            range_price = 500
        elif range_s == 'Пушкин' or range_s == 'Павловск' or range_s == 'Петергоф' or range_s == 'Красное село':
            range_price = 800
        else:
            range_s = math.ceil(int(range_s) / 10) * 10
            c = range_s // 10
            range_price = c * 500


        freight_elevator_price = "0"

        if freight_elevator == "Нет":
            freight_elevator_price = 1500

        price = (int(count) * height_price + int(freight_elevator_price) + range_price)
        if consumables == 'Да':
            consumables_metres = math.ceil(int(count) / 10)
            price += 1000 * consumables_metres

        if price < 5500:
            price = 5500

        price = price

        if height == '80_alum':
            height = '80'
        elif height == '100_alum':
            height = '100'

        height_google = f"Высота: {height}"
        zapil_quantity_v_google = f"Запил выворотка: {0}"
        zapil_quantity_k_google = f"Запил конверт: {0}"
        zapil_quantity_m_google = f"Запил для дверей скрытого монтажа: {0}"
        sealing_uniq_google = f"Отдельная герметизация соединения: {0}"
        sealing_up_google = f"Герметизиция по верху: {0}"
        mdf_color_g = f"Цвет: {mdf_color}"
        material_sign = 'Панели'

        await insert_new(count_google, height_google, material_google, address_google, phone_google, date,
                         zapil_quantity_v_google, zapil_quantity_k_google,
                         zapil_quantity_m_google, freight_elevator_google, sealing_uniq_google, sealing_up_google,
                         user_id_google, comment_google, name_google, floor_type_google, recognize_us_google,
                         consumables_g, mdf_color_g, material_sign)

        message_text = (f'Отлично, <b>{name}</b>, вы записаны на <b>{date}</b>\n\n'
                        f"<b>Цена</b>: {price} рублей\n"
                        f"<b>Дата</b>: {date}\n"
                        f"<b>Кол-во метров</b>: {count}\n"
                        f"<b>Тип</b>: {floor_type}\n"
                        f"<b>Высота</b>: {height}\n"
                        f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                        f"<b>Расходные материалы</b>: {consumables}\n"
                        f"<b>Материал:</b> {material}\n"
                        f"<b>Адрес</b>: <code>{address}</code>\n"
                        f"<b>Номер</b>: <code>{phone}</code>\n"
                        f"<b>Откуда о нас узнали</b>: {recognize_us}\n"
                        f"<b>Комментарий</b>: <b>{comment}</b>\n\n"
                        f'*ждите подтверждение вашей записи\n'
                        f'*расходные материалы в виде клея в стоимость монтажа не входят\n'
                        f'*в минимальный заказ входит монтаж плинтуса со всеми углами\n\n'
                        f'После получения заказа мы с Вами связемся для подтвержения!'
                        f' Либо можете уточнить у нас по номеру телефона +79045150339\n')
        if price == 5500:
            message_text = f"{message_text} *минимальная сумма заказа от 5500 рублей"

        await message.answer(message_text)

        await bot.send_message(chat_id=os.getenv("CHAT_ID"), text="<b>Новая заявка</b>\n\n"
                                                                  f"<b>Имя</b>: {name}\n"
                                                                  f"<b>Цена</b>: {price} рублей\n"
                                                                  f"<b>Дата</b>: {date}\n"
                                                                  f"<b>Кол-во метров</b>: {count}\n"
                                                                  f"<b>Тип</b>: {floor_type}\n"
                                                                  f"<b>Высота</b>: {height}\n"
                                                                  f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                                                                  f"<b>Расходные материалы</b>: {consumables}\n"
                                                                  f"<b>Материал:</b> {material}\n"
                                                                  f"<b>Адрес</b>: <code>{address}</code>\n"
                                                                  f"<b>Номер</b>: <code>{phone}</code>\n"
                                                                  f"<b>Откуда о нас узнали</b>: {recognize_us}\n"
                                                                  f"<b>User name</b>: <a href='https://t.me/{user_name}'>{user_name}</a>\n"
                                                                  f"<b>Комментарий</b>: <b>{comment}</b>\n")

    else:
        height = data["height"]
        zapil_quantity_v = data["zapil_quantity_v"]
        zapil_quantity_k = data["zapil_quantity_k"]
        zapil_quantity_m = data["zapil_quantity_m"]
        freight_elevator = data["freight_elevator"]
        sealing_uniq = data["sealing_uniq"]
        sealing_up = data["sealing_up"]

        try:
            mdf_color = data["mdf_color"]
        except:
            print('Нету')

        user_name = message.from_user.username

        if user_name is None:
            user_name = phone

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            await message.answer('Некорректный формат даты. Введите дату в формате ГГГГ-ММ-ДД.')
            return

        height_price = 0

        if height == "80":
            height_price = 210
        elif height == "90":
            height_price = 250
        elif height == "100":
            height_price = 300
        elif height == "110":
            height_price = 330
        elif height == "120":
            height_price = 350
        elif height == "130":
            height_price = 400
        elif height == "140":
            height_price = 450
        elif height == "150":
            height_price = 500
        elif height == "160":
            height_price = 550
        elif height == "170":
            height_price = 600
        elif height == 'shpon_260':
            height = height.split()
            height = height.split('_')[1]
        elif height == 'shpon_310':
            height_price = 310
            height = height.split('_')[1]
        elif height == 'shpon_360':
            height_price = 360
            height = height.split('_')[1]
        elif height == 'shpon_410':
            height_price = 410
            height = height.split('_')[1]
        elif height == 'shpon_460':
            height_price = 460
            height = height.split('_')[1]
        elif height == 'shpon_510':
            height_price = 510
            height = height.split('_')[1]
        elif height == 'shpon_560':
            height_price = 560
            height = height.split('_')[1]
        elif height == 'shpon_610':
            height_price = 610
            height = height.split('_')[1]
        elif height == 'shpon_660':
            height_price = 660
            height = height.split('_')[1]
        elif height == 'shpon_710':
            height_price = 710
            height = height.split('_')[1]

        if material == 'Теневые плинтуса':
            height_price = 500

        range_price = 0

        if range_s == '0':
            range_price = 0
        elif range_s == 'Мурино' or range_s == 'Девяткино' or range_s == 'Новоселье' or range_s == 'Кудрово':
            range_price = 500
        elif range_s == 'Пушкин' or range_s == 'Павловск' or range_s == 'Петергоф' or range_s == 'Красное село':
            range_price = 800
        else:
            range_s = math.ceil(int(range_s) / 10) * 10
            c = range_s // 10
            range_price = c * 500

        if (zapil_quantity_m == 'Выберу с мастером' and zapil_quantity_v == 'Выберу с мастером' and
                zapil_quantity_k == 'Выберу с мастером'):
            zapil_quantity_k = 0
            zapil_quantity_v = 0
            zapil_quantity_m = 0

        if sealing_up == 'Выберу с мастером' and sealing_uniq == "Выберу с мастером":
            sealing_up = "0"
            sealing_uniq = "0"

        k_price = int(zapil_quantity_k) * 250
        v_price = int(zapil_quantity_v) * 190
        m_price = int(zapil_quantity_m) * 250

        sealing_up_price = int(sealing_up) * 200
        sealing_uniq_price = int(sealing_uniq) * 50

        freight_elevator_price = "0"

        if freight_elevator == "Нет":
            freight_elevator_price = 1500

        price = (int(count) * height_price + int(freight_elevator_price) + range_price)

        if consumables == 'Да':
            consumables_metres = math.ceil(int(count) / 10)
            price += 1000 * consumables_metres

        if price < 5500:
            price = 5500

        price = (price + k_price + m_price + v_price + sealing_up_price + sealing_uniq_price)

        if zapil_quantity_m == 0 and zapil_quantity_v == 0 and zapil_quantity_k == 0:
            zapil_quantity_k = 'Выберу с мастером'
            zapil_quantity_v = 'Выберу с мастером'
            zapil_quantity_m = 'Выберу с мастером'

        if sealing_up == "0" and sealing_uniq == "0":
            sealing_up = 'Выберу с мастером'
            sealing_uniq = 'Выберу с мастером'

        height_google = f"Высота: {height}"
        zapil_quantity_v_google = f"Запил выворотка: {zapil_quantity_v}"
        zapil_quantity_k_google = f"Запил конверт: {zapil_quantity_k}"
        zapil_quantity_m_google = f"Запил для дверей скрытого монтажа: {zapil_quantity_m}"
        sealing_uniq_google = f"Отдельная герметизация соединения: {sealing_uniq}"
        sealing_up_google = f"Герметизиция по верху: {sealing_up}"
        mdf_color_g = f"Цвет: {mdf_color}"
        material_sign = "Плинтус"

        await insert_new(count_google, height_google, material_google, address_google, phone_google, date,
                         zapil_quantity_v_google, zapil_quantity_k_google,
                         zapil_quantity_m_google, freight_elevator_google, sealing_uniq_google, sealing_up_google,
                         user_id_google, comment_google, name_google, floor_type_google, recognize_us_google,
                         consumables_g, mdf_color_g, material_sign)

        message_text = (f'Отлично, <b>{name}</b>, вы записаны на <b>{date}</b>\n\n'
                        f"<b>Цена</b>: {price} рублей\n"
                        f"<b>Дата</b>: {date}\n"
                        f"<b>Кол-во метров</b>: {count}\n"
                        f"<b>Тип</b>: {floor_type}\n"
                        f"<b>Цвет</b>: {mdf_color}\n"
                        f"<b>Высота</b>: {height}\n"
                        f"<b>Запил выворотка</b>: {zapil_quantity_v}\n"
                        f"<b>Запил конверт</b>: {zapil_quantity_k}\n"
                        f"<b>Запил для дверей скрытого монтажа</b>:"
                        f" {zapil_quantity_m}\n"
                        f"<b>Герметизиция по верху</b>: {sealing_up}\n"
                        f"<b>Отдельная герметизация соединения</b>: "
                        f"{sealing_uniq}\n"
                        f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                        f"<b>Расходные материалы</b>: {consumables}\n"
                        f"<b>Материал:</b> {material}\n"
                        f"<b>Адрес</b>: <code>{address}</code>\n"
                        f"<b>Номер</b>: <code>{phone}</code>\n"
                        f"<b>Откуда о нас узнали</b>: {recognize_us}\n"
                        f"<b>Комментарий</b>: <b>{comment}</b>\n\n"
                        f'*ждите подтверждение вашей записи\n'
                        f'*расходные материалы в виде клея в стоимость монтажа не входят\n'
                        f'*в минимальный заказ входит монтаж плинтуса со всеми углами\n\n'
                        f'После получения заказа мы с Вами связемся для подтвержения!'
                        f' Либо можете уточнить у нас по номеру телефона +79045150339\n')
        if price == 5500:
            message_text = f"{message_text} *минимальная сумма заказа от 5500 рублей"

        await message.answer(message_text)

        await bot.send_message(chat_id=os.getenv("CHAT_ID"), text="<b>Новая заявка</b>\n\n"
                                                                  f"<b>Имя</b>: {name}\n"
                                                                  f"<b>Цена</b>: {price} рублей\n"
                                                                  f"<b>Дата</b>: {date}\n"
                                                                  f"<b>Кол-во метров</b>: {count}\n"
                                                                  f"<b>Тип</b>: {floor_type}\n"
                                                                  f"<b>Цвет</b>: {mdf_color}\n"
                                                                  f"<b>Высота</b>: {height}\n"
                                                                  f"<b>Запил выворотка</b>: {zapil_quantity_v}\n"
                                                                  f"<b>Запил конверт</b>: {zapil_quantity_k}\n"
                                                                  f"<b>Запил для дверей скрытого монтажа</b>:"
                                                                  f" {zapil_quantity_m}\n"
                                                                  f"<b>Герметизиция по верху</b>: {sealing_up}\n"
                                                                  f"<b>Отдельная герметизация соединения</b>: "
                                                                  f"{sealing_uniq}\n"
                                                                  f"<b>Есть ли грузовой лифт</b>: {freight_elevator}\n"
                                                                  f"<b>Расходные материалы</b>: {consumables}\n"
                                                                  f"<b>Материал:</b> {material}\n"
                                                                  f"<b>Адрес</b>: <code>{address}</code>\n"
                                                                  f"<b>Номер</b>: <code>{phone}</code>\n"
                                                                  f"<b>Откуда о нас узнали</b>: {recognize_us}\n"
                                                                  f"<b>User name</b>: <a href='https://t.me/{user_name}'>{user_name}</a>\n"
                                                                  f"<b>Комментарий</b>: <b>{comment}</b>\n")
