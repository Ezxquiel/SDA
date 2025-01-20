# Jz company
from datetime import date

def Edad(year:int):
    year_actual = date.today().year
    edad = year_actual - year
    print(edad)



#Edad(2008) #salida es de 20

#para usarla importar 
#from utils.Edad_actual import Edad

#usar en Edad(2005) usar una fecha en números

