import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Utilidad: (fila, columna)
# Variables de lo que se pide
def info():
    sheet = client.open("Acciones con Google Finance").sheet1
    rendimiento = sheet.cell(8, 25).value
    ganancia = sheet.cell(8, 23).value
    if float(ganancia) < 0:
        mensaje = f"Quiena:\nPerdiendo U$S {ganancia} ({rendimiento})"
    else:
        mensaje = f"Quiena:\nGanando U$S {ganancia} ({rendimiento})"
    
    datos = sheet.col_values(29)
    datos2 = sheet.col_values(30)
    mensaje2 = mensaje + f"\n\nBecerra:\nGeneral: {datos[5]} ({datos[7]})\nAcciones:\nDólares ({datos[10]}) - Pesos ({datos2[10]})\n\nEcoValores:\nDólares ({datos[-1]}) - Pesos ({datos2[-1]})"

    return mensaje2

def plan():
    sheet2 = client.open("Acciones con Google Finance").worksheet("Plan")
    hoja = sheet2.get_all_values()
    text = ""
    for i in range(6):
        try:
            accion = hoja[6+i][1]
            precio = hoja[6+i][2]
            target = hoja[6+i][7]
            stop = hoja[6+i][8]
            even = hoja[6+i][10]
            dias = hoja[6+i][-1]
            text += f"-----{accion}-----\n💸 Precio: ${precio}\n🎯 Target: {target}\n📉 Stop Loss: {stop}\n🧨 SL Even: {even}\n🗓 Total de dias: {dias}\n\n"
        except:
            break
    return text

def performance():
    sheet3 = client.open("Acciones con Google Finance").worksheet("Performance")
    datos = sheet3.get_all_records()
    tickers = [[dic["Symbol"], dic["Day Gain"], dic["Change"], dic["Total Gain"], dic["Gain %"]] for dic in datos[1:] if dic["Total Gain"] != 0]

    text = ""
    for i in tickers:
        text += f"------| {i[0]} |------\nDay: {i[1]} ({i[2]})\nTrade: {i[3]} ({i[4]})\n\n"

    return text
