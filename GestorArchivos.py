import os
import re
import shutil
import time
import zipfile
import datetime
from gulagcleaner.gulagcleaner_extract import deembed
from gulagcleaner.gulagcleaner_extract import extract_metadata

class GestorArchivos:
    criterio = ""
    directorio = None
    archivosArrayList = []
    indices = []
    archivosArrayListTipo = []
    carpetasCreadas = []
    informe = ""
    DecisionZip = False

    @staticmethod
    def getcriterio():
        return GestorArchivos.criterio

    @staticmethod
    def setCriterio(criterio):
        GestorArchivos.criterio = criterio

    @staticmethod
    def getDirectorio():
        return GestorArchivos.directorio

    @staticmethod
    def setDirectorio(directorio):
        GestorArchivos.directorio = directorio

    @staticmethod
    def comprobarDirectorio():
        cambiarlo = ""
        directorioNuevo = ""

        if GestorArchivos.getDirectorio() is not None:
            print("El directorio definido es", GestorArchivos.getDirectorio())
            cambiarlo = input("¿Quieres cambiarlo? Si es así, responde 'si': ")

            if cambiarlo.lower() == "si":
                directorioNuevo = input("Introduce el nuevo directorio: ")
                while directorioNuevo == "":
                    directorioNuevo = input("Introduce el nuevo directorio: ")

                GestorArchivos.setDirectorio(directorioNuevo)
            else:
                print("Vale, usaremos el directorio ya definido")
        else:
            directorioNuevo = input("Introduce el directorio para la ejecucion: ")
            GestorArchivos.setDirectorio(directorioNuevo)

    @staticmethod
    def carpeta():
        carpetaObj = os.path.abspath(GestorArchivos.getDirectorio())
        return carpetaObj

    @staticmethod
    def getListado():
        return os.listdir(GestorArchivos.carpeta())

    def completo(self):
        cadena = "El directorio es " + GestorArchivos.directorio
        return cadena

    @staticmethod
    def mostrarTodosArchivosLista():
        print("Ruta busqueda archivos:", GestorArchivos.getDirectorio())
        listado = GestorArchivos.getListado()
        if len(listado) != 0:
            print("Se han encontrado", len(listado), "archivos")
            time.sleep(0.4)
            for archivo in listado:
                print(archivo)
        else:
            print("No se ha encontrado ningún archivo en la ruta")

    @staticmethod
    def filtroporCriterio():
            GestorArchivos.archivosArrayList.clear()
            criterio = GestorArchivos.getcriterio()
            listado = GestorArchivos.getListado()
            #print("Listado de archivos obtenido:", listado)  # Depuración

            for archivo in listado:
                #print("Verificando archivo:", archivo)  # Depuración
                if archivo.startswith(criterio):
                    print("Archivo " + archivo + " empieza por: " + criterio)
                    GestorArchivos.archivosArrayList.append(archivo)

             #print("Archivos que cumplen el criterio:", GestorArchivos.archivosArrayList)  # Depuración

    @staticmethod
    def filtroporTipo(tipo):
        listado = GestorArchivos.getListado()

        for archivo in listado:
            print("Verificando archivo:", archivo)  # Depuración
            if archivo.endswith(tipo):
                print("Archivo " + archivo + " termina por: " + tipo)
                GestorArchivos.archivosArrayListTipo.append(archivo)

    @staticmethod
    def replaceName(nombreQuerido):
        print("Mostrando archivos que empiecen por", GestorArchivos.getcriterio(), ":")
        GestorArchivos.filtroporCriterio()

        if len(GestorArchivos.archivosArrayList) != 0:
            for archivo in GestorArchivos.archivosArrayList:
                file = os.path.join(GestorArchivos.getDirectorio(), archivo)
                archivoRenamed = archivo.replace(GestorArchivos.criterio, nombreQuerido)

                fileRenamed = os.path.join(GestorArchivos.getDirectorio(), archivoRenamed)
                os.rename(file, fileRenamed)

                print("Se ha renombrado el archivo " + archivo + " por " + archivoRenamed)
                GestorArchivos.informe += "Se ha renombrado el archivo " + archivo + " por " + archivoRenamed
                GestorArchivos.informe += "\n"
        else:
            print("No se ha encontrado ningún archivo que cumpla el criterio")

        print("\n")
        GestorArchivos.informe += "\n"
        GestorArchivos.generarinforme()
        GestorArchivos.resetearinforme()
        GestorArchivos.resetearlistas()

    @staticmethod
    def deleteName():
        print("Mostrando archivos que empiecen por", GestorArchivos.getcriterio(), ":")
        GestorArchivos.filtroporCriterio()

        if len(GestorArchivos.archivosArrayList) != 0:
            for archivo in GestorArchivos.archivosArrayList:
                file = os.path.join(GestorArchivos.getDirectorio(), archivo)
                fileRenamed = os.path.join(GestorArchivos.getDirectorio(), archivo.lstrip(GestorArchivos.criterio))
                os.rename(file, fileRenamed)
                print("Se ha renombrado el archivo " + archivo + " por " + archivo.lstrip(GestorArchivos.criterio))
                GestorArchivos.informe += "Se ha renombrado el archivo " + archivo + " por " + archivo.lstrip(GestorArchivos.criterio)
                GestorArchivos.informe += "\n"
        else:
            print("No se ha encontrado ningún archivo que cumpla el criterio")

        print("\n")
        GestorArchivos.informe += "\n"
        GestorArchivos.generarinforme()
        GestorArchivos.resetearinforme()
        GestorArchivos.resetearlistas()

    @staticmethod
    def crearcarpeta(nombrecarpeta):
        rutacarpeta = os.path.join(GestorArchivos.getDirectorio(), nombrecarpeta)

        try:
            os.mkdir(rutacarpeta)
            print("Se ha creado la carpeta", nombrecarpeta)
            GestorArchivos.carpetasCreadas.append(nombrecarpeta)
        except FileExistsError:
            print("La carpeta", nombrecarpeta, "ya existe")

    @staticmethod
    def moverArchivos(carpetadestino):
        rutaDestino = os.path.join(GestorArchivos.getDirectorio(), carpetadestino)

        for archivo in GestorArchivos.archivosArrayList:
            rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), archivo)
            try:
                shutil.move(rutaArchivo, rutaDestino)
                print("El archivo", archivo, "ha sido movido a la carpeta", carpetadestino)
            except:
                print("Error al mover el archivo", archivo)

    @staticmethod
    def moverarchivostipo(carpetadestino):
        rutaDestino = os.path.join(GestorArchivos.getDirectorio(), carpetadestino)

        for archivo in GestorArchivos.archivosArrayListTipo:
            rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), archivo)
            try:
                shutil.move(rutaArchivo, rutaDestino)
                print("El archivo", archivo, "ha sido movido a la carpeta", carpetadestino)
            except:
                print("Error al mover el archivo", archivo)

    @staticmethod
    def moveType(tipo):
        GestorArchivos.filtroporTipo(tipo)
        GestorArchivos.crearcarpeta(tipo)
        GestorArchivos.moverarchivostipo(tipo)


    @staticmethod
    def eliminarwuolah():
        GestorArchivos.criterio = 'wuolah-free'
        GestorArchivos.filtroporCriterio()

        for archivo in GestorArchivos.archivosArrayList:
            archivoruta = os.path.join(GestorArchivos.getDirectorio(), archivo)
            deembed(archivoruta)
            print("Archivo " + archivo + " limpiado con exito")
            print(extract_metadata(archivoruta))

        GestorArchivos.resetearinforme()
        GestorArchivos.resetearlistas()

    @staticmethod
    def eliminarygestionarwuolah():
        GestorArchivos.criterio = 'wuolah-free'

        GestorArchivos.archivosArrayList.clear()
        criterio = GestorArchivos.getcriterio()
        listado = GestorArchivos.getListado()
        # print("Listado de archivos obtenido:", listado)  # Depuración

        for archivo in listado:
            # print("Verificando archivo:", archivo)  # Depuración
            if archivo.startswith(criterio) and archivo.endswith(".pdf"):
                print("Archivo " + archivo + " empieza por: " + criterio + " y es de tipo pdf")
                GestorArchivos.archivosArrayList.append(archivo)

        for nombrearchivo in GestorArchivos.archivosArrayList:
            print("Archivo a organizar y limpiar " + nombrearchivo)
            archivo = os.path.join(GestorArchivos.getDirectorio(), nombrearchivo)

            ## Obtener informacion Universidad, Asignatura...

            try:
                metadata = extract_metadata(archivo)

                # Obtener cada valor por separado
                asignatura = metadata['Asignatura']
                curso_grado = metadata['Curso y Grado']
                facultad = metadata['Facultad']
                universidad = metadata['Universidad']

                # Imprimir los valores obtenidos
                print("Asignatura:", asignatura)
                print("Curso y Grado:", curso_grado)
                print("Facultad:", facultad)
                print("Universidad:", universidad)

                carpetaUni = ""
                carpetaFacultad = ""
                carpetaAsignatura = ""
                carpetaCursoGrado = ""

                ## Comprobamos la fecha de creacion del archivo para saber que metodo usar
                info_archivo = os.stat(archivo)

                # Obtener la fecha de creación del archivo
                fecha_creacion = datetime.datetime.fromtimestamp(info_archivo.st_ctime)
                print(fecha_creacion)

                # Comparar la fecha de creación con el 8/5/2023
                fecha_limite = datetime.datetime(2023, 5, 8)

            except Exception as e:
                print("Error:", str(e))
                break;

            try:
                carpetaUni = os.path.join(GestorArchivos.getDirectorio(), universidad)
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

                rutaFinal = os.path.join(carpetaAsignatura, nombrearchivo)
                shutil.move(archivo, rutaFinal)
                print("Se ha movido " + nombrearchivo + " a " + rutaFinal)

                """ 
                   Limpiamos el pdf de publicidad 

                   """

                if fecha_creacion < fecha_limite:
                    print("La fecha de creación del archivo es anterior al 8/5/2023.")
                    deembed(rutaFinal, True, "old")
                else:
                    print("La fecha de creación del archivo es posterior al 8/5/2023.")
                    print(deembed(rutaFinal, True))

            except NotADirectoryError:
                    print("El directorio no es válido.")
            except Exception as e:
                    print("Error:", str(e))

        GestorArchivos.resetearinforme()
        GestorArchivos.resetearlistas()

    @staticmethod
    def eliminarRepetidos():
        repetidos = GestorArchivos.getListado().copy()[::-1]
        pattern0 = r"(.*)\.([^\.]+)$"
        r0 = re.compile(pattern0)
        archivos_a_eliminar = []

        for fileName in repetidos:
            print("Archivo: " + fileName)
            m0 = r0.match(fileName)
            file = os.path.join(GestorArchivos.getDirectorio(), fileName)

            if m0 and not os.path.isdir(file):
                fileName = m0.group(1)

        listaRepetidos = list(repetidos)  # Copia la lista

        i = 0
        while i < len(listaRepetidos)-1:
            print(listaRepetidos[i])
            # Patron archivo (1)
            pattern = r"(.*) \((\d+)\)$"
            r = re.compile(pattern)
            m = r.match(listaRepetidos[i])
            m2 = r.match(listaRepetidos[i + 1])

            # Patron archivo - copia.tipo
            pattern3 = r"(.*) \- copia \(\d+\)$"
            r3 = re.compile(pattern3)
            m3 = r3.match(listaRepetidos[i])

            if(m3 is None):
                m3 = r3.match(listaRepetidos[i+1])
            else:
                print("SI " + m3.group(1))

            #Pattern que utilizamos para separar cada archivo y su tipo
            patternTipo = r"^(.*?)\.([^.]+)$"
            rTipo = re.compile(patternTipo)
            archivoSiguienteSinTipo = rTipo.match(listaRepetidos[i+1])


            if m:
                print("Archivo que coincide con el patron (posible repetido): " + listaRepetidos[i] + ' coincide con: ' + listaRepetidos[i + 1])

                #Si coincide, implica que el siguiente será otra copia, o el archivo original (el primero)
                print(m.group(1) + ' y ' + listaRepetidos[i + 1])


                ## Si esto se ejecuta, implica que hay otro archivo tambien que cumple con la expresion regular
                if m2 and m.group(1) == m2.group(1): ## Si tienen el mismo nombre base
                    GestorArchivos.archivosArrayList.append(GestorArchivos.getListado()[i])
                    GestorArchivos.informe += "Archivo " +GestorArchivos.getListado()[i] + " repetido eliminado.\n"
                    file1 = os.path.join(GestorArchivos.getDirectorio(),GestorArchivos.archivosArrayList[0])
                    os.remove(file1)
                    GestorArchivos.archivosArrayList.clear()
                    del listaRepetidos[i]
                    i -= 1

                ## Si no se cumplen las condiciones anteriores y el nombre base del archivo actual (m.group(1))
                # sea igual al nombre base del siguiente archivo en listaRepetidos, se considera que el archivo actual
                # y el siguiente archivo son duplicados
                ##
                elif m.group(1) == archivoSiguienteSinTipo.group(1):
                    print("Se han encontrado archivos repetidos: " + m.group(1))
                    GestorArchivos.archivosArrayList.append(GestorArchivos.getListado()[i])
                    GestorArchivos.informe+= "Archivo " + GestorArchivos.getListado()[i] + " repetido eliminado.\n"
                    file1 = os.path.join(GestorArchivos.getDirectorio(), GestorArchivos.archivosArrayList[0])
                    os.remove(file1)
                    GestorArchivos.archivosArrayList.clear()

                    del listaRepetidos[i]
                    i -= 1

            if m3:
                print("Archivo que coincide con el patron (copia): " + listaRepetidos[i] + ' coincide con: ' + listaRepetidos[i + 1])

                if m3.group(1) == archivoSiguienteSinTipo.group(1):
                    GestorArchivos.archivosArrayList.append(GestorArchivos.getListado()[i])
                    GestorArchivos.informe+= "Archivo " + GestorArchivos.getListado()[i] + " repetido eliminado.\n"
                    file1 = os.path.join(GestorArchivos.getDirectorio(), GestorArchivos.archivosArrayList[0])
                    os.remove(file1)
                    GestorArchivos.archivosArrayList.clear()
                    del listaRepetidos[i]
                    i -= 1

            i += 1
        print("")

        try:
            if len(GestorArchivos.informe) != 0:
                GestorArchivos.generarInforme()
                print("Generado informe con los cambios ")
            else:
                print("No se ha eliminado ningún archivo")
        except FileNotFoundError as e:
            print(e)

        GestorArchivos.resetearlistas()
        GestorArchivos.resetearinforme()

    @staticmethod
    def generarInforme():
        informe = "Informe de la ejecución:\n"
        informe += "========================\n\n"
        informe += "Directorio de búsqueda: " + GestorArchivos.getDirectorio() + "\n\n"

        if GestorArchivos.getcriterio() != "":
            informe += "Criterio de búsqueda: " + GestorArchivos.getcriterio() + "\n"
        else:
            informe += "Criterio de búsqueda: No se ha especificado\n"

        informe += "Archivos encontrados: " + str(len(GestorArchivos.archivosArrayList)) + "\n"
        informe += "Tipos de archivos encontrados: " + str(len(GestorArchivos.archivosArrayListTipo)) + "\n\n"

        informe += "Archivos renombrados: " + str(len(GestorArchivos.archivosArrayList)) + "\n"
        informe += "Carpetas creadas: " + str(len(GestorArchivos.carpetasCreadas)) + "\n\n"

       # informe += "Archivos movidos a carpetas: " + str(len(GestorArchivos.archivosArrayList)) + "\n"

        GestorArchivos.informe = informe

    @staticmethod
    def guardarInforme():
        fecha = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        nombreArchivo = "informe_" + fecha + ".txt"
        rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), nombreArchivo)

        with open(rutaArchivo, "w") as archivo:
            archivo.write(GestorArchivos.informe)

        print("Informe guardado en:", rutaArchivo)

    @staticmethod
    def comprimirArchivos():
        fecha = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        nombreArchivo = "archivos_" + fecha + ".zip"
        rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), nombreArchivo)

        with zipfile.ZipFile(rutaArchivo, "w") as zipObj:
            for archivo in GestorArchivos.archivosArrayList:
                rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), archivo)
                zipObj.write(rutaArchivo, os.path.basename(archivo))

        print("Archivos comprimidos en:", rutaArchivo)

    @staticmethod
    def moverarchivos():
        if len(GestorArchivos.archivosArrayList) > 0:
            for archivo in GestorArchivos.archivosArrayList:
                rutaArchivo = os.path.join(GestorArchivos.getDirectorio(), archivo)
                nombreCarpeta = os.path.splitext(archivo)[0]
                rutaCarpeta = os.path.join(GestorArchivos.getDirectorio(), nombreCarpeta)

                if not os.path.exists(rutaCarpeta):
                    os.makedirs(rutaCarpeta)
                    GestorArchivos.carpetasCreadas.append(rutaCarpeta)

                try:
                    shutil.move(rutaArchivo, rutaCarpeta)
                    print("Se ha movido el archivo", archivo, "a la carpeta", nombreCarpeta)
                except Exception as e:
                    print("Error al mover el archivo", archivo + ":", str(e))
        else:
            print("No hay archivos para mover.")

    @staticmethod
    def generarinforme():
       # GestorArchivos.informe = "Informe de Gestión\n\n"
        GestorArchivos.informe += "Fecha: " + time.strftime("%Y-%m-%d") + "\n\n"
        GestorArchivos.informe += "Archivos encontrados:\n"
        for archivo in GestorArchivos.archivosArrayList:
            GestorArchivos.informe += "- " + archivo + "\n"

        GestorArchivos.informe += "\nCarpetas creadas:\n"
        for carpeta in GestorArchivos.carpetasCreadas:
            GestorArchivos.informe += "- " + carpeta + "\n"

        nombreArchivoInforme = "informe_" + GestorArchivos.criterio + time.strftime("%Y%m%d%H%M%S") + ".txt"
        rutaArchivoInforme = os.path.join(GestorArchivos.getDirectorio(), nombreArchivoInforme)

        try:
            with open(rutaArchivoInforme, "w") as archivoInforme:
                archivoInforme.write(GestorArchivos.informe)

            print("Se ha generado el informe:", nombreArchivoInforme)
        except Exception as e:
            print("Error al generar el informe:", str(e))

    @staticmethod
    def resetearlistas():
        GestorArchivos.archivosArrayList.clear()
        GestorArchivos.carpetasCreadas.clear()
    @staticmethod
    def resetearinforme():
        GestorArchivos.informe = ""
