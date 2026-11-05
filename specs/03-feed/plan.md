# Plan técnico — Feed de publicaciones
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Lista doblemente enlazada con referencia a la cabeza y a la posición
actual (cursor). Publicar inserta un nodo al inicio; avanzar y retroceder
mueven el cursor al nodo siguiente o al anterior. Como cada nodo conoce a
sus dos vecinos, moverse en cualquier sentido es O(1).

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Lista simple | Un enlace menos por nodo | Retroceder obliga a recorrer desde la cabeza hasta el nodo previo: O(n) |
| Arreglo dinámico | Acceso por índice, índice actual simple | Publicar al inicio corre todos los elementos: O(n) por publicación |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| publicar | O(1) | O(1) | Enlazar un nodo antes de la cabeza |
| actual | O(1) | O(1) | Leer el nodo del cursor |
| avanzar | O(1) | O(1) | Mover el cursor al siguiente |
| retroceder | O(1) | O(1) | Mover el cursor al anterior |
| cantidad | O(1) | O(1) | Se lleva un contador |

## 4. Diseño interno
- NodoDoble (estructuras/nodo_doble.py): valor, anterior, siguiente
- ListaDoble (estructuras/lista_doble.py): cabeza, actual, tamanio;
  operaciones insertar_al_inicio, actual, avanzar, retroceder, tamanio.
  Insertar deja el cursor en la nueva cabeza.
- Publicacion (dominio/feed.py): texto y fecha
- Feed (dominio/feed.py): valida los datos y usa una ListaDoble
- Excepciones en estructuras/errores.py: PublicacionInvalidaError,
  FinDelFeedError, InicioDelFeedError
- Invariante de representación: cabeza.anterior es None; para todo nodo n
  con n.siguiente != None se cumple n.siguiente.anterior == n; tamanio =
  nodos alcanzables desde la cabeza; actual es None si y solo si
  tamanio es 0
- No se usa list, dict, set ni deque

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Al insertar, olvidar actualizar anterior de la cabeza vieja | Alto | Prueba que avanza y retrocede tras varias inserciones |
| Mover el cursor más allá de los extremos | Medio | Verificar el vecino antes de moverlo; CA-03 |