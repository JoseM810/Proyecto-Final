# Plan técnico — Red de seguimiento
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Grafo dirigido con lista de adyacencia: cada usuario tiene su propia lista
enlazada con los identificadores de las personas que sigue, con
referencia a su primer y último nodo. Seguir agrega al final de esa lista
si la relación no existe; dejar de seguir quita el nodo. Las recomendaciones
usan una búsqueda en anchura (BFS) limitada a dos saltos, con una
ColaEnlazada para la frontera.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Matriz de adyacencia densa | Saber si A sigue a B en O(1) | Ocupa V² celdas: con 100 usuarios son 10 000, casi todas vacías, y listar los seguidos de A cuesta O(V) en vez de O(grado) |
| Lista de aristas global | Muy simple | Listar los seguidos de A obliga a recorrer todas las relaciones: O(E) |
| DFS para recomendar | Código similar | No respeta la distancia: puede llegar a una persona por un camino largo y no distinguir si está a dos saltos |

## 3. Complejidad esperada
(V usuarios, E relaciones, g = cantidad de personas que sigue el usuario)
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| agregar_usuario | O(1) amortizado | O(1) | Agregar una lista vacía al arreglo de apoyo |
| cantidad_usuarios | O(1) | O(1) | Se lleva un contador |
| seguir | O(g) | O(1) | Se recorre la lista de a para comprobar que no esté ya; el enlace final es O(1) |
| dejar_de_seguir | O(g) | O(1) | Se recorre la lista de a hasta encontrar a b |
| sigue | O(g) | O(1) | Recorrido de la lista de a |
| seguidos | O(g) | O(1) | Recorre la lista de a, entregando de a uno |
| recomendar | O(V + E) | O(V) | Un BFS a dos saltos visita a lo sumo V usuarios y E relaciones; marca visitados con un arreglo de tamaño V |

## 4. Diseño interno
- Reutiliza Nodo (estructuras/nodo.py) y ColaEnlazada (estructuras/cola.py)
- ListaAdyacencia (estructuras/grafo.py): primero, ultimo, tamanio;
  agregar_si_no_existe(id), quitar(id), contiene(id), recorrer
- GrafoDirigido (estructuras/grafo.py): arreglo de apoyo con una
  ListaAdyacencia por usuario; agregar_vertice, agregar_arista,
  quitar_arista, existe_arista, vecinos y cantidad_vertices
- RedSeguimiento (dominio/red.py): valida identificadores, convierte los
  resultados en los errores de la spec y arma las recomendaciones
- Soporte interno con list: se usa para (1) guardar las listas de adyacencia
  indexadas por id, que da acceso al usuario en O(1), y (2) las marcas
  de visitado del BFS. Ninguno sustituye la estructura declarada, que es el
  grafo con sus listas enlazadas. Lo justifico aquí según la regla 4 de la
  constitución.
- Recomendar: a se marca como visitado y sus seguidos directos también;
  se recorre cada seguido de a y, de él, cada uno de sus seguidos; el
  que no está marcado se entrega y se marca. La ColaEnlazada guarda los
  seguidos directos pendientes de expandir
- Excepciones en estructuras/errores.py: UsuarioNoExisteError,
  AutoSeguimientoError
- Invariante de representación: ningún nodo de la lista de a contiene a
  ni repite un identificador; tamanio de cada lista = nodos alcanzables
  desde su primero; la cantidad de listas es la cantidad de usuarios
- No se usa dict, set ni deque

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Al quitar el último nodo de una lista, dejar el puntero al último apuntando a un nodo viejo | Alto | Actualizar ultimo siempre que se quite el último; prueba de seguir de nuevo tras dejar de seguir |
| Recomendar a alguien que ya sigo o a mí mismo | Alto | Marcar a y sus seguidos antes de expandir; CA-10 |
| Aceptar identificadores raros (True, 1.5, negativos) | Medio | Validar el tipo y el rango en un único método; CA-07 |
| Ciclos que hagan repetir recomendaciones | Medio | Marcar a cada candidato al entregarlo; prueba con A sigue a B y B sigue a A |