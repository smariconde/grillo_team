import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.




# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

#sheet.row_values(1)

#sheet.col_values(1)

# Utilidad: (fila, columna)
# Variables de lo que se pide
def info():
    sheet = client.open("Acciones con Google Finance").sheet1
    rendimiento = sheet.cell(8, 25).value
    ganancia = sheet.cell(8, 23).value
    if float(ganancia) < 0:
        mensaje = f"Quiena:\nPerdiendo U$S {ganancia}\nRendimiento del {rendimiento}"
    else:
        mensaje = f"Quiena:\nGanando U$S {ganancia}\nRendimiento del {rendimiento}"
    
    datos = sheet.col_values(29)
    datos2 = sheet.col_values(30)
    mensaje2 = mensaje + f"\n\nBecerra:\nGeneral: {datos[5]}, {datos[7]}\nAcciones:\nDólares: {datos[10]}, Pesos: {datos2[10]}\n\nEcoValores:\nDólares: {datos[-1]}, Pesos: {datos2[-1]}"

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
    tickers = [[dic["Symbol"], dic["Day Gain"], dic["Total Gain"], dic["Gain %"]] for dic in datos[1:] if dic["Total Gain"] != 0]

    text = ""
    for i in tickers:
        text += f"------| {i[0]} |------\nDay Gain: {i[1]}\nTotal Gain: {i[2]}\nGain %: {i[3]}\n\n"

    return text
