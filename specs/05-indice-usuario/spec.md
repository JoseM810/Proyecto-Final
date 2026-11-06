# Especificación — Índice de usuarios
**Versión:** 1.0 · **Fecha:** 6 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Guarda los usuarios de la red identificados por su nombre y permite
encontrar uno por su nombre exacto y listar todos los nombres en orden
alfabético. Soporta las historias HU-05 (buscar usuarios) y HU-01 (nombres
únicos).

## 2. Fuera de alcance
- Búsqueda por prefijo o por coincidencia parcial
- Búsqueda de publicaciones (la ofrece el feed)
- Borrar o renombrar usuarios
- Ignorar mayúsculas: "Ana" y "ana" son nombres distintos
- Guardar el índice entre ejecuciones

## 3. Operaciones

### `agregar(nombre, usuario)`
- **Precondiciones:** nombre es un texto no vacío; usuario no es nulo;
  no existe otro usuario con ese nombre
- **Postcondiciones:** el usuario queda registrado con ese nombre y
  cantidad() sube en uno
- **Errores:** EntradaInvalidaError si nombre no es un texto no vacío o
  usuario es nulo (se revisa primero); NombreDuplicadoError si el nombre
  ya existe, y en ese caso el usuario anterior no cambia

### `buscar(nombre)`
- **Postcondiciones:** devuelve el usuario registrado con ese nombre
  exacto, o None si no existe. Un nombre que no es texto devuelve None.
  No modifica el índice ni lanza error.

### `listar()`
- **Postcondiciones:** entrega los nombres registrados en orden
  alfabético ascendente (comparación de textos de Python: las mayúsculas
  van antes que las minúsculas). No modifica el índice.

### `cantidad()`
- **Postcondiciones:** devuelve cuántos usuarios hay registrados.

## 4. Invariantes
- INV-01: cantidad() >= 0 en todo momento
- INV-02: no hay dos usuarios registrados con el mismo nombre
- INV-03: listar() entrega los nombres en orden estrictamente ascendente

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|--------------------------------------------------------------|-----------------------------------|
| CA-01 | Buscar un nombre registrado devuelve ese usuario | test_buscar_existente |
| CA-02 | Buscar un nombre inexistente devuelve None y no lanza error, también con el índice vacío | test_buscar_inexistente |
| CA-03 | listar() entrega los nombres en orden alfabético sin importar el orden en que se agregaron | test_listar_en_orden |
| CA-04 | Agregar un nombre ya existente lanza NombreDuplicadoError, no cambia cantidad() y conserva el usuario original | test_agregar_duplicado |
| CA-05 | Agregar con nombre vacío o no texto, o con usuario nulo, lanza EntradaInvalidaError y no cambia cantidad() | test_agregar_invalido |
| CA-06 | Un índice vacío tiene cantidad() 0 y listar() no entrega nada ni lanza error | test_indice_vacio |
| CA-07 | Con 2 000 nombres agregados ya ordenados, buscar sigue encontrando el primero, uno del medio y el último, y listar() los entrega todos | test_nombres_ya_ordenados |

## 6. Casos extremos considerados
- Índice vacío · un solo usuario · nombres agregados ya ordenados o en
  orden inverso · nombres con mayúsculas y minúsculas · nombre con
  espacios o tildes · nombre que no es texto

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 6 nov 2026 | Versión inicial | — |