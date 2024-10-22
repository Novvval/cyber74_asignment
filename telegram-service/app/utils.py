from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start the bot'),
        BotCommand(command='help', description='Show help message'),
        BotCommand(command='products', description='Show tracked products'),
    ]
    await bot.set_my_commands(commands)


def breakup_message(text: str, max_length: int = 4096) -> list[str]:
    chunks = []
    current_chunk = ''
    for line in text.splitlines():
        if len(current_chunk) + len(line) < max_length:
            current_chunk += line + '\n'
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks
