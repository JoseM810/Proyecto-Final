# Historias de usuario — Red social UCC

## HU-01 · Datos de prueba reproducibles (F-01)
Como docente que evalúa el sistema, quiero que la red arranque con 100 o más
usuarios generados siempre igual, para poder repetir las mismas demostraciones.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Generar con la misma semilla dos veces produce los mismos usuarios, en el mismo orden |
| CA-02 | Se generan al menos 100 usuarios, cada uno con nombre único |

## HU-02 · Seguir y dejar de seguir (F-02)
Como estudiante, quiero seguir a otras personas de la red, para ver lo que publican.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Después de seguir a B, B aparece entre los seguidos de A |
| CA-02 | Seguir a alguien que ya sigo no duplica la relación ni lanza error |
| CA-03 | Dejar de seguir a quien no sigo devuelve False y no cambia nada |
| CA-04 | No se puede seguir a uno mismo (lanza AutoSeguimientoError) |

## HU-03 · Publicar y recorrer mi feed (F-03)
Como estudiante, quiero publicar y ver mis publicaciones avanzando y retrocediendo,
para revisar lo que he compartido.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | La publicación más reciente aparece primero |
| CA-02 | Avanzar y luego retroceder deja en la misma publicación |
| CA-03 | Retroceder en la primera o avanzar en la última no cambia la posición y avisa |
| CA-04 | Un feed vacío muestra un mensaje y no lanza error |

## HU-04 · Comentar y responder en hilos (F-04)
Como estudiante, quiero comentar y responder a otros comentarios, para conversar
sobre una publicación.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Una respuesta queda debajo del comentario al que responde |
| CA-02 | Mostrar el hilo lista cada comentario después de su padre, con sangría según su profundidad |
| CA-03 | Responder a un comentario inexistente lanza ComentarioNoEncontradoError |

## HU-05 · Buscar (F-05)
Como estudiante, quiero buscar personas por nombre y publicaciones por fecha o
palabra, para encontrar lo que me interesa.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Buscar un nombre existente devuelve a ese usuario |
| CA-02 | Buscar un nombre inexistente devuelve vacío y no lanza error |
| CA-03 | Listar usuarios devuelve los nombres en orden alfabético |
| CA-04 | Buscar publicaciones por palabra devuelve solo las que la contienen |

## HU-06 · Volver a la pantalla anterior (F-06)
Como estudiante, quiero volver a la pantalla anterior, para no perderme al navegar.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Tras visitar A, B y C, volver lleva a B y luego a A |
| CA-02 | Volver sin pantallas previas avisa y no lanza error |
| CA-03 | Tras visitar A, B y C, volver (queda en B) y visitar D, volver lleva a B y C ya no es alcanzable |

## HU-07 · Notificaciones (F-07)
Como estudiante, quiero enterarme de nuevos seguidores, comentarios y respuestas,
para reaccionar a tiempo.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Las notificaciones se leen en el orden en que llegaron |
| CA-02 | Leer con la cola vacía devuelve vacío y no lanza error |
| CA-03 | Seguir a alguien, comentarle o responderle genera una notificación para esa persona |

## HU-08 · Personas que quizá conozcas (F-08)
Como estudiante, quiero que me sugieran personas que sigue gente que yo sigo,
para ampliar mi red.
| ID | Criterio de aceptación |
|----|------------------------|
| CA-01 | Se sugieren personas a exactamente 2 saltos que aún no sigo |
| CA-02 | Nunca se sugiere a la propia persona ni a quien ya sigue |
| CA-03 | Un usuario sin seguidos recibe una lista vacía |