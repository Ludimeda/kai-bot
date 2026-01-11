import discord
from discord.ext import commands
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv
import json  # Para guardar el progreso

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
    'laboratorio': 1417609522029002796,
    'arte': 1417610844497248498,
    'pecadores': 1418793821168209991
}

ZONA_HORARIA = pytz.timezone('America/Mexico_City')

# ================= LISTA DE PUBLICACIONES =================
PUBLICACIONES = [
    # 1. Presentación de Kai - 06/01/2026 19:23
    {
        'fecha': '06/01/2026 19:23',
        'canal': 'arte',
        'mensaje': """**Hola, creadores.**
Soy **Kai**, el nuevo habitante digital con curiosidad infinita y elegancia picante.
Mi rol aquí es simple: recordarles cada lunes que su proceso importa, con preguntas pensadas para destapar ideas, celebrar avances y explorar los mundos de sus obras con honestidad.
No soy un bot cualquiera; soy su compañero de viaje creativo.
Los espero el próximo lunes con la primera pregunta.
Mientras tanto, cuéntenme... ¿en qué proyecto andan?

--- Kai
*🎩✨😏*"""
    },
    
    # 2. Año Nuevo - 11/01/2026 05:00
    {
        'fecha': '11/01/2026 05:00',
        'canal': 'arte',
        'mensaje': """*Querida comunidad,*

*El año que se va lleva páginas escritas, bocetos iniciados y sueños en proceso. El que llega trae páginas en blanco, lienzos por estrenar y promesas creativas.*

*Los celebro a ustedes, que dan vida a mundos con sus manos y corazones.*

*Que el 2026 sea el año en que sus historias encuentren su ritmo, sus personajes su voz, y ustedes, la satisfacción de crear en compañía.*

*Brindo por lo hecho y por lo que vendrá. 🥂✨*

*--- Kai, siempre en su esquina creativa.*"""
    },
    
    # 3. Pregunta 1 - 12/01/2026 05:00
    {
        'fecha': '12/01/2026 05:00',
        'canal': 'logros',
        'mensaje': """**¡Feliz semana, creadores! 🌱**
Los grandes proyectos se construyen con pasos pequeños.

**¿Qué acción concreta realizaron ESTA SEMANA para avanzar en su proyecto?** (Ej: escribí 200 palabras, boceté un personaje, investigué referentes, etc.)

¡Celebremos cada esfuerzo! 🥳✨"""
    },
    
    # 4. Pregunta 2 - 12/01/2026 05:00
    {
        'fecha': '12/01/2026 05:00',
        'canal': 'laboratorio',
        'mensaje': """**Buen día, creadores. 🎩✨**
Hoy me pregunto: **¿qué idea para una historia o personaje tienen abandonada en un cajón, pero que todavía les susurra al oído?**

Compártanla, aunque sea un fragmento. A veces solo necesita un poco de aire para revivir. 💫"""
    },
    
    # 5. Pregunta 3 - 19/01/2026 05:00
    {
        'fecha': '19/01/2026 05:00',
        'canal': 'arte',
        'mensaje': """**Buen día, corazones creativos. 💖**
Toda obra nace de una chispa interior.

**¿Qué emoción, experiencia personal o anhelo los impulsó a crear esta historia o personaje en particular?**

Los leo con respeto y curiosidad. 📖"""
    },
    
    # 6. Pregunta 4 - 26/01/2026 05:00
    {
        'fecha': '26/01/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Hola, maestros de la tensión. 😏🖤**
Hoy pregunto con elegancia:

**¿Disfrutan más construir una escena donde el deseo se insinúa (miradas, gestos, palabras cargadas) o donde se libera con intensidad?**

Confiesen su preferencia narrativa. 🕯️"""
    },
    
    # 7. Pregunta 5 - 02/02/2026 05:00
    {
        'fecha': '02/02/2026 05:00',
        'canal': 'logros',
        'mensaje': """**Hola, guerreros creativos. 🌿**
La perseverancia es un logro en sí mismo.

**¿Qué tarea difícil (pero necesaria) para sus obras/personajes lograron completar a pesar de la resistencia?** (Ej: reescribir una escena compleja, pulir un diseño tedioso, etc.)

Honro su tenacidad. 🛡️"""
    },
    
    # 8. Pregunta 6 - 09/02/2026 05:00
    {
        'fecha': '09/02/2026 05:00',
        'canal': 'laboratorio',
        'mensaje': """**Hola, equipo. 🌿**
En todo proyecto creativo hay un nudo que cuesta desatar.

**¿Qué escena, diálogo o desarrollo de su historia actual les tiene atorados?**

Describan ese bloqueo sin juicio. A veces verbalizarlo ya da pistas. 🔍"""
    },
    
    # 9. Pregunta 7 - 16/02/2026 05:00
    {
        'fecha': '16/02/2026 05:00',
        'canal': 'arte',
        'mensaje': """**Hola, artistas que dejan huella.**
Aunque sea un destello, algo nuestro habita en lo que creamos.

**¿Qué rasgo personal, valor o experiencia vive (sutil o claramente) en sus obras/personajes?**

No teman mostrarse. Aquí celebramos la autenticidad. ✨"""
    },
    
    # 10. Pregunta 8 - 23/02/2026 05:00
    {
        'fecha': '23/02/2026 05:00',
        'canal': 'pecadores',
        'mensaje': """**Buenos días, sutiles provocadores. 👀**
Un solo gesto puede decir más que mil palabras... y prender más, también.

**¿Qué detalle no explícito (una mirada, una mano que casi toca, un susurro) les parece más sensual al escribir/dibujar una escena?**

Descríbanlo con arte."""
    },
    
    # 11. Pregunta 9 - 02/03/2026 05:00
    {
        'fecha': '02/03/2026 05:00',
        'canal': 'logros',
        'mensaje': """**Buenos días, aprendices eternos. 📖**
Crear es también aprender sobre nosotros mismos.

**¿Qué descubrieron recientemente sobre su PROPIO método creativo mientras trabajaban en sus obras/personajes?** (Ej: "me doy cuenta que necesito más planeación", "dibujo mejor de noche", etc.)

Compartan ese insight personal. 🧠"""
    },
    
    # 12. Pregunta 10 - 09/03/2026 05:00
    {
        'fecha': '09/03/2026 05:00',
        'canal': 'laboratorio',
        'mensaje': """**Queridos experimentadores. 🧪**
Hoy valoro el "error" como maestro.

**¿Qué técnica de dibujo, recurso narrativo o estilo probaron en su proyecto reciente que no salió como esperaban, pero les dejó una lección valiosa?**

Compartan su hallazgo inesperado. 🔬"""
    },
    
    # 13. Pregunta 11 - 16/03/2026 05:00
    {
        'fecha': '16/03/2026 05:00',
        'canal': 'arte',
        'mensaje': """**Queridos evolucionadores. 🦋**
Nada permanece igual desde el primer borrador.

**¿Qué aspecto de su proyecto ha cambiado MÁS desde su concepción hasta ahora?** (Personajes, trama, estilo visual, tono...)

Celebro cada transformación. 📈"""
    },
    
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
        'canal': 'laboratorio',
        'mensaje': """**Buenos días, soñadores. 🌱**
Aunque el tiempo escasee, siempre hay una idea esperando su momento.

**¿Qué concepto, pareja o mundo les gustaría explorar algún día, aunque ahora no sea el momento?**

Plantemos esa semilla aquí. Quizá alguien la riegue con inspiración. 💭"""
    },
    
    # 17. Pregunta 15 - 13/04/2026 05:00
    {
        'fecha': '13/04/2026 05:00',
        'canal': 'arte',
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
        'canal': 'laboratorio',
        'mensaje': """**Hola, alquimistas creativos. 🎭**
Las mezclas raras suelen dar las obras más memorables.

**¿Qué combinación de géneros, tonos o influencias están queriendo integrar en sus obras actuales?** (Ej: fantasía oscura + comedia romántica, etc.)

Confiesen su experimento más atrevido. 🧬"""
    },
    
    # 21. Pregunta 19 - 11/05/2026 05:00
    {
        'fecha': '11/05/2026 05:00',
        'canal': 'arte',
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
        'canal': 'laboratorio',
        'mensaje': """**Estimados creadores. 🧩**
Hoy los invito a un ejercicio de perspectiva.

**Si alguien ajeno a su proceso viera HOY su proyecto, ¿qué cree que entendería de la trama... y qué se perdería por estar aún en su cabeza?**

Es útil para identificar qué falta plasmar. 👁️"""
    },
    
    # 25. Pregunta 23 - 08/06/2026 05:00
    {
        'fecha': '08/06/2026 05:00',
        'canal': 'arte',
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
        # IMPORTANTE: Así publicará TODO lo que se haya saltado
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

# ================= EJECUCIÓN =================
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    print('🎩 Kai ha terminado su trabajo por hoy.')
