# Especificación — Sistema de Red Social
**Versión:** 1.0 · **Fecha:** 12 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Orquestador que integra IndiceUsuarios, RedSeguimiento y Usuario en una sola
capa. Mantiene la correspondencia entre nombres de usuario, objetos Usuario e
identificadores de vértice en RedSeguimiento. Soporta las historias HU-02
(seguir y dejar de seguir), HU-05 (buscar usuarios), HU-07 (notificaciones al
seguir) y HU-08 (recomendaciones).

## 2. Fuera de alcance
- Autenticación ni contraseñas.
- Guardar la red entre ejecuciones.
- Feed combinado de personas seguidas (cada usuario tiene su propio feed).
- Lista de seguidores (quién me sigue): solo se conoce a quién sigo.
- Comentarios vinculados a publicaciones: esa integración queda para una etapa posterior.

## 3. Operaciones

### `registrar_usuario(username, nombre_visible, biografia="")`
- **Precondiciones:** username es un texto no vacío y no duplicado; nombre_visible es un texto no vacío.
- **Postcondiciones:** asigna un ID entero consecutivo de RedSeguimiento, crea el Usuario, lo indexa por nombre y lo guarda por ID.
- **Errores:** NombreDuplicadoError si el username ya existe (delegado en IndiceUsuarios); EntradaInvalidaError si username no es un texto no vacío o nombre_visible es nulo (delegado en IndiceUsuarios, se revisa primero).
- **Complejidad:** Tiempo O(h), espacio O(1), con h la altura del BST.

### `buscar_usuario_por_nombre(username)`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve el Usuario con ese username exacto, o None si no existe.
- **Complejidad:** Tiempo O(h), espacio O(1).

### `obtener_usuario_por_id(id_usuario)`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve el Usuario con ese ID entero, o None si no existe o está fuera de rango.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `seguir(username_a, username_b)`
- **Precondiciones:** username_a y username_b existen en el índice.
- **Postcondiciones:** username_a empieza a seguir a username_b. Si la relación es nueva, genera una notificación NUEVO_SEGUIDOR para username_b.
- **Errores:** UsuarioNoExisteError si alguno de los usuarios no existe. AutoSeguimientoError si username_a es igual a username_b.
- **Complejidad:** Tiempo O(h + g), espacio O(1), con h la altura del BST y g el grado del usuario en el grafo.

### `dejar_de_seguir(username_a, username_b)`
- **Precondiciones:** username_a y username_b existen en el índice.
- **Postcondiciones:** username_a deja de seguir a username_b. Devuelve True si la relación existía, False si no.
- **Errores:** UsuarioNoExisteError si alguno de los usuarios no existe.
- **Complejidad:** Tiempo O(h + g), espacio O(1).

### `listar_usuarios()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** entrega los nombres de usuario en orden alfabético ascendente.
- **Complejidad:** Tiempo O(n), espacio O(h).

### `cantidad_usuarios()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve cuántos usuarios están registrados.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `cargar_desde_generador(datos_usuarios)`
- **Precondiciones:** datos_usuarios es una lista de tuplas (username, nombre_visible, biografia).
- **Postcondiciones:** registra todos los usuarios. Valida duplicados antes de registrar cualquiera, evitando carga parcial.
- **Errores:** NombreDuplicadoError si hay nombres duplicados en los datos.
- **Complejidad:** Tiempo O(n·h), espacio O(n).

### `obtener_todas_publicaciones()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve una lista con todas las publicaciones de todos los usuarios,
  ordenadas por ID global descendente (más reciente primero). Cada publicación incluye
  su ID global, autor y texto.
- **Complejidad:** Tiempo O(n·m log m) donde n es la cantidad de usuarios y
  m la cantidad de publicaciones por feed, espacio O(m·n).

## 4. Invariantes
- INV-01: el id de cada Usuario coincide con su vértice en RedSeguimiento.
- INV-02: los IDs son consecutivos desde 0 sin huecos.
- INV-03: no hay dos usuarios con el mismo username.
- INV-04: una notificación NUEVO_SEGUIDOR solo se genera la primera vez que se sigue una relación.

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|-----------------------------------------------------------|---------------------------|
| CA-01 | Registrar un usuario lo indexa y le asigna ID consecutivo | test_registrar_usuario, test_registrar_varios_usuarios_ids_consecutivos |
| CA-02 | Buscar por nombre existente devuelve el usuario; inexistente devuelve None | test_buscar_usuario_por_nombre, test_buscar_usuario_inexistente_devuelve_none |
| CA-03 | Seguir genera notificación una sola vez; usuario inexistente lanza error | test_seguir_usuario_genera_notificacion, test_seguir_repetido_no_genera_notificacion_duplicada, test_seguir_usuario_inexistente_lanza_error |

## 6. Casos extremos considerados
- obtener_usuario_por_id con ID negativo devuelve None.
- obtener_usuario_por_id con ID fuera de rango devuelve None.
- Seguir repetido no duplica notificaciones.
- Seguir a sí mismo lanza AutoSeguimientoError y no modifica el grafo.
- Cargar con nombres duplicados lanza NombreDuplicadoError sin carga parcial.

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 12 nov 2026 | Versión inicial | — |
