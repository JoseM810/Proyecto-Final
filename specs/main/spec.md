# Especificación — Interfaz de consola (main.py)
**Versión:** 1.0 · **Fecha:** 12 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Interfaz de consola en Python básico que sirve como punto de entrada del MVP
de la red social. Orquesta los componentes de dominio ya implementados
(SistemaRed, GeneradorUsuarios, Usuario, Feed, Historial, RedSeguimiento,
IndiceUsuarios, BandejaNotificaciones, HiloComentarios) y permite al usuario
navegar por el sistema mediante un menú de texto. Soporta las historias HU-01
a HU-08.

## 2. Fuera de alcance
- Interfaz web (HTML, CSS, JavaScript) ni frameworks.
- Persistencia en disco ni bases de datos: los datos se regeneran con la semilla al iniciar.
- Búsqueda por prefijo: la búsqueda de usuarios es por nombre exacto.
- Autenticación ni contraseñas: no existe login ni sesión.

## 3. Operaciones

### `cargar_usuarios_iniciales()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** carga al menos 100 usuarios con semilla fija (42) usando
  GeneradorUsuarios y SistemaRed.cargar_desde_generador(). Tras la carga
  **no hay usuario activo seleccionado**; debe seleccionarse uno antes de
  usar operaciones que lo requieran.
- **Complejidad:** Tiempo O(n·h), espacio O(n), con n la cantidad de usuarios
  y h la altura del BST (documentado en specs/sistema-red/plan.md).

### `seleccionar_usuario(username)`
- **Precondiciones:** username existe en el índice de usuarios.
- **Postcondiciones:** establece al usuario indicado como el activo para el
  resto de la sesión. Si el username no existe, muestra un mensaje y no cambia
  el usuario activo.
- **Errores:** ninguno lanza excepción; se maneja con mensaje por consola.
- **Complejidad:** Tiempo O(h), espacio O(1).

### `publicar(texto)`
- **Precondiciones:** existe un usuario activo; texto es un texto no vacío.
- **Postcondiciones:** el usuario activo publica en su feed propio, con fecha
  interna 0 y un identificador global único asignado por SistemaRed.
- **Errores:** PublicacionInvalidaError si texto no cumple (delegado en Feed).
- **Complejidad:** Tiempo O(1), espacio O(1).

### `recorrer_feed()`
- **Precondiciones:** existe un usuario activo.
- **Postcondiciones:** muestra las publicaciones del feed del usuario activo,
  permitiendo navegar entre ellas. 'A' va a la publicación más antigua
  (siguiente en la lista); 'R' va a la publicación más reciente (anterior
  en la lista).
- **Complejidad:** Tiempo O(1) por operación de navegación, espacio O(1).

### `explorar_publicaciones()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** muestra las publicaciones de todos los usuarios de la
  red, ordenadas por ID global descendente (más reciente primero), mostrando
  ID, autor y texto. Permite navegar entre todas las publicaciones con
  'A' (más antigua) y 'R' (más reciente).
- **Complejidad:** Tiempo O(1) por operación de navegación, espacio O(m·n)
  donde m es el promedio de publicaciones por usuario y n la cantidad de
  usuarios.

### `seguir_usuario(username_destino)`
- **Precondiciones:** existe un usuario activo y username_destino existe en el
  índice de usuarios.
- **Postcondiciones:** el usuario activo sigue a username_destino. Si la
  relación es nueva, SistemaRed genera una notificación NUEVO_SEGUIDOR para
  username_destino (almacenada en su BandejaNotificaciones).
- **Errores:** UsuarioNoExisteError si alguno de los usuarios no existe;
  AutoSeguimientoError si se intenta seguirse a sí mismo.
- **Complejidad:** Tiempo O(h + g), espacio O(1).

### `dejar_de_seguir_usuario(username_destino)`
- **Precondiciones:** existe un usuario activo y username_destino existe en el
  índice de usuarios.
- **Postcondiciones:** el usuario activo deja de seguir a username_destino.
- **Errores:** UsuarioNoExisteError si alguno de los usuarios no existe.
- **Complejidad:** Tiempo O(h + g), espacio O(1).

