import requests
import pandas as pd
import datetime

def proceso():
    api = "https://api-token.odepa.gob.cl/oauth/token"

    cuerpo = {"grant_type":"password",
            "username":"dev-user-r",
            "password":12345678}

    url1= "https://api-reportes.odepa.gob.cl/apps-odepa/v1/noticias-mercado/precios-consumidor?mesTermino=1&mesInicio=1&productos=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155&region=99&sector=101&tipoPeso=2&tipoProducto=20&tipoSerie=2&semanaTermino=52&semanaInicio=1&annio=2024&annioTermino=2024&annioInicio=2024&tipoPuntoMonitoreo=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15&ipc=6512"
    response = requests.post(api, data=cuerpo,headers={"authorization": "Basic b2F1dGgyLXV0aWxpdGllczoxMjM0NTY3ODkw","Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"})
    response = requests.get(url1, headers={"Authorization":"Bearer " + response.json()['access_token']})
    df = pd.DataFrame(response.json()["objParams"])
    del df["sector"]
    columnas = ["Semana","Fecha inicio","Fecha término","Región","Tipo punto monitoreo","Producto","Variedad","Calidad","Unidad","Precio mínimo","Precio máximo","Precio promedio"]
    df.columns = columnas
    df["Fecha inicio"]  = df["Fecha inicio"] .apply(lambda x:datetime.datetime.fromtimestamp(x / 1000).strftime("%d-%m-%Y 0:00:00"))
    df["Fecha término"] = df["Fecha término"].apply(lambda x:datetime.datetime.fromtimestamp(x / 1000).strftime("%d-%m-%Y 0:00:00"))
    df["Precio promedio"] = df["Precio promedio"].round(0)
    ref2 = pd.read_excel("producto_tipo.xlsx")
    merge = df.merge(ref2)
    if(len(df) == len(merge)):
        
        merge.to_excel("ODEPA Precios al Consumidor_2024.xlsx", index=False)
    else:
        fecha_maxima = str(df["Fecha término"].max())
        with open(f'archivo_{fecha_maxima}.txt', 'w') as archivo:
        # Escribe en el archivo
            archivo.write('Error')     

if __name__ == '__main__':
    print("Cerradas...")
    proceso()