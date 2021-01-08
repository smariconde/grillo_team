import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Acciones con Google Finance").sheet1
sheet2 = client.open("Acciones con Google Finance").worksheet("Plan")

# Extract and print all of the values
#list_of_hashes = sheet.get_all_records()
#print(list_of_hashes)

#sheet.row_values(1)

#sheet.col_values(1)

# Utilidad: (fila, columna)
# Variables de lo que se pide
def quiena():
    rendimiento = sheet.cell(8, 25).value
    ganancia = sheet.cell(8, 23).value
    if float(ganancia) < 0:
        mensaje = f"Perdiendo U$S {ganancia}, con un rendimiento del {rendimiento}"
    else:
        mensaje = f"Ganando U$S {ganancia}, con un rendimiento del {rendimiento}"
    return mensaje

fila = sheet2.row_values(9)
#print(fila)