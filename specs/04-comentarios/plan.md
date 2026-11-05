# Plan técnico — Hilo de comentarios
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Árbol general en la representación primer-hijo / siguiente-hermano: cada
nodo guarda su primer hijo, su último hijo y su siguiente hermano. Una
raíz virtual (que no es un comentario) tiene como hijos los comentarios de
primer nivel. Responder enlaza el nodo nuevo al final de los hijos del
padre; como se conserva el último hijo, es O(1). Mostrar el hilo es un
recorrido en preorden.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Lista plana con id del padre | Insertar es trivial | Reconstruir el hilo exige buscar los hijos de cada comentario: O(n²) |
| Árbol con un arreglo de hijos por nodo | Acceso directo a cada hijo | Cada nodo carga un arreglo que casi siempre tiene 0 o 1 elementos, y obliga a usar list como sustituto del enlace |
| Recorrido recursivo en lugar de pila | Código más corto | Un hilo con miles de respuestas anidadas desborda la recursión de Python |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| comentar | O(1) | O(1) | Enlazar al final de los hijos de la raíz virtual |
| responder | O(1) | O(1) | Buscar el padre por id en el arreglo de apoyo y enlazar al final |
| obtener | O(1) | O(1) | Leer la posición id del arreglo de apoyo |
| recorrer | O(n) | O(n) | Visita cada nodo una vez; en el peor caso la pila guarda n nodos |
| cantidad | O(1) | O(1) | Se lleva un contador |

## 4. Diseño interno
- NodoComentario (dominio/hilo_comentarios.py): id, autor, texto,
  profundidad, primer_hijo, ultimo_hijo, siguiente_hermano
- HiloComentarios (dominio/hilo_comentarios.py): raíz virtual y un
  arreglo de apoyo indexado por id
- Soporte interno con list: el arreglo de apoyo guarda cada nodo en la
  posición de su id, y no sustituye la estructura declarada, que es el
  árbol. Permite encontrar al padre en O(1) sin recorrer el árbol. Lo
  justifico aquí según la regla 4 de la constitución.
- El identificador de un comentario nuevo es cantidad() + 1. La spec solo
  promete que son enteros positivos únicos, así que esto es decisión del plan.
- recorrer() usa una PilaEnlazada propia para el preorden, sin recursión:
  apila los hermanos pendientes y desciende al primer hijo
- Invariante de representación: el nodo de la posición i del arreglo tiene
  id i; los hijos de un nodo forman una cadena de hermanos que termina en
  su último hijo; profundidad del hijo = profundidad del padre + 1
- Excepciones en estructuras/errores.py: ComentarioInvalidoError,
  ComentarioNoEncontradoError

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Al enlazar el primer hijo de un padre, olvidar actualizar ultimo_hijo | Alto | Prueba de dos respuestas seguidas al mismo padre (CA-04) |
| Preorden con la pila mal ordenada, que invierte las respuestas | Alto | CA-02 y CA-04 comprueban el orden exacto |
| Aceptar como id un valor que no es entero (True, 1.5, texto) | Medio | Validar el tipo antes de indexar; prueba con ids raros |