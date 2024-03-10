import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from utils.commands import set_commands

from user.user_handler import (start_handler, Form, start_of_recording_count, start_of_recording_height_call,
                               start_of_recording_material_call, start_of_recording_address, start_of_recording_phone,
                               start_of_recording_date, start_of_recording_sealing_call,
                               start_of_recording_zapil_quantity_k, start_of_recording_zapil_quantity_v,
                               start_of_recording_sealing_up, start_of_recording_sealing_uniq,
                               start_of_recording_freight_elevator_callback, start_of_recording_comment,
                               start_of_recording_name, start_of_recording_floor_type, start_of_recording_range,
                               start_of_recording_address_call, start_of_recording_sealing_uniq_callback,
                               mdf_choices_color_call, start_of_recording_consumables_callback, start_of_recording_recognize_us)
from user.user_callback import (about_info_callback, main_menu_return_callback, contacts_callback,
                                services_list_callback, price_list_callback, sign_up_callback)
from request.sql_request import create_table

router = Router()


async def start_bot(bot: Bot):
    load_dotenv()
    await set_commands(bot)
    await create_table()
    await bot.send_message(os.getenv("ADMIN_ID"), text='Бот запущен!')


async def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(os.getenv("TOKEN"), parse_mode="HTML")

    dp.startup.register(start_bot)

    dp.message.register(start_handler, Command('start'))

    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('50_mdf'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('100_mdf'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('240_mdf'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('50_dur'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('100_dur'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('240_dur'))

    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('80_alum'))
    dp.callback_query.register(start_of_recording_sealing_uniq_callback, F.data.startswith('100_alum'))

    dp.message.register(start_of_recording_name, Form.start_of_recording_name)
    dp.message.register(start_of_recording_floor_type, Form.start_of_recording_floor_type)
    dp.message.register(start_of_recording_count, Form.start_of_recording_count)
    dp.message.register(start_of_recording_address, Form.start_of_recording_address)
    dp.message.register(start_of_recording_phone, Form.start_of_recording_phone)
    dp.message.register(start_of_recording_date, Form.start_of_recording_date)
    dp.message.register(start_of_recording_comment, Form.start_of_recording_comment)

    dp.message.register(start_of_recording_zapil_quantity_v, Form.start_of_recording_zapil_quantity_v)
    dp.message.register(start_of_recording_zapil_quantity_k, Form.start_of_recording_zapil_quantity_k)

    dp.message.register(start_of_recording_sealing_up, Form.start_of_recording_sealing_up)
    dp.message.register(start_of_recording_sealing_uniq, Form.start_of_recording_sealing_uniq)
    dp.message.register(start_of_recording_range, Form.start_of_recording_range)

    dp.message.register(start_of_recording_recognize_us, Form.start_of_recording_recognize_us)

    dp.callback_query.register(start_of_recording_freight_elevator_callback, F.data.startswith('yes_freight_elevator'))
    dp.callback_query.register(start_of_recording_freight_elevator_callback, F.data.startswith('no_freight_elevator'))

    dp.callback_query.register(start_of_recording_consumables_callback, F.data.startswith('choices_consumables_yes'))
    dp.callback_query.register(start_of_recording_consumables_callback, F.data.startswith('choices_consumables_no'))

    dp.callback_query.register(mdf_choices_color_call, F.data.startswith('mdf_choices_color_white'))
    dp.callback_query.register(mdf_choices_color_call, F.data.startswith('mdf_choices_color_tekstur'))

    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('iam_in_city'))

    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('murino'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('devyatkino'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('novoselye'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('kudrovo'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('pushkin'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('pavlovsk'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('petergof'))
    dp.callback_query.register(start_of_recording_address_call, F.data.startswith('red_village'))

    dp.callback_query.register(start_of_recording_floor_type, F.data.startswith('panel_type'))
    dp.callback_query.register(start_of_recording_floor_type, F.data.startswith('plintus_type'))

    dp.callback_query.register(start_of_recording_zapil_quantity_v, F.data.startswith('zapil_v'))
    dp.callback_query.register(start_of_recording_zapil_quantity_v, F.data.startswith('zapil_k'))
    dp.callback_query.register(start_of_recording_zapil_quantity_v, F.data.startswith('zapil_m'))
    dp.callback_query.register(start_of_recording_zapil_quantity_v, F.data.startswith('zapil_master'))

    dp.callback_query.register(start_of_recording_sealing_call, F.data.startswith('sealing_up'))
    dp.callback_query.register(start_of_recording_sealing_call, F.data.startswith('sealing_uniq'))
    dp.callback_query.register(start_of_recording_sealing_call, F.data.startswith('sealing_master'))

    dp.callback_query.register(about_info_callback, F.data.startswith('about_info'))
    dp.callback_query.register(main_menu_return_callback, F.data.startswith('main_menu_return'))
    dp.callback_query.register(contacts_callback, F.data.startswith('contacts'))
    dp.callback_query.register(services_list_callback, F.data.startswith('services_list'))
    dp.callback_query.register(price_list_callback, F.data.startswith('price_list'))
    dp.callback_query.register(sign_up_callback, F.data.startswith('sign_up'))

    dp.callback_query.register(start_of_recording_material_call, F.data.startswith('mdf_choices'))
    dp.callback_query.register(start_of_recording_material_call, F.data.startswith('duropolimer_choices'))
    dp.callback_query.register(start_of_recording_material_call, F.data.startswith('shadow_choices'))
    dp.callback_query.register(start_of_recording_material_call, F.data.startswith('shopinrovan_choices'))
    dp.callback_query.register(start_of_recording_material_call, F.data.startswith('alum_choices'))

    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('80'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('90'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('100'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('110'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('120'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('130'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('140'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('150'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('160'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('170'))

    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_260'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_310'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_360'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_410'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_460'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_510'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_560'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_610'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_660'))
    dp.callback_query.register(start_of_recording_height_call, F.data.startswith('shpon_710'))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
