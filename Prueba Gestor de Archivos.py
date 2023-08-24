import os
import json
import shutil
import datetime

from gulagcleaner.gulagcleaner_extract import deembed
from gulagcleaner.gulagcleaner_extract import extract_metadata

directorio = "" ## ESCRIBIR DIRECTORIO

archivosArrayList = []


@staticmethod
def carpeta():
    carpetaObj = os.path.abspath(directorio)
    return carpetaObj


@staticmethod
def getListado():
    return os.listdir(carpeta())


def soloPdf():
    listado = getListado()

    for archivo in listado:
        if archivo.startswith("wuolah-free-") and archivo.endswith(".pdf"):
            archivosArrayList.append(archivo)


@staticmethod
def prueba():
    # ruta = "C:\\Users\\Alejandro\\Downloads\\pruebagulag"
    ruta = directorio
    # nombreArchivo = 'wuolah-free-Formulario-Final-Todos-Los-Temas.pdf'
    soloPdf()

    for nombreArchivo in archivosArrayList:

        print(nombreArchivo)
        # nombreArchivo = "wuolah-free-Enunciados.pdf"
        # ruta = "C:\\Users\\Alejandro\\Downloads\\pdfwuolah\\"

        archivo = os.path.join(ruta, nombreArchivo)
        data = str(extract_metadata(archivo))

        # Eliminar las comillas simples alrededor del string y convertirlo a JSON válido
        data = data.replace("'", "\"")

        # Analizar el string JSON
        parsed_data = json.loads(data)

        # Obtener cada valor por separado
        archivoJson = parsed_data['Archivo']
        autor = parsed_data['Autor']
        asignatura = parsed_data['Asignatura']
        curso_grado = parsed_data['Curso y Grado']
        facultad = parsed_data['Facultad']
        universidad = parsed_data['Universidad']

        # Imprimir los valores obtenidos
        print("Archivo:", archivo)
        print("Autor:", autor)
        print("Asignatura:", asignatura)
        print("Curso y Grado:", curso_grado)
        print("Facultad:", facultad)
        print("Universidad:", universidad)

        # Comprobamos la fecha de creacion del archivo para saber que metodo usar
        info_archivo = os.stat(archivo)

        # Obtener la fecha de creación del archivo
        fecha_creacion = datetime.datetime.fromtimestamp(info_archivo.st_ctime)
        print(fecha_creacion)

        # Comparar la fecha de creación con el 8/5/2023
        fecha_limite = datetime.datetime(2023, 5, 8)

        carpetaUni = os.path.join(ruta, universidad)
        if not (os.path.exists(carpetaUni)):
            os.mkdir(carpetaUni)

        carpetaFacultad = os.path.join(carpetaUni, facultad)
        if not (os.path.exists(carpetaFacultad)):
            os.mkdir(carpetaFacultad)

        carpetaCursoGrado = os.path.join(carpetaFacultad, curso_grado)
        if not (os.path.exists(carpetaCursoGrado)):
            os.mkdir(carpetaCursoGrado)

        carpetaAsignatura = os.path.join(carpetaCursoGrado, asignatura)
        if not (os.path.exists(carpetaAsignatura)):
            os.mkdir(carpetaAsignatura)

        rutaFinal = os.path.join(carpetaAsignatura, nombreArchivo)
        shutil.move(archivo, rutaFinal)
        print("Se ha movido " + archivo + " a " + rutaFinal)

        """ 
        Limpiamos el pdf de publicidad 

        """

        if fecha_creacion < fecha_limite:
            print("La fecha de creación del archivo es anterior al 8/5/2023.")
            deembed(rutaFinal, True, "old")
        else:
            print("La fecha de creación del archivo es posterior al 8/5/2023.")
            print(deembed(rutaFinal, True))


prueba()