### `buscar_usuario(nombre)`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve el usuario con ese nombre exacto, o indica que
  no existe si no se encuentra o si el nombre no es texto.
- **Complejidad:** Tiempo O(h), espacio O(1).

### `listar_usuarios()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** muestra los nombres de usuario en orden alfabético
  ascendente (comparación de Python: mayúsculas antes que minúsculas).
- **Complejidad:** Tiempo O(n), espacio O(h).

### `mostrar_recomendaciones()`
- **Precondiciones:** existe un usuario activo.
- **Postcondiciones:** muestra las personas sugeridas por
  RedSeguimiento.recomendar(id_usuario_activo): personas que siguen los
  seguidos del usuario activo a exactamente dos saltos, que el usuario activo
  no sigue ni es él mismo. Sin repetidos, ordenadas por el primer camino en
  que aparecen en el recorrido BFS limitado a 2 saltos.
- **Complejidad:** Tiempo O(V + E), espacio O(V).

### `consultar_notificaciones()`
- **Precondiciones:** existe un usuario activo.
- **Postcondiciones:** muestra las notificaciones pendientes del usuario
  activo en orden de llegada. Cada llamada a BandejaNotificaciones.leer_siguiente()
  **consume** (descarta) la notificación leída; si no hay pendientes, devuelve
  None y no lanza error.
- **Complejidad:** Tiempo O(1) por notificación leída, espacio O(1).

### `comentar_publicacion(id_publicacion, texto)`
- **Precondiciones:** existe un usuario activo; `id_publicacion` corresponde a
  una publicación existente del feed del usuario activo; `texto` es un texto
  no vacío.
- **Postcondiciones:** crea un comentario de nivel 0 vinculado a la publicación
  indicada, autorizado por el usuario activo.
- **Errores:** PublicacionNoEncontradaError si el id no existe;
  ComentarioInvalidoError si el texto no es válido.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `responder_comentario(id_comentario_padre, texto)`
- **Precondiciones:** existe un usuario activo; `id_comentario_padre` corresponde
  a un comentario existente; `texto` es un texto no vacío.
- **Postcondiciones:** crea una respuesta anidada bajo el comentario indicado,
  autorizada por el usuario activo.
- **Errores:** ComentarioNoEncontradoError si el id padre no existe;
  ComentarioInvalidoError si el texto no es válido.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `ver_comentarios_publicacion(id_publicacion)`
- **Precondiciones:** `id_publicacion` corresponde a una publicación existente.
- **Postcondiciones:** muestra los comentarios y respuestas de la publicación
  en recorrido preorden, con sangría según profundidad.
- **Errores:** PublicacionNoEncontradaError si el id no existe.
- **Complejidad:** Tiempo O(n), espacio O(n), con n la cantidad de comentarios.

### `visitar_pantalla(nombre_pantalla)`
- **Precondiciones:** nombre_pantalla es un texto no vacío.
- **Postcondiciones:** registra la pantalla en el Historial (apilada) y la
  deja como pantalla actual.
- **Errores:** PantallaInvalidaError si nombre_pantalla es nulo o vacío.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `volver_pantalla_anterior()`
- **Precondiciones:** el Historial tiene al menos dos pantallas.
- **Postcondiciones:** vuelve a la pantalla anterior y la deja como actual.
  La pantalla abandonada deja de ser alcanzable.
