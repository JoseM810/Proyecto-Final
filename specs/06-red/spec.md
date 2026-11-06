# Especificación — Red de seguimiento
**Versión:** 1.0 · **Fecha:** 6 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Guarda quién sigue a quién entre los usuarios de la red y sugiere
personas que quizá se conozcan. Cada usuario se identifica con un número
entero que recibe al ser agregado. Soporta las historias HU-02 (seguir y
dejar de seguir) y HU-08 (personas que quizá conozcas).

## 2. Fuera de alcance
- Saber quién sigue a una persona (lista de seguidores)
- Cadena de conexión más corta entre dos personas (A*)
- Relaciones de amistad que requieran aceptación
- Nombres, perfiles y publicaciones de los usuarios
- Guardar la red entre ejecuciones

## 3. Operaciones

### `agregar_usuario()`
- **Postcondiciones:** registra un usuario nuevo sin relaciones y devuelve
  su identificador: el primero es 0 y cada uno siguiente es el anterior más uno

### `cantidad_usuarios()`
- **Postcondiciones:** devuelve cuántos usuarios hay. No modifica nada.

### `seguir(a, b)`
- **Precondiciones:** a y b son identificadores existentes y distintos
- **Postcondiciones:** a sigue a b. Devuelve True si la relación no existía
  y False si ya existía; en ese caso nada cambia.
- **Errores:** UsuarioNoExisteError si a o b no existen (se revisa primero);
  AutoSeguimientoError si a es igual a b

### `dejar_de_seguir(a, b)`
- **Precondiciones:** a y b son identificadores existentes
- **Postcondiciones:** a deja de seguir a b. Devuelve True si la relación
  existía y False si no existía; en ese caso nada cambia.
- **Errores:** UsuarioNoExisteError si a o b no existen

### `sigue(a, b)`
- **Postcondiciones:** devuelve True si a sigue a b. No modifica nada.
- **Errores:** UsuarioNoExisteError si a o b no existen

### `seguidos(a)`
- **Postcondiciones:** entrega los identificadores de las personas que a
  sigue, en el orden en que empezó a seguirlas, sin repetidos. No modifica nada.
- **Errores:** UsuarioNoExisteError si a no existe

### `recomendar(a)`
- **Postcondiciones:** entrega las personas que sigue alguna persona que a
  sigue, y que a no sigue ni es a. Sin repetidos, ordenadas por el
  primer camino en que aparecen: se recorren los seguidos de a en su
  orden y, de cada uno, sus propios seguidos en su orden. No modifica nada.
- **Errores:** UsuarioNoExisteError si a no existe

## 4. Invariantes
- INV-01: cantidad_usuarios() >= 0 en todo momento
- INV-02: nadie se sigue a sí mismo
- INV-03: nadie sigue a la misma persona más de una vez
- INV-04: los identificadores son 0, 1, 2… sin huecos

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|--------------------------------------------------------------|---------------------------------|
| CA-01 | Los identificadores devueltos por agregar_usuario son 0, 1, 2… y cantidad_usuarios() sube en uno cada vez | test_ids_consecutivos |
| CA-02 | Tras seguir(A, B): devuelve True, sigue(A, B) es True y B aparece en seguidos(A) | test_seguir_y_aparece |
| CA-03 | Seguir a quien ya sigo devuelve False, no lo duplica en seguidos y no lanza error | test_seguir_repetido |
| CA-04 | Seguir a uno mismo lanza AutoSeguimientoError y no cambia nada | test_seguir_a_si_mismo |
| CA-05 | La relación tiene dirección: si A sigue a B, sigue(B, A) es False | test_relacion_dirigida |
| CA-06 | Dejar de seguir a quien sigo devuelve True y lo quita sin alterar el orden de los demás; dejar de seguir a quien no sigo devuelve False y no cambia nada | test_dejar_de_seguir |
| CA-07 | Un identificador inexistente (negativo, mayor o igual que la cantidad, booleano o no entero) lanza UsuarioNoExisteError en cada operación que lo recibe, y no cambia nada | test_usuario_inexistente |
| CA-08 | seguidos(A) entrega a quienes A sigue en el orden en que empezó a seguirlos | test_seguidos_en_orden |
| CA-09 | Si A sigue a B y B sigue a C, recomendar(A) entrega C; una persona a tres relaciones de distancia no se recomienda | test_recomendar_a_dos_saltos |
| CA-10 | recomendar(A) nunca entrega a A ni a quienes A ya sigue, ni repite a nadie aunque lo alcance por dos caminos | test_recomendar_sin_repetidos_ni_conocidos |
| CA-11 | recomendar(A) devuelve vacío si A no sigue a nadie o si ninguno de sus seguidos sigue a otra persona, y no lanza error | test_recomendar_sin_candidatos |
| CA-12 | recomendar entrega las personas en el orden descrito en la sección 3 | test_recomendar_orden |

## 6. Casos extremos considerados
- Sin usuarios · un solo usuario · usuario sin relaciones · seguir y dejar
  de seguir varias veces la misma relación · ciclos (A sigue a B y B sigue a A) ·
  dos caminos a la misma persona · muchos usuarios con muchas relaciones

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 6 nov 2026 | Versión inicial | — |