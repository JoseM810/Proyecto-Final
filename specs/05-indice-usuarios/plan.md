# Plan técnico — Índice de usuarios
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Árbol binario de búsqueda (BST) ordenado por nombre. Cada nodo guarda un
nombre, su usuario y dos hijos: a la izquierda los nombres menores y a la
derecha los mayores. Buscar y agregar descienden por una sola rama; listar
es un recorrido en orden, que entrega los nombres ya ordenados sin
ordenar nada. Todo se escribe con ciclos y no con recursión.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Tabla hash | Buscar en O(1) | No guarda el orden: listar alfabéticamente exige ordenar, O(n log n) por consulta |
| Arreglo ordenado + búsqueda binaria | Buscar en O(log n) | Agregar corre los elementos: O(n) por usuario, y obliga a usar list como sustituto de la estructura |
| AVL | O(log n) garantizado | Más código (rotaciones). Queda como mejora (Should): como el contrato no cambia, solo se cambia el plan y el código |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| agregar | O(h) | O(1) | Desciende por una rama; h es la altura: O(log n) en promedio, O(n) si los nombres llegan ya ordenados |
| buscar | O(h) | O(1) | Igual que agregar |
| listar | O(n) | O(h) | Visita cada nodo una vez; la pila guarda como máximo una rama |
| cantidad | O(1) | O(1) | Se lleva un contador |

## 4. Diseño interno
- NodoArbol (estructuras/arbol_bst.py): clave, valor, izquierdo, derecho
- ArbolBST (estructuras/arbol_bst.py): raiz y tamanio; insertar devuelve
  True si agregó y False si la clave ya existía; buscar devuelve el valor
  o None; recorrer_en_orden es un generador que entrega las claves usando
  una PilaEnlazada; tamanio
- IndiceUsuarios (dominio/indice_usuarios.py): valida nombre y usuario,
  convierte el False de insertar en NombreDuplicadoError y devuelve None
  si el nombre no es texto
- Excepciones en estructuras/errores.py: EntradaInvalidaError,
  NombreDuplicadoError
- Los usuarios nunca son None, así que None de buscar significa "no existe"
- Invariante de representación: para todo nodo, las claves de su subárbol
  izquierdo son menores y las del derecho mayores; tamanio = nodos
  alcanzables desde la raíz
- No se usa list, dict, set ni heapq

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Insertar nombres ya ordenados degenera el árbol en una lista: O(n) por operación | Medio | Medirlo en ANALISIS.md; el AVL queda como mejora sin tocar la spec (CA-07) |
| Recursión desbordada con un árbol degenerado | Alto | Todo iterativo; CA-07 lo verifica con 2 000 nombres ordenados |
| Insertar una clave duplicada y sobrescribir el usuario | Alto | insertar devuelve False sin tocar el nodo; CA-04 |