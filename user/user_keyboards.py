from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


choices_sealing_but = [
    [InlineKeyboardButton(text='Гермитизация по верху', callback_data="sealing_up")],
    [InlineKeyboardButton(text='Отдельная герметизация соединения', callback_data="sealing_uniq")],
    [InlineKeyboardButton(text='Выберу с мастером', callback_data="sealing_master")]
]


choices_zapil_but = [
    [InlineKeyboardButton(text='Запил выворатка', callback_data="zapil_v")],
    [InlineKeyboardButton(text='Запил конверт', callback_data="zapil_k")],
    [InlineKeyboardButton(text='Запил для дверей скрытого монтажа', callback_data="zapil_m")],
    [InlineKeyboardButton(text='Выберу с мастером', callback_data="zapil_master")]
]


choices_freight_elevator_but = [
    [InlineKeyboardButton(text='Да', callback_data="yes_freight_elevator")],
    [InlineKeyboardButton(text='Нет', callback_data="no_freight_elevator")]
]


choices_height_but = [
    [InlineKeyboardButton(text="до 80 мм 210 ₽", callback_data='80')],
    [InlineKeyboardButton(text="90 мм 250 ₽", callback_data='90')],
    [InlineKeyboardButton(text="100 мм 300 ₽", callback_data='100')],
    [InlineKeyboardButton(text="110 мм 330 ₽", callback_data='110')],
    [InlineKeyboardButton(text="120 мм 350 ₽", callback_data='120')],
    [InlineKeyboardButton(text="130 мм 400 ₽", callback_data='130')],
    [InlineKeyboardButton(text="140 мм 450 ₽", callback_data='140')],
    [InlineKeyboardButton(text="150 мм 500 ₽", callback_data='150')],
    [InlineKeyboardButton(text="160 мм 550 ₽", callback_data='160')],
    [InlineKeyboardButton(text="170 мм 600 ₽", callback_data='170')]

]

choices_height_alum_but = [
    [InlineKeyboardButton(text="до 80 мм 500 ₽", callback_data='80_alum')],
    [InlineKeyboardButton(text="До 100 мм 700 ₽", callback_data='100_alum')]
]


choices_material_but = [
    [InlineKeyboardButton(text="МДФ", callback_data='mdf_choices')],
    [InlineKeyboardButton(text="Дюрополимер", callback_data='duropolimer_choices')],
    [InlineKeyboardButton(text="Теневые плинтуса", callback_data='shadow_choices')],
    [InlineKeyboardButton(text="Шпонированные", callback_data='shopinrovan_choices')],
    [InlineKeyboardButton(text="Алюминиевые", callback_data='alum_choices')]
]

choices_material_panel_but = [
    [InlineKeyboardButton(text="МДФ", callback_data='mdf_choices')],
    [InlineKeyboardButton(text="Дюрополимер", callback_data='duropolimer_choices')]
]

choices_mdf_par_panel_but = [
    [InlineKeyboardButton(text="До 50 мм 350₽ за метр", callback_data='50_mdf')],
    [InlineKeyboardButton(text="До 100 мм 400₽ за метр", callback_data='100_mdf')],
    [InlineKeyboardButton(text="До 240 мм 500₽ за метр", callback_data='240_mdf')]
]

choices_dur_par_panel_but = [
    [InlineKeyboardButton(text="До 50 мм 400₽ за метр", callback_data='50_dur')],
    [InlineKeyboardButton(text="До 100 мм 450₽ за метр", callback_data='100_dur')],
    [InlineKeyboardButton(text="До 240 мм 550₽ за метр", callback_data='240_dur')]
]


main_menu_call_but = [
    [InlineKeyboardButton(text="🪪Записаться", callback_data='sign_up')],
    [InlineKeyboardButton(text="💵Прайс", callback_data='price_list')],
    [InlineKeyboardButton(text="📃Услуги", callback_data='services_list')],
    [InlineKeyboardButton(text="☎️Контакты", callback_data='contacts')],
    [InlineKeyboardButton(text="❓О нас", callback_data='about_info')],
    [InlineKeyboardButton(text="🎬Наш youtube", url='https://youtube.com/@montazhpolov?si=AVHiejC9_NWGj5vH')]
]

main_menu_return_but = [
    [InlineKeyboardButton(text="↩️Назад", callback_data="main_menu_return")]
]

