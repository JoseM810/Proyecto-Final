# Decisión de estructuras — Red social UCC

| Capacidad | Estructura | Operación dominante | Complejidad | Alternativa descartada | Dónde se usa |
|---|---|---|---|---|---|
| Feed de publicaciones | Lista doblemente enlazada | publicar al inicio y moverse ← → | O(1) ambas | Arreglo dinámico: insertar al inicio corre todos los elementos, O(n) | HU-03 |
| Historial de pantallas | Pila enlazada | apilar y desapilar | O(1) ambas | Lista doble con cursor: cortar el "adelante" agrega casos sin ganar costo | HU-06 |
| Notificaciones | Cola enlazada (frente y final) | encolar al final, desencolar al frente | O(1) ambas | Arreglo dinámico: desencolar del inicio es O(n) | HU-07 |
| Índice de usuarios | BST por nombre (luego AVL) | buscar por nombre | O(log n) promedio; O(n) peor caso en BST, O(log n) garantizado en AVL | Tabla hash: busca en O(1) pero no recorre en orden alfabético (CA-03 de HU-05) | HU-05 |
| Hilos de comentarios | Árbol general (cada nodo guarda sus respuestas) | mostrar el hilo (preorden) | O(n) | Lista con id del padre: reconstruir el hilo es O(n²) | HU-04 |
| Relaciones entre usuarios | Grafo dirigido con lista de adyacencia | seguir y consultar seguidos | O(1) y O(grado) | Matriz densa: 100 usuarios son 10 000 celdas casi vacías | HU-02 |
| Recomendaciones | BFS limitado a 2 saltos sobre el mismo grafo | recorrer vecinos de vecinos | O(V + E) | DFS: no garantiza respetar la distancia de 2 saltos | HU-08 |

## Estructuras con soporte interno
Si algún componente usa `list` por dentro (por ejemplo, el arreglo de vértices del
grafo, indexado por id de usuario), se justifica en su plan.md.