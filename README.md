# HOLAAAAAAAAAa

estructuras de datos básicas (arrays, pilas, colas y listas) para modelar operaciones de un sistema hospitalario simple

## Estructuras

- Arrays: gestión y búsqueda de camas en `data_structures/bed_array.py`.
- Pilas (Stacks): seguimiento de acciones (undo/redo) en `data_structures/action_stack.py` y el servicio de deshacer en `services/undo_service.py`.
- Colas (Queues): cola de espera de pacientes en `data_structures/waiting_queue.py` y la lógica de `services/waiting_room_service.py`.
- Listas simples: almacenamiento secuencial de historial en `data_structures/intervention_history.py` y listas de atributos en modelos como `models/patient.py`.

## Como ejercutar

1. Crear un entorno virtual e instalar dependencias:

   pip install -r requirements.txt

2. Ejecutar la aplicación:

   python app.py
