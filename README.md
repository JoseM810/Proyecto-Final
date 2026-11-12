# Proyecto-Final

Red social de consola — MVP para la primera versión demostrable.

## Objetivo

Una aplicación de consola (CLI) en Python que simula una red social básica. Permite a los usuarios registrarse, seguirse unos a otros, publicar en su propio feed, comentar y responder publicaciones, recibir notificaciones, ver recomendaciones de personas a dos saltos y navegar entre pantallas con un historial de visita/volver.

## Tecnologías utilizadas

- Lenguaje: Python 3.15.2
- Framework de pruebas: pytest (250 pruebas automatizadas)
- Estructuras de datos propias implementadas desde cero: BST (índice de usuarios), grafo dirigido (red de seguimiento), lista doble (feed), pila enlazada (historial), cola enlazada (notificaciones)

## Requisitos

- Python 3.10 o superior
- `uv` (opcional, recomendado para gestionar el entorno)
- No se requieren dependencias externas adicionales

## Instalación y configuración

1. Clona el repositorio:
   ```
   git clone https://github.com/JoseM810/Proyecto-Final.git
   cd Proyecto-Final
   ```

2. (Opcional) Crea y activa el entorno con `uv`:
   ```
   uv sync
   ```

3. No se requieren pasos adicionales de configuración. El proyecto no usa dependencias externas.

## Comando para iniciar la aplicación

Con `uv`:
```
uv run python main.py
```

O directamente con Python:
```
python main.py
```

## Opciones del menú (0-14)

| Opción | Descripción |
|--------|-------------|
| 0 | Salir de la aplicación |
| 1 | Listar usuarios registrados (orden alfabético) |
| 2 | Seleccionar usuario activo para la sesión |
| 3 | Buscar usuario por nombre exacto |
| 4 | Publicar en el feed del usuario activo |
| 5 | Ver y navegar el feed del usuario activo (avanzar/retroceder) |
| 6 | Seguir a otro usuario |
| 7 | Dejar de seguir a otro usuario |
| 8 | Ver recomendaciones de personas a dos saltos |
| 9 | Ver y consultar notificaciones pendientes |
| 10 | Comentar en una publicación |
| 11 | Responder a un comentario existente |
| 12 | Ver comentarios y respuestas de una publicación |
| 13 | Visitar una pantalla (registra en el historial) |
| 14 | Volver a la pantalla anterior (historial) |

## Funcionalidades principales

- **HU-01**: Carga de 100 usuarios con semilla fija para demostraciones reproducibles.
- **HU-02**: Seguir y dejar de seguir usuarios, con notificación al ser seguido.
- **HU-03**: Publicar en el feed propio y navegar adelante/atrás entre publicaciones.
- **HU-04**: Comentar en publicaciones y responder a comentarios (hilos con profundidad).
- **HU-05**: Buscar usuarios por nombre exacto y listar en orden alfabético.
- **HU-06**: Navegar entre pantallas con historial (visitar/volver). El menú captura `NadaAtrasError` cuando no hay pantalla anterior y muestra un aviso sin cerrar la aplicación.
- **HU-07**: Notificaciones por nuevo seguidor, comentario y respuesta. Se leen en orden de llegada y se consumen al leerlas.
- **HU-08**: Recomendaciones de personas que siguen las personas que el usuario sigue (a dos saltos, sin repetidos ni conocidos).

## Cómo ejecutar las pruebas automatizadas

Con `uv`:
```
uv run python -m pytest -q
```

O directamente con Python:
```
python -m pytest -q
```

**Resultado actual: 250 pruebas pasando.**

## Estructura del proyecto

```
Proyecto-Final/
├── main.py                  # Interfaz de consola con menú (opciones 0-14)
├── README.md                # Este archivo
├── dominio/                 # Capa de dominio (reglas de negocio)
│   ├── usuario.py           # Usuario con feed y bandeja de notificaciones
│   ├── feed.py              # Feed individual de publicaciones
│   ├── sistema_red.py       # Orquestador: usuarios, seguimiento, recomendaciones
│   ├── historial.py         # Historial de navegación (visitar/volver)
│   ├── generador_usuarios.py # Generación de usuarios con semilla fija
│   ├── hilo_comentarios.py  # Hilos de comentarios y respuestas
│   ├── red.py               # Red de seguimiento (grafo dirigido)
│   ├── indice_usuarios.py   # Índice de usuarios (BST por username)
│   └── notificaciones.py    # Bandeja de notificaciones (cola)
└── estructuras/             # Estructuras de datos propias
    ├── pila.py              # Pila enlazada
    ├── cola.py              # Cola enlazada
    ├── lista_doble.py       # Lista doblemente enlazada
    ├── arbol_bst.py         # Árbol binario de búsqueda
    ├── grafo.py             # Grafo dirigido
    ├── nodo.py              # Nodo genérico
    └── errores.py           # Excepciones propias del proyecto
└── tests/                   # Pruebas automatizadas (250 tests)
```
