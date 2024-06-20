# Trabajo de Fin de Grado
## Título: Chat para la resolución de problemas técnicos en la UDC


### Instalación
Para instalar el proyecto, se debe clonar el repositorio y crear un fichero .env en la raíz del proyecto con las siguientes variables de entorno:
```
POSTGRES_USER = "usuario de la base de datos"
POSTGRES_PASSWORD = "contraseña de la base de datos"
SECRET_KEY = "clave privada de Django"
CONFLUENCE_USERNAME = "usuario de Confluence"
CONFLUENCE_PASSWORD = "contraseña de Confluence"
```

### Despliegue

Para desplegar el proyecto, se debe ejecutar los siguientes comandos en la raíz del proyecto:
```
docker compose build
docker compose up
````

A continuación, se debe crear el modelo de datos:
```docker exec -it <id_contenedor_docker> python manage.py migrate --noinput```

Y cargar unos datos iniciales básicos desde la consola:
```
docker exec -it <id_contenedor_docker> python manage.py shell
>>> from chat.models import UserType
>>> user_type = UserType(type='Estudante', active=True)
>>> user_type.save()
>>> user_type = UserType(type='Profesor', active=True)
>>> user_type.save()
>>> user_type = UserType(type='Admin', active=True)
>>> user_type.save()
```
### Uso
Para acceder a la aplicación, se debe abrir un navegador y acceder a la dirección http://localhost:8000/chat/login


