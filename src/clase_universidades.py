

import pandas as pd
import numpy as np
import requests
import mysql.connector
import sys

#Importamos la librería para sacar las coordenadas.
from geopy.geocoders import Nominatim

#Importamos la librería de variables.
sys.path.append("../")
from src import libreria_variables as lv




class Universidades():

    def __init__(self, nombre_bbdd, contraseña):
        """Este es el constructor de la clase.
        Args:
        - nombre_bbdd: string. Es el nombre que deseamos ponerle a la base de datos que crearemos más adelante.
        - contraseña: string. Es la contraseña del servidor de MySQL."""

        self.nombre_bbdd = nombre_bbdd
        self.contraseña = contraseña
   

    def extraer_argentina(self):
        """Esta función llama a la API y extrae los datos de las universidades de Argentina.
        No recibe parámetros.
        Returns: un dataframe."""

        url_argentina = "http://universities.hipolabs.com/search?country=Argentina"
        response_argentina = requests.get(url = url_argentina)
        print(f"La solicitud ha tenido una respuesta con código {response_argentina.status_code}, y nos devuelve el mensaje {response_argentina.reason}")
        df_argentina = pd.DataFrame(response_argentina.json())
        return df_argentina
    

    def extraer_canada(self):
        """Esta función llama a la API y extrae los datos de las universidades de Canadá.
        No recibe parámetros.
        Returns: un dataframe."""

        url_canada = "http://universities.hipolabs.com/search?country=Canada"
        response_canada = requests.get(url = url_canada)
        print(f"La solicitud ha tenido una respuesta con código {response_canada.status_code}, y nos devuelve el mensaje {response_canada.reason}")
        df_canada = pd.DataFrame(response_canada.json())
        return df_canada
    

    def extraer_eeuu(self):
        """Esta función llama a la API y extrae los datos de las universidades de Estados Unidos.
        No recibe parámetros.
        Returns: un dataframe."""

        url_eeuu = "http://universities.hipolabs.com/search?country=United States"
        response_eeuu = requests.get(url = url_eeuu)
        print(f"La solicitud ha tenido una respuesta con código {response_eeuu.status_code}, y nos devuelve el mensaje {response_eeuu.reason}")
        df_eeuu = pd.DataFrame(response_eeuu.json())
        return df_eeuu
    
    
    def limpieza(self, df):
        """Esta función recibe un dataframe, limpia las columnas, elimina la columna 'domains', elimina todos los enlaces a las páginas web menos el primero de cada universidad,
        cambia los nulos por "Unknown" y unifica los nombres de las provincias.
        Args:
        - El dataframe que se quiere limpiar.
        Returns: el dataframe modificado."""

        df.rename(columns = {col:col.replace("-", "_") for col in df.columns}, inplace = True)

        df.drop(["domains"], axis = 1, inplace = True)

        df= df.explode("web_pages")

        duplicados = df.duplicated(["name"]).sum()
        print(f"El dataframe tiene {duplicados} duplicados.")
        
        if duplicados > 0:
            df.drop_duplicates(["name"], inplace = True)
        print(f"Después de la limpieza, el dataframe tiene {df.duplicated(['name']).sum()} duplicados.")
        
        df.fillna(value= np.nan, inplace=True)
        print(f"El dataframe tiene un total de {df['state_province'].isnull().sum()} nulos en la columna 'state_province'.")

        df.fillna(value= "Unknown", inplace=True)
        print(f"Después de la limpieza, el dataframe tiene un total de {df['state_province'].isnull().sum()} nulos en la columna 'state_province'.")


        for k,v in lv.cambio_provincias.items():

            df["state_province"].replace(k,v, inplace = True)

        return df
    
    
    def sacar_coordenadas(self, df_argentina, df_canada, df_eeuu):
        """Esta función recibe tres dataframes y extrae las coordenadas de cada una de las provincias que aparecen en ellos.
        Args:
        - df_argentina: el dataframe con los datos de Argentina.
        - df_canada: el dataframe con los datos de Canadá.
        - df_eeuu: el dataframe con los datos de Estados Unidos.
        Returns: un dataframe nuevo con las coordenadas y los nombres de todas las provincias."""

        provincias_argentina = df_argentina["state_province"].unique()
        provincias_canada = df_canada["state_province"].unique()
        provincias_eeuu = df_eeuu["state_province"].unique()
        provincias = set(list(provincias_argentina) + list(provincias_canada) + list(provincias_eeuu))
        provincias.remove("Unknown")
        provincias = list(provincias)
        latitudes = []
        longitudes = []

        for elem in provincias:

            geolocator = Nominatim(user_agent="Lidya")
            location = geolocator.geocode(elem)
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)

        provincias.append("Unknown")
        latitudes.append("Unknown")
        longitudes.append("Unknown")    

        dicc_latlon = {"state_province": provincias, "latitude" : latitudes, "longitude": longitudes}
        df_latitud_longitud = pd.DataFrame(dicc_latlon)

        return df_latitud_longitud
    

    def unir_dataframes(self, df_argentina, df_canada, df_eeuu, df_latitud_longitud):
        """Esta función recibe cuatro dataframes y los une en uno solo, los tres primeros concatenados por filas y el último mergeado por columnas.
        Args:
        - df_argentina: el dataframe con los datos de Argentina.
        - df_canada: el dataframe con los datos de Canadá.
        - df_eeuu: el dataframe con los datos de Estados Unidos.
        - df_latitud_longitud: el dataframe con los datos de las coordenadas.
        Returns: un dataframe final con todos los datos extraídos hasta ahora."""

        df_paises = pd.concat([df_argentina, df_canada, df_eeuu], axis = 0)
        df_completo = df_paises.merge(df_latitud_longitud, on='state_province')

        return df_completo
    

    def crear_bbdd_sql(self):
        """Esta función hace la conexión con MySQL y crea una base de datos con el nombre elegido en el método constructor.
        No recibe parámetros.
        Returns: un mensaje que indica si la operación ha tenido éxito o no."""


        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password=f'{self.contraseña}') 
        mycursor = mydb.cursor()
        print("Conexión realizada con éxito.")

        try:
            mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.nombre_bbdd};")
            return f"La base de datos {self.nombre_bbdd} ha sido creada correctamente."
            
        except:
            return "Ha sucedido un error en la creación de la base de datos."

    
    def crear_tablas_sql(self):
        """Esta función hace la conexión con MySQL y crea las tablas con las queries definidas en la librería de variables importada.
        No recibe parámetros.
        Returns: un mensaje que indica si la operación ha tenido éxito o no."""
        
        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password=f'{self.contraseña}', 
                                       database=f"{self.nombre_bbdd}") 
        mycursor = mydb.cursor()
        
        try:
            mycursor.execute(lv.tabla_paises)
            mycursor.execute(lv.tabla_universidades)
            mydb.commit()
            return "Las tablas 'paises' y 'universidades' han sido creadas correctamente."
          
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)


    def insertar_datos_sql(self, query):
        """Esta función hace la conexión con MySQL y aplica las queries que le indiquemos.
        Args:
        - query: str. La query que contiene el código para insertar los datos.
        Returns: un mensaje que indica si la operación ha tenido éxito o no."""

        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password=f'{self.contraseña}', 
                                       database=f"{self.nombre_bbdd}") 
        mycursor = mydb.cursor()
        
        try:
            mycursor.execute(query)
            mydb.commit()
            return "Las inserción se ha realizado correctamente."
          
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
    
    
    def extraer_idestado(self, provincia):
        """Esta función hace la conexión con MySQL y extrae los índices de 'idestado' según la provincie que indiquemos.
        Args:
        - provincia: str. La provincia de la que deseamos extraer el índice.
        Returns: un mensaje que indica si la operación ha tenido éxito o no."""
    
        mydb = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password=f'{self.contraseña}', 
                                       database=f"{self.nombre_bbdd}") 

        mycursor = mydb.cursor()
        
        try:
            query_sacar_id = f"SELECT idestado FROM paises WHERE nombre_provincia = '{provincia}'"
            mycursor.execute(query_sacar_id)
            id_ = mycursor.fetchall()[0][0]
            return id_
        
        except: 
            return "Lo lamentamos, no tenemos información de ese país en la base de datos."