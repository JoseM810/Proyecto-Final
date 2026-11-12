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
| buscar | O(n·m) | O(1) | Recorre las n publicaciones una vez y compara cada texto de longitud m con la palabra |
| obtener_por_id | O(n) | O(1) | Recorre las n publicaciones una vez comparando el ID |

## 4. Diseño interno
- NodoDoble (estructuras/nodo_doble.py): valor, anterior, siguiente
- ListaDoble (estructuras/lista_doble.py): cabeza, actual, tamanio;
  operaciones insertar_al_inicio, actual, avanzar, retroceder, tamanio.
  Insertar deja el cursor en la nueva cabeza.
- Publicacion (dominio/feed.py): id, texto, fecha, hilo (HiloComentarios)
- Feed (dominio/feed.py): _lista (ListaDoble), _siguiente_id (contador entero)
  - Insertar deja el cursor en la nueva cabeza. Si se proporciona id_publicacion,
    se usa ese valor en lugar del contador interno.
- HiloComentarios (dominio/hilo_comentarios.py): árbol general de comentarios por publicación
- Excepciones en estructuras/errores.py: PublicacionInvalidaError,
  FinDelFeedError, InicioDelFeedError, BusquedaInvalidaError,
  PublicacionNoEncontradaError
- Invariante de representación: cabeza.anterior es None; para todo nodo n
  con n.siguiente != None se cumple n.siguiente.anterior == n; tamanio =
  nodos alcanzables desde la cabeza; actual es None si y solo si
  tamanio es 0; cada Publicacion tiene un ID único y su propio HiloComentarios
- No se usa list, dict, set ni deque
- ListaDoble.recorrer: generador de la cabeza a la cola que no mueve el
  cursor; Feed.buscar lo usa y entrega las publicaciones que contienen la
  palabra (comparando en minúsculas). Feed.buscar valida la palabra y
  devuelve un generador interno, para que el error se lance al llamarlo.
- Excepción nueva en estructuras/errores.py: BusquedaInvalidaError,
  PublicacionNoEncontradaError

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Al insertar, olvidar actualizar anterior de la cabeza vieja | Alto | Prueba que avanza y retrocede tras varias inserciones |
| Mover el cursor más allá de los extremos | Medio | Verificar el vecino antes de moverlo; CA-03 |
| Olvidar asignar ID o hilo a una nueva publicación | Medio | Prueba que cada publicación tiene ID único y hilo independiente |