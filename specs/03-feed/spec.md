# Especificación — Feed de publicaciones
**Versión:** 1.1 · **Fecha:** 7 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Guarda las publicaciones de una persona de la red y permite recorrerlas
una a una, de la más reciente a la más antigua y de vuelta. Hay un feed
por usuario. Soporta la historia HU-03.

## 2. Fuera de alcance
- Feed combinado con las publicaciones de las personas que sigo
- Editar o borrar publicaciones
- Comentarios (los maneja el componente de hilos)
- Guardar el feed entre ejecuciones

## 3. Operaciones

### `publicar(texto, fecha, id_publicacion=None)`
- **Precondiciones:** texto es un texto no vacío; fecha es un entero >= 0
  (día de la simulación); id_publicacion es un entero >= 0 opcional. Si se
  omite, se asigna automáticamente desde el contador interno del feed.
- **Postcondiciones:** la publicación es la más reciente del feed y pasa
  a ser la posición actual. Cada publicación tiene un identificador entero
  único asignado.
- **Errores:** PublicacionInvalidaError si texto o fecha no cumplen

### `actual()`
- **Postcondiciones:** devuelve la publicación en la posición actual, o
  None si el feed está vacío. No modifica el feed.

### `avanzar()`
- **Precondiciones:** existe una publicación más antigua que la actual
- **Postcondiciones:** la posición actual pasa a la siguiente publicación
  más antigua. La devuelve.
- **Errores:** FinDelFeedError si la actual ya es la más antigua o el feed
  está vacío

### `retroceder()`
- **Precondiciones:** existe una publicación más reciente que la actual
- **Postcondiciones:** la posición actual pasa a la siguiente publicación
  más reciente. La devuelve.
- **Errores:** InicioDelFeedError si la actual ya es la más reciente o el
  feed está vacío

### `buscar(palabra)`
- **Precondiciones:** palabra es un texto no vacío
- **Postcondiciones:** entrega las publicaciones cuyo texto contiene la
  palabra, sin distinguir mayúsculas de minúsculas, de la más reciente a
  la más antigua. No modifica el feed ni la posición actual.
- **Errores:** BusquedaInvalidaError si palabra no es un texto no vacío;
  se lanza al llamar a buscar, no al recorrer los resultados

### `cantidad()`
- **Postcondiciones:** devuelve cuántas publicaciones hay. No modifica nada.

### `obtener_por_id(id_publicacion)`
- **Precondiciones:** id_publicacion es un entero válido
- **Postcondiciones:** devuelve la publicación con ese identificador entero. No modifica el feed.
- **Errores:** PublicacionNoEncontradaError si no existe una publicación con ese ID
- **Complejidad:** Tiempo O(n), espacio O(1), con n la cantidad de publicaciones

## 4. Invariantes
- INV-01: cantidad() >= 0 en todo momento
- INV-02: actual() es None si y solo si cantidad() es 0
- INV-03: cada publicación tiene un identificador entero único asignado por el feed
- INV-04: cada publicación tiene su propio hilo de comentarios asociado

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|----------------------------------------------------------|---------------------------------|
| CA-01 | La publicación más reciente aparece primero: tras publicar A y luego B, actual() es B y avanzar() lleva a A | test_la_mas_reciente_aparece_primero |
| CA-02 | Avanzar y luego retroceder deja en la misma publicación | test_avanzar_y_retroceder |
| CA-03 | Retroceder en la más reciente lanza InicioDelFeedError y avanzar en la más antigua lanza FinDelFeedError; la posición no cambia | test_limites_del_feed |
| CA-04 | Con el feed vacío, actual() devuelve None, cantidad() es 0 y no se lanza error | test_feed_vacio |
| CA-05 | Publicar con texto vacío o fecha inválida lanza PublicacionInvalidaError y no cambia cantidad() | test_publicar_invalida |
| CA-06 | buscar(palabra) entrega solo las publicaciones cuyo texto contiene la palabra, sin distinguir mayúsculas, de la más reciente a la más antigua | test_buscar_por_palabra |
| CA-07 | buscar sin coincidencias, o con el feed vacío, no entrega nada y no lanza error | test_buscar_sin_coincidencias |
| CA-08 | buscar con una palabra vacía o que no es texto lanza BusquedaInvalidaError al llamarla y no cambia nada | test_buscar_palabra_invalida |
| CA-09 | buscar no modifica la posición actual ni cantidad() | test_buscar_no_modifica_el_feed |
| CA-10 | Cada publicación tiene un identificador entero único y consecutivo asignado por el feed | test_ids_secueneciales |
| CA-11 | Cada publicación tiene su propio hilo de comentarios independiente | test_hilo_independiente_por_publicacion |
| CA-12 | Obtener por ID existente devuelve la publicación correcta | test_obtener_por_id_existente |
| CA-13 | Obtener por ID inexistente lanza PublicacionNoEncontradaError | test_obtener_por_id_inexistente |

## 6. Casos extremos considerados
- Feed vacío · una sola publicación · publicar estando en medio del
  recorrido (la nueva pasa a ser la actual) · muchas publicaciones
· búsqueda sin coincidencias · palabra que aparece dentro de otra
· publicación con ID 1 (primera) · ID mayor que la cantidad
· ID inexistente

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 5 nov 2026 | Versión inicial | — |
| 1.1 | 7 nov 2026 | Se agrega buscar(palabra) con CA-06 a CA-09 | HU-05 CA-04 exige buscar publicaciones por palabra y la v1.0 no lo cubría |
| 1.2 | 12 nov 2026 | Cada publicación tiene un ID entero secuencial y su propio HiloComentarios. Agrega obtener_por_id con CA-10 a CA-13 | HU-06 requiere vincular comentarios a publicaciones específicas mediante ID |