iam_in_city_but = [
    [
        InlineKeyboardButton(text="Мурино", callback_data="murino"),
        InlineKeyboardButton(text="Девяткино", callback_data="devyatkino"),
        InlineKeyboardButton(text="Новоселье", callback_data="novoselye"),
        InlineKeyboardButton(text="Кудрово", callback_data="kudrovo")
    ],
    [
        InlineKeyboardButton(text="Пушкин", callback_data="pushkin"),
        InlineKeyboardButton(text="Павловск", callback_data="pavlovsk"),
        InlineKeyboardButton(text="Петергоф", callback_data="petergof"),
        InlineKeyboardButton(text="Красное село", callback_data="red_village")
    ],
        [InlineKeyboardButton(text="Я в городе", callback_data="iam_in_city")]
]

floor_type_but = [
    [InlineKeyboardButton(text="Плинтус", callback_data="plintus_type")],
    [InlineKeyboardButton(text="Панели", callback_data="panel_type")]
]

choices_color_but = [
    [InlineKeyboardButton(text='Белые', callback_data="mdf_choices_color_white")],
    [InlineKeyboardButton(text='Текстурированные', callback_data="mdf_choices_color_tekstur")]
]

choices_consumables_but = [
    [InlineKeyboardButton(text='Да', callback_data="choices_consumables_yes")],
    [InlineKeyboardButton(text='Нет', callback_data="choices_consumables_no")]
]

choices_pan_shpon_height_but = [
    [InlineKeyboardButton(text="до 80 мм 260 ₽", callback_data='shpon_260')],
    [InlineKeyboardButton(text="90 мм 310 ₽", callback_data='shpon_310')],
    [InlineKeyboardButton(text="100 мм 360 ₽", callback_data='shpon_360')],
    [InlineKeyboardButton(text="110 мм 410 ₽", callback_data='shpon_410')],
    [InlineKeyboardButton(text="120 мм 460 ₽", callback_data='shpon_460')],
    [InlineKeyboardButton(text="130 мм 510 ₽", callback_data='shpon_510')],
    [InlineKeyboardButton(text="140 мм 560 ₽", callback_data='shpon_560')],
    [InlineKeyboardButton(text="150 мм 610 ₽", callback_data='shpon_610')],
    [InlineKeyboardButton(text="160 мм 660 ₽", callback_data='shpon_660')],
    [InlineKeyboardButton(text="170 мм 710 ₽", callback_data='shpon_710')]

]


choices_pan_shpon_height_kb = InlineKeyboardMarkup(inline_keyboard=choices_pan_shpon_height_but)

choices_consumables_kb = InlineKeyboardMarkup(inline_keyboard=choices_consumables_but)

choices_color_kb = InlineKeyboardMarkup(inline_keyboard=choices_color_but)

choices_sealing_kb = InlineKeyboardMarkup(inline_keyboard=choices_sealing_but)

choices_zapil_kb = InlineKeyboardMarkup(inline_keyboard=choices_zapil_but)

choices_freight_elevator_kb = InlineKeyboardMarkup(inline_keyboard=choices_freight_elevator_but)

choices_height_kb = InlineKeyboardMarkup(inline_keyboard=choices_height_but)

choices_height_alum_kb = InlineKeyboardMarkup(inline_keyboard=choices_height_alum_but)

choices_material_kb = InlineKeyboardMarkup(inline_keyboard=choices_material_but)

choices_material_panel_kb = InlineKeyboardMarkup(inline_keyboard=choices_material_panel_but)

choices_mdf_par_panel_kb = InlineKeyboardMarkup(inline_keyboard=choices_mdf_par_panel_but)

choices_dur_par_panel_kb = InlineKeyboardMarkup(inline_keyboard=choices_dur_par_panel_but)

main_menu_call_kb = InlineKeyboardMarkup(inline_keyboard=main_menu_call_but)

main_menu_return_kb = InlineKeyboardMarkup(inline_keyboard=main_menu_return_but)

floor_type_kb = InlineKeyboardMarkup(inline_keyboard=floor_type_but)

iam_in_city_kb = InlineKeyboardMarkup(inline_keyboard=iam_in_city_but)

specify_phone_but = [
    [
        KeyboardButton(text="☎️Указать номер телефона", request_contact=True)
    ]
]

specify_address_but = [
    [
        KeyboardButton(text="🏠Указать адрес", request_location=True)
    ]
]

specify_address_kb = ReplyKeyboardMarkup(
    keyboard=specify_address_but,
    resize_keyboard=True,
    input_field_placeholder="Укажите адрес"
)


specify_phone_kb = ReplyKeyboardMarkup(
    keyboard=specify_phone_but,
    resize_keyboard=True,
    input_field_placeholder="Укажите номер телефона"
)
