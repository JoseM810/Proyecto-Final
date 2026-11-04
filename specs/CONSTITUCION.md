# Constitución del proyecto — Red académica UCC
**Autor:** Jose Miguel Alvarez Ortega · **Temática:** B

## Principios
1. Toda estructura de datos que elegí se implementa desde cero. No uso list,
   dict, set, deque ni heapq como sustituto de esa estructura; si los uso
   como soporte interno, lo justifico en el plan.md.
2. Ninguna operación pública está terminada sin docstring con su complejidad
   declarada y pruebas del caso normal y de los casos extremos
   (vacío, un elemento, elemento inexistente).
3. La especificación precede al código. Si cambia el comportamiento,
   primero cambia el spec.md, en su propio commit, con una línea en su
   historial de cambios.
4. Cada prueba nombra en su docstring el criterio de aceptación (CA-xx)
   que verifica.

## Restricciones
- Lenguaje: Python 3.11 o superior
- Dependencias permitidas: pytest y, opcionalmente, matplotlib
- Interfaz: consola. Debe ejecutarse en una máquina limpia siguiendo el README
- Datos: 100 usuarios o más, generados con semilla fija

## Definición de terminado
Una funcionalidad está terminada cuando:
- [ ] Todos sus criterios de aceptación tienen prueba y pasan
- [ ] La complejidad real coincide con la declarada en el plan
- [ ] Revisé el código contra la spec antes de integrarlo
- [ ] spec.md, plan.md y tasks.md reflejan el estado real

## Uso de asistentes de IA
Permitido para: entender conceptos, depurar y revisar mi código contra la spec.
No permitido para: entregar código que no pueda explicar línea por línea.
Todo uso se declara en BITACORA.md y en el informe final.