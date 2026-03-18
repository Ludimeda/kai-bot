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
       
      
      # 14. Pregunta 12 - 23/03/2026 05:00
    {
        'fecha': '23/03/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Queridos exploradores conscientes. 🖤**
La sensualidad tiene fronteras personales, y todas son válidas.

**¿Hasta qué punto de explicitud se sienten cómodos llevando una escena íntima en sus obras?** (Ej: solo insinuación, sensualidad tácita, cierto grado de desnudez emocional/metafórica, etc.)

Respeto absoluto a su zona de confort. 🛡️"""
    },
    
    # 15. Pregunta 13 - 30/03/2026 05:00
    {
        'fecha': '30/03/2026 05:00',
        'canal': 'logros',
        'mensaje': """**Hola, equipo. ✨**
Las victorias más importantes a veces son las que nadie ve.

**Compartan un logro interno relacionado con sus obras/personajes que no es evidente para el público.** (Ej: vencer la autocrítica, definir el tono emocional, tomar una decisión clave, etc.)

Los leo con admiración. 🗝️"""
    },
    
    # 16. Pregunta 14 - 06/04/2026 05:00
    {
        'fecha': '06/04/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Buenos días, soñadores. 🌱**
Aunque el tiempo escasee, siempre hay una idea esperando su momento.

**¿Qué concepto, pareja o mundo les gustaría explorar algún día, aunque ahora no sea el momento?**

Plantemos esa semilla aquí. Quizá alguien la riegue con inspiración. 💭"""
    },
    
    # 17. Pregunta 15 - 13/04/2026 05:00
    {
        'fecha': '13/04/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Hola, cómplices. 😏🤫**
Hoy toca sinceridad creativa sin vergüenza.

**¿Qué cliché, tropo o dinámica aman secretamente, aunque se diga que está "gastado"?**

Este es un espacio libre de juicios. Confiesen. 💘"""
    },
    
    # 18. Pregunta 16 - 20/04/2026 05:00
    {
        'fecha': '20/04/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Hola, arquitectos del ambiente. 🌫️**
El clima de una escena puede multiplicar su carga emocional.

**¿Qué atmósfera prefieren para momentos de tensión romántica/erótica en sus obras: íntima y cercana, oscura y peligrosa, suave y nostálgica, u otra?**

Definan su vibra favorita. 🕯️"""
    },
    
    # 19. Pregunta 17 - 27/04/2026 05:00
    {
        'fecha': '27/04/2026 05:00',
        'canal': 'logros',
        'mensaje': """**Queridos cuidadores de su llama. 🕯️**
Sin bienestar, no hay creatividad sostenible.

**¿Qué acción de autocuidado aplicaron ESTA SEMANA para proteger su energía creativa mientras trabajan en sus proyectos?** (Ej: pausas activas, límites de horario, consumo de inspiración, etc.)

Cuiden al artista que hay en ustedes. 🌿"""
    },
    
    # 20. Pregunta 18 - 04/05/2026 05:00
    {
        'fecha': '04/05/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Hola, alquimistas creativos. 🎭**
Las mezclas raras suelen dar las obras más memorables.

**¿Qué combinación de géneros, tonos o influencias están queriendo integrar en sus obras actuales?** (Ej: fantasía oscura + comedia romántica, etc.)

Confiesen su experimento más atrevido. 🧬"""
    },
    
    # 21. Pregunta 19 - 11/05/2026 05:00
    {
        'fecha': '11/05/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Estimados tejedores de emociones. 🧠**
Más allá de la trama, hay una vibra que queremos transmitir.

**¿Qué sensación o reflexión les gustaría que quedara flotando en el lector/espectador de sus obras, incluso si no puede expresarla con palabras?**

Hablen desde la intención profunda. 💫"""
    },
    
    # 22. Pregunta 20 - 18/05/2026 05:00
    {
        'fecha': '18/05/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Estimados jugadores con el deseo. 🎭**
La narrativa BL juega con distintas formas de anhelo.

**¿Qué les interesa más explorar actualmente: el deseo correspondido y realizado, o el deseo contenido, prohibido o no correspondido?**

Confiesen su inclinación dramática. 🔗"""
    },
    
    # 23. Pregunta 21 - 25/05/2026 05:00
    {
        'fecha': '25/05/2026 05:00',
        'canal': 'logros',
        'mensaje': """**¡Hola, soñadores en acción! 🌈**
Sin presión, solo intención.

**¿Qué meta REALISTA y amable se gustaría alcanzar en su proyecto BL durante ESTE MES Y EL MES QUE VIENE?** (Ej: terminar el capítulo 3, tener el character sheet completo, etc.)

La comparto para tenerla presente. ⭐"""
    },
    
    # 24. Pregunta 22 - 01/06/2026 05:00
    {
        'fecha': '01/06/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Estimados creadores. 🧩**
Hoy los invito a un ejercicio de perspectiva.

**Si alguien ajeno a su proceso viera HOY su proyecto, ¿qué cree que entendería de la trama... y qué se perdería por estar aún en su cabeza?**

Es útil para identificar qué falta plasmar. 👁️"""
    },
    
    # 25. Pregunta 23 - 08/06/2026 05:00
    {
        'fecha': '08/06/2026 05:00',
        'canal': 'ideas',
        'mensaje': """**Querida familia BL. 🏳️‍🌈**
Hoy pregunto por el corazón mismo de lo que hacemos.

**¿Qué los atrajo específicamente al Boys' Love como espacio creativo?** (La representación, la exploración emocional, la libertad narrativa, etc.)

Celebro su elección. 💖"""
    },
    
    # 26. Pregunta 24 - 15/06/2026 05:00
    {
        'fecha': '15/06/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Última confesión de la semana, queridos valientes. 🕯️**
A veces lo que más cuesta es también lo más magnetizante.

**¿Qué tipo de escena cargada de tensión romántica/sexual les resulta difícil escribir o dibujar, pero igual los atrae creativamente?**

Los leo sin juicios, solo con curiosidad. 🖤"""
    }
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
