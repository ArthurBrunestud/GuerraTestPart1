# Sistema de Gestión de Inventario

Módulo web de gestión interna de inventario desarrollado con Flask y PostgreSQL,
desplegado mediante Docker Compose.

## Requisitos previos

- Docker Desktop instalado y corriendo
- Git para clonar el repositorio
- Puerto 5000 y 5432 disponibles en la máquina

## Pasos para levantar el proyecto

### 1. Clonar el repositorio

git clone <url-del-repositorio>
cd inventarios

### 2. Crear el archivo .env(opcional)

Crear un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

DB_USER=admin
DB_PASSWORD=secret123
DB_NAME=inventario_db
SECRET_KEY=OrfevreCastorieGoldshipDreamJourneySlSuzukaMorganArtoria
FLASK_ENV=development

Esto es en caso no se halla clonado del .env.
### 3. Limpiar contenedores anteriores (opcional)

Ejecutar solo si hubo una ejecución previa y se quiere partir desde cero:

docker compose down -v
docker builder prune -af

### 4. Construir y levantar los servicios

docker compose up --build

### 5. Acceder a la aplicación

http://localhost:5000

## Credenciales de acceso

| Campo      | Valor       |
|------------|-------------|
| DNI        | 71376979    |
| Contraseña | Oskitar69   |

El usuario está precargado en la base de datos mediante el script `init.sql`.
La contraseña se almacena hasheada internamente, estas credenciales son
solo para facilitar la evaluación del proyecto.


## Notas

- La base de datos se inicializa automáticamente con las tablas y el usuario
  de prueba la primera vez que se levanta el contenedor.
- Las imágenes de productos se almacenan en `app/static/uploads/` y persisten
  entre reinicios gracias al volumen de Docker.
- El sistema está diseñado para uso en red local, no requiere conexión a internet.
