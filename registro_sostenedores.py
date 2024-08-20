# -*- coding: utf-8 -*-
"""registro-sostenedores.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/smassas/357119c79db3062048c7df98e4dae4ed/registro-sostenedores.ipynb

# Registro de sostenedores

Descargar registro de sostenedores [aquí](https://www.supereduc.cl/wp-content/uploads/2024/07/20240711-Correos-de-Sostenedores-Actualizados-hasta-JULIO-2024.pdf)

1. Instalar librerías de Python
"""

!pip install requests
!pip install PyPDF2

"""2. Importar librerías"""

import pandas as pd
import PyPDF2
from google.colab import drive
import re

"""3. Agregar la ruta del archivo

`NOTA`: Para agregar la ruta del archivo, primero deberá subir el archivo descargado a Google Colab. Una vez realizado el paso anterior, podrá copiar la ruta directamente en el archivo, pegando la dirección en las comillas.


<img src = "https://miro.medium.com/v2/resize:fit:1400/1*eLs1D3BI4_HLAabN5WUTPg.png" width="500" height="300">


"""

pdf_path = '/20240711-Correos-de-Sostenedores-Actualizados-hasta-JULIO-2024.pdf'

"""4. Correr función para extraer texto de PDF"""

def extraer_texto_pdf(pdf_path):
    texto = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pags = len(reader.pages)
        for pag_num in range(num_pags):
            pag = reader.pages[pag_num]
            texto += pag.extract_text()
    return texto

pdf_text = extraer_texto_pdf(pdf_path)

"""5. Inspeccionar el set de datos"""

lines = pdf_text.split('\n')
df = pd.DataFrame(lines, columns=['columna'])
df.head(5)

"""6. Extraer solo registros de correos electrónicos"""

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def encontrar_emails(text):
    emails = re.findall(email_regex, text)
    return emails

df['emails'] = df['columna'].apply(encontrar_emails)

df = df[df['emails'].apply(lambda x: len(x) > 0)]

print(df.head())

print("Del registro de sostenedores Supereduc, se han extraido " + str(len(df['emails'])) + " correos.")

df["emails"].head(30)

"""7. Guardar listado de correos en XLSX

`NOTA: ` El archivo quedará almacenado en el repositorio de Google Colab, pudiendo ser descargado directamente.
"""

df = pd.DataFrame(df)
df['emails'] = df['emails'].astype(str)
df_filtrado = df[~df['emails'].str.contains(r'jardin', case=False)]
df_filtrado = df_filtrado[~df_filtrado['emails'].str.contains(r'escuela', case=False)]
listado_correos = df_filtrado['emails']
listado_correos.to_excel("listado_correos.xlsx")

"""8. Enviar correo electrónico mediante loop"""

import smtplib
from email.mime.text import MIMEText

subject = "testing"
body = "testing"
sender = "ingresa_correo"
recipients = ["ingresa_correo_contacto"]
password = ""

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Mensaje enviado!")


send_email(subject, body, sender, recipients, password)