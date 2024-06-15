# API y Framework WEB de todo list
video: https://drive.google.com/file/d/1_ZXHMMKqRZ5Ei0Ab0qFRuJUFiNXcbFZE/view?usp=sharing 

## Resumen

En este código vamos a crear con Flask una pequeña **plataforma WEB** que a su vez tendrá una **API RESTful** que permitirá:

- Añadir nuestros tareas y usuarios.
- Filtrar por id de tareas y usuarios.
- Modificar tareas y usuarios.
- Eliminar tareas y usuarios.

## Ejemplos de uso de la API

En nuestro caso dispondremos de las siguientes secciones:

- `taskApi`: Esta sección nos permitirá añadir, modificar, eliminar y filtrar tareas.
- `userApi`: Esta sección nos permitirá añadir, modificar, eliminar y filtrar usuarios.

### Usuarios

A continuación, se muestran un ejemplo de uso para los diferentes métodos http. 

- **Obtener el detalle de los usuarios o un usuario concreto:**
    ```bash
    curl http://localhost:5000/userApi o curl http://localhost:5000/userApi/<id>

- **Añadir un nuevo usuario:** Importante, no hay que repetir datos.
    ```bash
    curl -X POST -H "Content-Type: application/json" -d "{\"first_name\": \"NuevoNombre\", \"last_name\": \"NuevoApellido\", \"email\": \"nuevo_correo@example.com\", \"password\": \"nueva_contraseña\"}" http://127.0.0.1:5000/userApi 
    ```
- **Modificar un usuario:** .
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d "{\"first_name\": \"NuevoNombre\", \"last_name\": \"NuevoApellido\", \"email\": \"nuevo_correo@example.com\", \"password\": \"nueva_contraseña\"}" http://127.0.0.1:5000/userApi/<id>
    ```
- **Eliminar un ingreso/gasto ya existente:**
    ```bash
    curl -X DELETE http://127.0.0.1:5000/userApi/<id>
    ```

### Tareas

- **Obtener el detalle de una tarea concreta:**
    ```bash
    curl http://localhost:5000/taskApi o curl http://localhost:5000/taskApi/<id> o
    curl http://localhost:5000/taskApi/all/<completed=[false or true]>
    ```

- **Añadir una Tarea:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d "{\"Task\": \"tarea ejemplo\", \"Description\": \"descripción de la tarea\", \"fecha_inicio\": \"2024-06-15\", \"fecha_fin\": \"2024-06-30\", \"user_id\": 1, \"completed\": true}" http://127.0.0.1:5000/taskApi
    ```

- **Modificar una tarea ya existente:**
    ```bash
    curl -X PUT -H "Content-Type: application/json" -d "{\"Task\": \"tarea ejemplo\", \"Description\": \"descripción de la tarea\", \"fecha_inicio\": \"2024-06-15\", \"fecha_fin\": \"2024-06-30\", \"user_id\": 1, \"completed\": true}" http://
    127.0.0.1:5000/taskApi/14
    ```

- **Eliminar una tarea ya existente:**
    ```bash
    curl -X DELETE http://127.0.0.1:5000/taskApi/<id>
    ```
