# Especificación — Feed de publicaciones
**Versión:** 1.0 · **Fecha:** 5 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

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

### `publicar(texto, fecha)`
- **Precondiciones:** texto es un texto no vacío; fecha es un entero >= 0
  (día de la simulación)
- **Postcondiciones:** la publicación es la más reciente del feed y pasa
  a ser la posición actual
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

### `cantidad()`
- **Postcondiciones:** devuelve cuántas publicaciones hay. No modifica nada.

## 4. Invariantes
- INV-01: cantidad() >= 0 en todo momento
- INV-02: actual() es None si y solo si cantidad() es 0

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|----------------------------------------------------------|---------------------------------|
| CA-01 | La publicación más reciente aparece primero: tras publicar A y luego B, actual() es B y avanzar() lleva a A | test_la_mas_reciente_aparece_primero |
| CA-02 | Avanzar y luego retroceder deja en la misma publicación | test_avanzar_y_retroceder |
| CA-03 | Retroceder en la más reciente lanza InicioDelFeedError y avanzar en la más antigua lanza FinDelFeedError; la posición no cambia | test_limites_del_feed |
| CA-04 | Con el feed vacío, actual() devuelve None, cantidad() es 0 y no se lanza error | test_feed_vacio |
| CA-05 | Publicar con texto vacío o fecha inválida lanza PublicacionInvalidaError y no cambia cantidad() | test_publicar_invalida |

## 6. Casos extremos considerados
- Feed vacío · una sola publicación · publicar estando en medio del
  recorrido (la nueva pasa a ser la actual) · muchas publicaciones

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 5 nov 2026 | Versión inicial | — |