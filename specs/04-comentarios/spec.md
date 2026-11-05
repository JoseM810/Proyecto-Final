# Especificación — Hilo de comentarios
**Versión:** 1.0 · **Fecha:** 5 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Guarda los comentarios de una publicación y las respuestas a cada uno,
que a su vez pueden recibir respuestas. Hay un hilo por publicación.
Permite mostrar la conversación completa en orden. Soporta la historia HU-04.

## 2. Fuera de alcance
- Editar o borrar comentarios
- Generar notificaciones (lo hace el dominio al comentar o responder)
- Votos, reacciones o moderación
- Guardar el hilo entre ejecuciones

## 3. Operaciones

### `comentar(autor, texto)`
- **Precondiciones:** autor y texto son textos no vacíos
- **Postcondiciones:** crea un comentario de primer nivel (profundidad 0),
  posterior a los comentarios de primer nivel anteriores. Devuelve su
  identificador, un entero positivo único dentro del hilo.
- **Errores:** ComentarioInvalidoError si autor o texto no cumplen

### `responder(id_padre, autor, texto)`
- **Precondiciones:** autor y texto son textos no vacíos; existe un
  comentario con identificador id_padre
- **Postcondiciones:** crea un comentario con profundidad igual a la del
  padre más uno, posterior a las demás respuestas de ese padre. Devuelve
  su identificador.
- **Errores:** ComentarioInvalidoError si autor o texto no cumplen (se
  revisa primero); ComentarioNoEncontradoError si id_padre no existe

### `obtener(id_comentario)`
- **Postcondiciones:** devuelve el comentario (autor, texto y profundidad).
  No modifica el hilo.
- **Errores:** ComentarioNoEncontradoError si no existe

### `recorrer()`
- **Postcondiciones:** devuelve todos los comentarios, cada uno con su
  profundidad, de forma que cada comentario aparece después de su padre y
  antes de los comentarios que no descienden de él. No modifica el hilo.

### `cantidad()`
- **Postcondiciones:** devuelve cuántos comentarios hay (respuestas incluidas).

## 4. Invariantes
- INV-01: cantidad() >= 0 en todo momento
- INV-02: no hay dos comentarios con el mismo identificador
- INV-03: en recorrer(), todo comentario con padre aparece después de su padre

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|--------------------------------------------------------------|-------------------------------------|
| CA-01 | Una respuesta queda debajo del comentario al que responde: tiene profundidad del padre + 1 y aparece justo después de él | test_respuesta_queda_bajo_padre |
| CA-02 | recorrer() lista cada comentario después de su padre, con su profundidad: con A, su respuesta B, la respuesta C a B y el comentario D, el orden es A(0), B(1), C(2), D(0) | test_hilo_en_preorden |
| CA-03 | Responder a un comentario inexistente lanza ComentarioNoEncontradoError y no cambia cantidad() | test_responder_inexistente |
| CA-04 | Las respuestas a un mismo comentario aparecen en el orden en que llegaron | test_respuestas_en_orden_de_llegada |
| CA-05 | Comentar o responder con autor o texto vacío lanza ComentarioInvalidoError y no cambia cantidad() | test_comentario_invalido |
| CA-06 | Un hilo sin comentarios tiene cantidad() 0 y recorrer() no devuelve nada ni lanza error | test_hilo_vacio |
| CA-07 | obtener devuelve autor y texto del comentario pedido; con un id inexistente lanza ComentarioNoEncontradoError | test_obtener_comentario |

## 6. Casos extremos considerados
- Hilo vacío · un solo comentario · responder a una respuesta · cadena
  profunda de respuestas · muchos comentarios de primer nivel · id cero,
  negativo o que no es entero

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 5 nov 2026 | Versión inicial | — |