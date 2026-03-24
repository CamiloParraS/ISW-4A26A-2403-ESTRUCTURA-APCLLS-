# Sistema de gestión (Estructuras de datos) - Breve README

## Descripción

Proyecto de ejemplo que usa estructuras de datos básicas (arrays, pilas, colas y listas) para modelar operaciones de un sistema hospitalario simple.

## Estructura relevante

- `data_structures/bed_array.py`: manejo de camas usando un arreglo (Array).
- `data_structures/action_stack.py`: pila (Stack) para historial de acciones y deshacer/rehacer.
- `data_structures/waiting_queue.py`: cola (Queue) para la sala de espera.
- `data_structures/intervention_history.py`: listas simples para historial de intervenciones.

## Dónde se usan las estructuras

- Arrays: gestión y búsqueda de camas en `data_structures/bed_array.py`.
- Pilas (Stacks): seguimiento de acciones (undo/redo) en `data_structures/action_stack.py` y el servicio de deshacer en `services/undo_service.py`.
- Colas (Queues): cola de espera de pacientes en `data_structures/waiting_queue.py` y la lógica de `services/waiting_room_service.py`.
- Listas simples: almacenamiento secuencial de historial en `data_structures/intervention_history.py` y listas de atributos en modelos como `models/patient.py`.

## Cómo ejecutar (rápido)

1. Crear un entorno virtual e instalar dependencias:

   pip install -r requirements.txt

2. Ejecutar la aplicación:

   python app.py

## Contacto

Si quieres que adapte el README (más detalle, diagramas o instrucciones de tests), dime qué prefieres.
