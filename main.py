import os

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import openai
from bs4 import BeautifulSoup
import subprocess

# Configuración
OPENAI_API_KEY = os.environ.get("OPENAI_KEY")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "liberstudiobcn@gmail.com"
EMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")

def get_trendics():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select("div.feed-item div.details-top div.title span")
    return [title.text.strip() for title in titles]


# 2. Filtrar tendencias según intereses del usuario usando OpenAI (sustituye por Gemini si lo prefieres)
def filter_trendics(trends, user_interests):
    prompt = f"""Your goal is to create a report in English for the indicated person, focusing only on trending topics that might be of interest to them.
Also, you should provide something he could say about the topic, as if he were tweeting about it.
Filter the following trending topics for this person.
Return a UTF-8 encoded HTML file with the relevant topics and a brief explanation of why they are relevant to their interests.
The HTML structure should be: (Do not add comments or unnecessary tags, just the plain HTML)
<meta charset="UTF-8">
<h1>Relevant Trending Topics</h1>
<p>These are the trending topics relevant to the person.</p>
<h2>Relevant Topic (#TopicHashTag if applicable)</h2>
<p>Reason for relevance.</p>
<pre>Example tweet of the person talking about the topic.</pre>
<h3>YouTube Video example: [Aquí un título nuevo de vídeo parecido igual de tendencioso que los suyos en mayúsculas y español]</h3>
...

Trending: {', '.join(trends)}.

Person: {user_interests}.
"""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# 3. Enviar email HTML
# def send_email(html_body, subject="Trending Topics Relevantes", to_email="hola@mundo.com"):
#     # with open("trending_topics2.html", "w") as file:
#     #     file.write(html_body)

#     msg = MIMEMultipart("alternative")
#     msg["Subject"] = subject
#     msg["From"] = EMAIL_USERNAME
#     msg["To"] = to_email

#     html_part = MIMEText(html_body, "html")
#     msg.attach(html_part)

#     server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#     server.starttls()
#     server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
#     server.sendmail(EMAIL_USERNAME, EMAIL_USERNAME, msg.as_string())
#     server.quit()


def send_email(html_body, subject="Trending Topics Relevantes", to_email="hola@mundo.com"):
    message = f"""\
From: no-reply@localhost
To: {EMAIL_USERNAME}
Subject: {subject}
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8

{html_body}
"""
    try:
        subprocess.run(["/usr/sbin/sendmail", "-t", "-oi"], input=message.encode(), check=True)
    except Exception as e:
        print(f"[ERROR] No se pudo enviar el email con sendmail: {e}")

