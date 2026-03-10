import discord
import requests
import asyncio

TOKEN = 'YOUR-DISCORD-TOKEN'
GUILD_ID = YOUR-GUILD-DISCORD-ID

SYMBOL = 'SOLUSDT'
NAME = 'SOL'

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def obtener_precio(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')
    guild = client.get_guild(GUILD_ID)

    precio_anterior = await obtener_precio(SYMBOL)
    flecha = ''  # flecha retenida

    while True:
        try:
            precio_actual = await obtener_precio(SYMBOL)

            if precio_actual > precio_anterior:
                flecha = '↗'
            elif precio_actual < precio_anterior:
                flecha = '↘'
            # Si no cambia, mantenemos la flecha anterior

            nuevo_nick = f"{NAME} {flecha} ${precio_actual:,.2f}"

            bot_miembro = guild.get_member(client.user.id)
            if bot_miembro:
                await bot_miembro.edit(nick=nuevo_nick)
                print(f'🟢 Nick actualizado a: {nuevo_nick}')
            else:
                print("❌ No se encontró al bot en el servidor.")

            precio_anterior = precio_actual

        except Exception as e:
            print(f'⚠️ Error: {e}')

        await asyncio.sleep(60)

client.run(TOKEN)
