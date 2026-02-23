# Staff de cocina - Gestión de Inventario

Esta es una aplicación Full Stack diseñada para gestionar el stock de un bar de forma eficiente. El sistema detecta automáticamente qué productos están bajo el nivel crítico y genera una lista de pedidos pendientes.

## Tecnologías utilizadas

* **Backend:** FastAPI (Python 3.11) + SQLAlchemy
* **Frontend:** Vue 3 (Vite)
* **Base de Datos:** PostgreSQL 15
* **Contenedores:** Docker & Docker Compose

## Requisitos previos

Antes de empezar, asegúrate de tener instalado:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/)

## Instalación y Despliegue

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/nsanchezcastro/bar_app.git](https://github.com/nsanchezcastro/bar_app.git)
    cd bar_app
    ```

2.  **Levanta la infraestructura con Docker:**
    ```bash
    docker-compose up --build
    ```

3.  **Accede a la aplicación:**
    * **Frontend:** [http://localhost:5173](http://localhost:5173)
    * **API Documentation (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Estructura del Proyecto

* `/backend`: API construida con FastAPI y conexión a base de datos.
* `/frontend`: Interfaz de usuario construida con Vue.js.
* `docker-compose.yml`: Configuración de los contenedores de base de datos, backend y frontend.

## Funcionalidades actuales

* Listado automático de productos con stock bajo el mínimo.
* Actualización dinámica de inventario al recibir pedidos.
* Base de datos persistente con PostgreSQL.

---
Desarrollado por [nsanchezcastro](https://github.com/nsanchezcastro)
