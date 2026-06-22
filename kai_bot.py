import discord
from discord.ext import commands
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv
import asyncio

# ================= CONFIGURACIÓN =================
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Verificar token
if TOKEN is None:
    print("❌ ERROR: No se encontró DISCORD_TOKEN en variables de entorno")
    exit(1)

# IDs de tus canales (actualiza si es necesario)
CANALES = {
    'logros': 1415875718327570545,
    'ideas': 1417610844497248498,
    'pecadores': 1418793821168209991
}

ZONA_HORARIA = pytz.timezone('America/Mexico_City')

# ================= LISTA DE PUBLICACIONES =================
PUBLICACIONES = [    
     
     



      
       
]

# ================= FUNCIONES AUXILIARES =================
def obtener_publicaciones_pendientes(todas_publicaciones):
    """Filtra las publicaciones que ya deberían haberse publicado"""
    pendientes = []
    ahora = datetime.now(ZONA_HORARIA)
    
    for pub in todas_publicaciones:
        # Convertir fecha string a datetime
        fecha_pub = datetime.strptime(pub['fecha'], '%d/%m/%Y %H:%M')
        fecha_pub = ZONA_HORARIA.localize(fecha_pub)
        
        # Si la fecha ya pasó, es pendiente
        if fecha_pub <= ahora:
            pendientes.append(pub)
    
    # Ordenar por fecha (más antigua primero)
    pendientes.sort(key=lambda x: datetime.strptime(x['fecha'], '%d/%m/%Y %H:%M'))
    
    return pendientes

# ================= BOT PRINCIPAL =================
async def main():
    print('=' * 50)
    print('🚀 Kai se está despertando...')
    print('=' * 50)
    
    # Obtener TODAS las publicaciones que ya deberían haberse hecho
    pendientes = obtener_publicaciones_pendientes(PUBLICACIONES)
    print(f'📅 Publicaciones pendientes hasta ahora: {len(pendientes)}')
    
    if not pendientes:
        print('✅ No hay publicaciones pendientes para este momento.')
        return
    
    # Mostrar qué va a publicar
    for i, pub in enumerate(pendientes[:3]):  # Mostrar solo las primeras 3
        print(f'  {i+1}. {pub["fecha"]} → {pub["canal"]}')
    if len(pendientes) > 3:
        print(f'  ... y {len(pendientes)-3} más')
    
    # Configurar el bot
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='!', intents=intents)
    
    @bot.event
    async def on_ready():
        print(f'✅ Conectado como {bot.user}')
        print('📤 Enviando publicaciones pendientes...')
        
        for pub in pendientes:
            try:
                canal_id = CANALES[pub['canal']]
                canal = bot.get_channel(canal_id)
                
                if canal:
                    print(f'  • Enviando a {pub["canal"]} ({pub["fecha"]})...')
                    
                    embed = discord.Embed(
                        description=pub['mensaje'],
                        color=discord.Color.purple()
                    )
                    embed.set_footer(text="🧠 Kai • Compañero creativo • Publicación automática")
                    
                    await canal.send(embed=embed)
                    print(f'  ✅ Enviada: {pub["fecha"]} en {pub["canal"]}')
                    
                    # Pequeña pausa para no saturar
                    await asyncio.sleep(1)
                    
                else:
                    print(f'  ❌ Canal no encontrado: {pub["canal"]}')
                    
            except Exception as e:
                print(f'  ⚠️ Error al publicar: {e}')
        
        # Cerrar el bot
        print('🛑 Cerrando conexión...')
        await bot.close()
    
    # Iniciar el bot
    print('🔗 Conectando a Discord...')
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f'❌ Error al conectar: {e}')

# ================= EJECUCIÓN =================
if __name__ == "__main__":
    asyncio.run(main())
    print('🎩 Kai ha terminado su trabajo por hoy.')
