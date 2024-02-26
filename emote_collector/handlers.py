from aiogram.types import Message


from emote_collector import dp 

@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)