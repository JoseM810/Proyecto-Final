"""Interfaz de consola de la red social (MVP).

Punto de entrada del sistema. Orquesta los módulos de dominio
y permite al usuario navegar mediante un menú de texto.
"""

import sys

from dominio.sistema_red import SistemaRed
from dominio.generador_usuarios import GeneradorUsuarios


def mostrar_menu():
    """Muestra el menú principal de la aplicación.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print("\n=== RED SOCIAL - MENÚ PRINCIPAL ===")
    print("1. Listar usuarios")
    print("2. Seleccionar usuario activo")
    print("3. Buscar usuario por nombre")
    print("4. Publicar en mi feed")
    print("5. Ver mi feed")
    print("6. Seguir a un usuario")
    print("7. Dejar de seguir a un usuario")
    print("8. Ver recomendaciones")
    print("9. Ver mis notificaciones")
    print("10. Comentar en una publicación")
    print("11. Responder a un comentario")
    print("12. Ver comentarios de una publicación")
    print("0. Salir")
    print("===================================")


def opcion_no_implementada(opcion):
    """Muestra mensaje para opciones que aún no están implementadas.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print(f"\nLa opción {opcion} aún no está implementada.")


def salir():
    """Termina la ejecución del programa.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print("\nSaliendo de la aplicación. ¡Hasta pronto!")
    sys.exit(0)


def cargar_usuarios_iniciales(sistema):
    """Carga usuarios iniciales con semilla fija en el sistema.

    Complejidad: Tiempo O(n·h), espacio O(n), con n la cantidad de usuarios
    y h la altura del BST.
    """
    generador = GeneradorUsuarios(semilla=42)
    datos = generador.generar(100)
    sistema.cargar_desde_generador(datos)
    return sistema


def listar_usuarios(sistema):
    """Muestra los usuarios registrados en orden alfabético.

    Complejidad: Tiempo O(n), espacio O(h), con n la cantidad de usuarios
    y h la altura del BST.
    """
    usuarios = list(sistema.listar_usuarios())
    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return
    print("\n--- Usuarios registrados ---")
    for nombre in usuarios:
        print(f"- {nombre}")
    print(f"Total: {len(usuarios)} usuarios")


def seleccionar_usuario(sistema):
    """Selecciona un usuario como activo para la sesión.

    Complejidad: Tiempo O(h), espacio O(1), con h la altura del BST.
    """
    username = input("Ingrese el nombre de usuario: ").strip()
    usuario = sistema.buscar_usuario_por_nombre(username)
    if usuario is None:
        print(f"\nEl usuario '{username}' no existe.")
        return None
    print(f"\nUsuario activo: {usuario.nombre_visible} (@{usuario.username})")
    return usuario


def main():
    """Función principal de la aplicación de consola.

    Complejidad: Tiempo O(n) donde n es el número de iteraciones del bucle,
    espacio O(1).
    """
    sistema = SistemaRed()
    cargar_usuarios_iniciales(sistema)

    usuario_activo = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            salir()
        elif opcion == "1":
            listar_usuarios(sistema)
        elif opcion == "2":
            usuario_seleccionado = seleccionar_usuario(sistema)
            if usuario_seleccionado is not None:
                usuario_activo = usuario_seleccionado
        else:
            opcion_no_implementada(opcion)


if __name__ == "__main__":
    main()
