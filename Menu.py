import os
import shutil
from GestorArchivos import GestorArchivos

class Menu:

    @staticmethod
    def introMenu():
        sc = input()

        print("")
        print("")
        print("¡Escoja una opcion!")
        print("\t\t\tAutor: MrSh4d0w")
        print("1. Eliminar la primera parte del nombre de un archivo (tu delimitas cual es esta) ")
        print(
            "2. Sustituir la primera parte del nombre de un archivo (tu delimitas cual es esta) por el nombre que quieras")
        print("3. Crear una carpeta para un tipo de archivo y mover todos los archivos que cumplan ese tipo a ella")
        print("4. Elimina toda la publicidad de wuolah y organiza tus apuntes")
        print(
            "5. Organiza todos los archivos por carpetas con el nombre del tipo que sean (pdf: todos los pdf, docx: todos los docx...)")
        print("6. Elimina todos los archivos repetidos que haya en la carpeta")
        print("7. Exit")

        decisionMenu = 0

        while True:
            try:
                decisionMenu = int(input())
                break
            except ValueError:
                print("Error: valor no válido")

        Menu.eleccionmenu(decisionMenu)


    @staticmethod
    def eleccionmenu(decisionMenu):
        sc = input()
        nombreBorrar = ""
        nombreQuerido = ""

        print("")

        if decisionMenu == 1:
            print("Eliminaremos la primera parte del nombre un archivo o archivos")
            GestorArchivos.comprobarDirectorio()

            print("¿Que parte quieres eliminar?")
            nombreBorrar = input()
            print("Vamos a borrar " + nombreBorrar)
            GestorArchivos.setCriterio(nombreBorrar)

            GestorArchivos.deleteName()
            Menu.introMenu()

        elif decisionMenu == 2:
            print("Sustituiremos la primera parte del nombre un archivo o archivos")
            GestorArchivos.comprobarDirectorio()

            print("¿Que parte quieres eliminar?")
            nombreBorrar = input()
            GestorArchivos.setCriterio(nombreBorrar)
            print(GestorArchivos.getcriterio())

            print("¿Que quieres poner en su lugar?")
            nombreQuerido = input()
            print(nombreQuerido)

            GestorArchivos.replaceName(nombreQuerido)
            Menu.introMenu()

        elif decisionMenu == 3:
            print(
                "Creamos una carpeta para un tipo de archivo y moveremos todos los archivos que cumplan ese tipo a ella")
            GestorArchivos.comprobarDirectorio()

            print("¿Que tipo quieres? (java,txt,docx...)")
            tipo = input()

            GestorArchivos.moveType(tipo)

            Menu.main()

        elif decisionMenu == 4:
           # print("Quita la publicidad de wuolah del nombre y del archivo pdf")
            print(" Elimina toda la publicidad de wuolah y organiza tus apuntes por universidad, facultad, curso y asignatura")
            GestorArchivos.comprobarDirectorio()
            GestorArchivos.eliminarygestionarwuolah()
            #print("Crea paquetes de java a partir de los archivos java encontrados")
            #print("Este programa procura organizar archivos java sueltos y asignarle sus respectivos paquetes")
            #GestorArchivos.comprobarDirectorio()
            Menu.introMenu()

        elif decisionMenu == 5:
            print(
                "Organiza todos los archivos por carpetas con el nombre del tipo que sean (pdf: todos los pdf, docx: todos los docx...)")
            GestorArchivos.comprobarDirectorio()

            GestorArchivos.eliminarRepetidos()
            GestorArchivos.organizarPorTodosTipos()
            Menu.introMenu()

        elif decisionMenu == 6:
            print("Elimina todos los archivos repetidos que haya en la carpeta")
            GestorArchivos.comprobarDirectorio()
            GestorArchivos.eliminarRepetidos()
            Menu.introMenu()

        elif decisionMenu == 7:
            print("¡Adios! Nos vemos pronto ;)")
            print("\tAutor: MrSh4d0w")
            exit(0)

        else:
            print("Opcion no correcta, por favor escoja otra: ")

    @staticmethod
    def main():
        Menu.introMenu()


Menu.main()  # Agrega esta línea para llamar a la función main y comenzar la ejecución del programa #
