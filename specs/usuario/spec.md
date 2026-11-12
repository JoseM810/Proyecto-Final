# Especificación — Entidad Usuario
**Versión:** 1.0 · **Fecha:** 12 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Agrupa la identidad de un usuario de la red con su feed de publicaciones y su
bandeja de notificaciones propios. Cada usuario tiene un identificador entero
que coincide con su vértice en RedSeguimiento. Soporta las historias HU-03
(publicar y recorrer mi feed) y HU-07 (notificaciones).

## 2. Fuera de alcance
- Autenticación ni contraseñas: no existe login ni sesión.
- Guardar el usuario entre ejecuciones: los datos se regeneran con la semilla.
- Nombres de seguidores: el usuario conoce a quién sigue, no quién lo sigue.
- Relacionar el usuario con publicaciones de otros usuarios: solo su propio feed.

## 3. Atributos
| Atributo | Tipo | Descripción |
|---|---|---|
| id | int | Identificador entero. Coincide con su vértice en RedSeguimiento. |
| username | str | Nombre de usuario único. Clave en IndiceUsuarios. |
| nombre_visible | str | Nombre visible mostrado en el perfil. |
| biografia | str | Texto biográfico del usuario (vacío por defecto). |
| feed | Feed | Feed de publicaciones del usuario. |
| bandeja | BandejaNotificaciones | Bandeja de notificaciones del usuario. |

## 4. Operaciones

### `__init__(id_usuario, username, nombre_visible, biografia="")`
- **Precondiciones esperadas:** id_usuario es un entero >= 0; username y nombre_visible son textos no vacíos; biografia es un texto.
- **Validaciones implementadas:** el constructor no valida ninguna precondición; asigna los atributos directamente. Las validaciones de texto no vacío y entero >= 0 no están codificadas.
- **Postcondiciones:** crea un usuario con feed y bandeja vacíos.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `publicar(texto, fecha)`
- **Precondiciones:** texto es un texto no vacío; fecha es un entero >= 0.
- **Postcondiciones:** la publicación se agrega al feed propio como la más reciente.
- **Errores:** PublicacionInvalidaError si texto o fecha no cumplen (delegado en Feed).
- **Complejidad:** Tiempo O(1), espacio O(1).

### `agregar_notificacion(tipo, origen)`
- **Precondiciones:** tipo es NUEVO_SEGUIDOR, COMENTARIO o RESPUESTA; origen es un texto no vacío.
- **Postcondiciones:** la notificación queda pendiente en la bandeja propia.
- **Errores:** NotificacionInvalidaError si tipo u origen no cumplen (delegado en BandejaNotificaciones).
- **Complejidad:** Tiempo O(1), espacio O(1).

### `cantidad_notificaciones()`
- **Precondiciones:** ninguna.
- **Postcondiciones:** devuelve cuántas notificaciones están pendientes. No modifica nada.
- **Complejidad:** Tiempo O(1), espacio O(1).

## 5. Invariantes
- INV-01: el feed y la bandeja se inicializan vacíos al crear el usuario.
- INV-02: el id coincide con el vértice del usuario en RedSeguimiento.

## 6. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|-----------------------------------------------------------|---------------------------|
| CA-01 | El usuario guarda id, username, nombre_visible y biografía | test_usuario_tiene_id_y_campos |
| CA-02 | Un usuario nuevo tiene su feed con cantidad 0 | test_usuario_tiene_feed_vacio_inicialmente |
| CA-03 | Un usuario nuevo tiene su bandeja con 0 pendientes | test_usuario_tiene_bandeja_vacia_inicialmente |

## 7. Casos extremos considerados
- Biografía vacía por defecto si no se indica al crear.
- Publicar y agregar notificaciones son operaciones independientes entre sí.

## 8. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 12 nov 2026 | Versión inicial | — |
