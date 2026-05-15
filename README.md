Para Levantar el proyecto
1. Ir a la carpeta del proyecto

Se debe de hacer un cd a la carpeta inventarios

El proyecto está configurado para ejecutarse mediante contenedores de Docker, por lo que es necesario iniciar los servicios antes de usar la aplicación web.

3. Limpiar contenedores y caché (opcional)

Estos comandos eliminan contenedores, volúmenes y caché de compilación anteriores para evitar conflictos:


docker compose down -v
docker builder prune -af


 3. Construir y levantar los servicios

Ejecutar el siguiente comando para construir las imágenes e iniciar la aplicación:

docker compose up --build
4. Acceder a la aplicación

Una vez iniciados los contenedores, la aplicación estará disponible en:

http://localhost:5000

Posdata:
En caso no se clone el archivo .env por medidas de seguridad se debe de crear en la raiz del proyecto osea la carpeta inventarios.
Contenido del .env:
DB_USER=admin
DB_PASSWORD=secret123
DB_NAME=inventario_db
SECRET_KEY=OrfevreCastorieGoldshipDreamJourneySlSuzukaMorganArtoria
FLASK_ENV=development