- **Errores:** NadaAtrasError si hay menos de dos pantallas en el Historial.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `salir()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** termina la ejecución del programa.

## 4. Invariantes
- INV-01: después de cargar usuarios, no hay usuario activo hasta que se
  selecciona uno con seleccionar_usuario(). Las operaciones que requieren
  usuario activo verifican que exista antes de proceder.
- INV-02: el Historial empieza vacío (0 pantallas); tras la primera visita
  tiene exactamente una pantalla; actual() devuelve None si y solo si cantidad()
  es 0.
- INV-03: los datos no persisten entre ejecuciones; se regeneran con la
  semilla fija al iniciar.

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|-----------------------------------------------------------|---------------------------|
| HU-01 CA-01 | Misma semilla produce mismos usuarios en mismo orden | Prueba manual de main.py con semilla 42 |
| HU-01 CA-02 | Se generan al menos 100 usuarios con nombre único | Prueba manual de main.py |
| HU-02 CA-01 | Después de seguir a B, B aparece entre los seguidos de A | main.py opción seguir |
| HU-02 CA-02 | Seguir a alguien que ya sigo no duplica ni lanza error | main.py opción seguir repetido |
| HU-02 CA-03 | Dejar de seguir a quien no sigo devuelve False | main.py opción dejar de seguir |
| HU-02 CA-04 | No se puede seguir a uno mismo | main.py opción seguir a sí mismo |
| HU-03 CA-01 | La publicación más reciente aparece primero | main.py opción publicar y ver feed |
| HU-03 CA-02 | Avanzar y luego retroceder deja en la misma publicación | main.py opción navegar feed |
| HU-03 CA-03 | Retroceder en la primera o avanzar en la última avisa sin cambiar posición | main.py opción navegar feed |
| HU-03 CA-04 | Un feed vacío muestra un mensaje y no lanza error | main.py opción ver feed sin publicaciones |
| HU-05 CA-01 | Buscar un nombre existente devuelve a ese usuario | main.py opción buscar usuario |
| HU-05 CA-02 | Buscar un nombre inexistente devuelve vacío sin error | main.py opción buscar usuario |
| HU-05 CA-03 | Listar usuarios entrega nombres en orden alfabético | main.py opción listar usuarios |
| HU-06 CA-01 | Tras visitar A, B y C, volver lleva a B y luego a A | main.py Historial |
| HU-06 CA-02 | Volver sin pantallas previas avisa sin lanzar error | main.py Historial |
| HU-06 CA-03 | Tras volver y visitar D, volver lleva a B y C ya no es alcanzable | main.py Historial |
| HU-07 CA-01 | Las notificaciones se leen en el orden en que llegaron | main.py opción notificaciones |
| HU-07 CA-02 | Leer con la cola vacía devuelve vacío sin error | main.py opción notificaciones |
| HU-07 CA-03 | Seguir a alguien genera una notificación para esa persona | main.py opción seguir |
| HU-08 CA-01 | Se sugieren personas a exactamente 2 saltos que aún no sigo | main.py opción recomendaciones |
| HU-08 CA-02 | Nunca se sugiere a la propia persona ni a quien ya sigue | main.py opción recomendaciones |
| HU-08 CA-03 | Un usuario sin seguidos recibe una lista vacía | main.py opción recomendaciones |
| HU-04 CA-01 | Comentar en una publicación genera un comentario vinculado a esa publicación | main.py opción comentar |
| HU-04 CA-02 | Mostrar comentarios lista cada comentario después de su padre, con profundidad | main.py opción ver comentarios |
| HU-04 CA-03 | Responder a un comentario inexistente lanza error sin crear respuesta | main.py opción responder |
| HU-07 CA-04 | Comentar en una publicación genera notificación COMENTARIO | main.py opción comentar |
| HU-07 CA-05 | Responder a un comentario genera notificación RESPUESTA | main.py opción responder |
| HU-08 CA-04 | Se pueden explorar publicaciones de todos los usuarios ordenadas por ID global | main.py opción explorar publicaciones |

## 6. Casos extremos considerados
- Sin usuarios cargados: mostrar mensaje y no permitir operaciones que requieran usuario.
- Usuario activo sin publicaciones: feed vacío muestra mensaje.
- Usuario activo sin seguidos: recomendaciones vacías.
- Historial vacío: no hay pantalla actual; visitar agrega la primera.
- Historial con una sola pantalla: volver no está disponible (NadaAtrasError).
- Notificaciones vacías: leer_siguiente() devuelve None sin error.
- Seleccionar usuario inexistente: muestra mensaje, no cambia usuario activo.
- Comentar en publicación inexistente: muestra mensaje de error sin crear comentario.
- Responder a comentario inexistente: muestra mensaje de error sin crear respuesta.
- Publicación sin comentarios: ver comentarios muestra mensaje vacío.
- Sin publicaciones en la red: explorar publicaciones muestra mensaje vacío.

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 12 nov 2026 | Versión inicial | — |