# Ejecución principal
if __name__ == "__main__":
    intereses = """
    Person: Daniel Lacalle.

   👤 Professional Profile
Birth and Education
Born in Madrid in 1967. He holds a degree in Economics and Business from the Autonomous University of Madrid, a Master's in Economic Research, a CIIA certification, and completed postgraduate studies at IESE.

Career
He began his career at Repsol, worked at Enagás, ABN AMRO, asset managers like Citadel, Ecofin, and PIMCO, and is currently Chief Economist at Tressis.

Teaching and Advisory Roles
He teaches Global Economics at IE Business School and the Instituto de Estudios Bursátiles (IEB), and has collaborated with the Mises Hispano Institute since 2017.

🧠 Ideology and Key Interests
Economic Liberalism and Austrian School
Advocate of conservative liberalism, with a focus on reducing public spending, privatizations, and less government intervention. He aligns with the Austrian School and collaborates with the Mises Institute.

Financial Markets and Commodities
His fund has worked in equities, fixed income, energy, oil, and commodities; he supports diversified portfolios, even in sectors perceived as “cheap.”

Geopolitics and Monetary System
Frequently discusses geopolitical risks—particularly in the Middle East and China—and central banks’ trend toward gold as a hedge against a potential collapse of the monetary system.

✍️ Books and Outreach
He has authored several books, including We, the Markets, Journey to Economic Freedom, The Mother of All Battles, The Big Trap, Freedom or Equality, and Grow Your Money.

His analyses appear in outlets like El Español, El Confidencial, CNBC, BBC, El Mundo, and The Wall Street Journal.

📺 YouTube Channel
On his “Daniel Lacalle” YouTube channel and the Money & Markets program, he covers topics such as financial crises, energy markets, inflation, gold, bitcoin, and global policy.

Recent videos include commentary on whether a crisis worse than 2008 is approaching, as well as analyses of gold demand, central bank decisions, and monetary trends.

🎯 Main Areas of Interest
Liberal economics and market policy

Investment and fund management

Commodities, energy, and oil

Currencies, gold, and cryptocurrencies (bitcoin)

Geopolitical and monetary risks

Economic media and education

✅ In Summary
Daniel Lacalle is a prominent conservative liberal economist with a strong background in fund management, specializing in energy and commodities. He is deeply committed to education and public communication. He has written numerous books and maintains an active presence in the media and on YouTube, where he analyzes global finance, geopolitics, economic risks, and monetary trends such as gold and bitcoin.

    More popular vídeos of Daniel Lacalle in YouTube:

13:42
Reproduciendo
¡BUKELE DESTAPA EL ENGAÑO DEL SISTEMA MONETARIO DE ESTADOS UNIDOS!
933 K visualizaciones
hace 1 año


20:46
Reproduciendo
¿VIENE UNA GRAN CRISIS EN 2025? ANÁLISIS Y CLAVES
665 K visualizaciones
hace 5 meses


6:46
Reproduciendo
RUSIA ¿AL BORDE DE LA QUIEBRA?
636 K visualizaciones
hace 3 años


15:47
Reproduciendo
CHINA CONTRAATACA Y VENDE SUS BONOS DEL TESORO DE ESTADOS UNIDOS
627 K visualizaciones
hace 2 meses


18:58
Reproduciendo
EL COLAPSO ECONÓMICO ESTÁ MÁS CERCA DE LO QUE PIENSAS
610 K visualizaciones
hace 9 meses


23:50
Reproduciendo
CÓMO ALEMANIA HUNDIÓ SU ECONOMÍA
577 K visualizaciones
hace 5 meses


12:11
Reproduciendo
ELON MUSK EXPONE EL DESPILFARRO Y LA IZQUIERDA ENLOQUECE
559 K visualizaciones
hace 4 meses


15:35
Reproduciendo
DEMÓCRATAS EN PÁNICO POR DESPILFARRO MILLONARIO QUE NO PUEDEN EXPLICAR
474 K visualizaciones
hace 4 meses


11:42
Reproduciendo
TRUMP PROHÍBE LA MONEDA DIGITAL DEL BANCO CENTRAL
436 K visualizaciones
hace 4 meses


8:49
Reproduciendo
DONALD TRUMP ARRASA Y KAMALA SE VA A SU CASA
433 K visualizaciones
hace 7 meses


17:44
Reproduciendo
EL APAGÓN EN ESPAÑA NO FUE CASUALIDAD
430 K visualizaciones
hace 1 mes


34:04
Reproduciendo
LO QUE LOS MEDIOS NO TE MOSTRARON SOBRE TRUMP Y ZELENSKI
429 K visualizaciones
hace 3 meses


19:09
Reproduciendo
EL INCENDIO DE LOS ÁNGELES: UN DESASTRE ANUNCIADO POR DECISIONES POLÍTICAS
426 K visualizaciones
hace 5 meses


5:45
Reproduciendo
Discutí con Yolanda Díaz hace 6 años... NO HA SERVIDO DE NADA
425 K visualizaciones
hace 2 años


13:51
Reproduciendo
TRUMP PIDE AL CONGRESO ELIMINAR EL IMPUESTO DE LA RENTA
420 K visualizaciones
hace 4 meses


14:46
Reproduciendo
EL FRAUDE EN USAID ES DE MILES DE MILLONES
419 K visualizaciones
hace 4 meses


13:11
Reproduciendo
USAID ES YA EL MAYOR CASO DE CORRUPCIÓN DE AMERICA
400 K visualizaciones
hace 4 meses


18:04
Reproduciendo
LA CNN DESTROZA A KAMALA HARRIS Y LA DEJA EN RIDÍCULO
392 K visualizaciones
hace 8 meses


16:02
Reproduciendo
¿ESTÁ COLAPSANDO LA ECONOMÍA CHINA?
390 K visualizaciones
hace 1 mes


19:25
Reproduciendo
TRUMP SE DISPARA EN ENCUESTAS Y KAMALA ENTRA EN PÁNICO
380 K visualizaciones
hace 8 meses
    """
    try:
        trendings = get_trendics()
        html_filtrado = filter_trendics(trendings, intereses)
        send_email(html_filtrado)
        print("✅ Email enviado con los trending topics filtrados.")
    except Exception as e:
        print(f"❌ Error: {e}")
