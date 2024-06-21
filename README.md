# Proyecto de Gestión de Inventarios

## Introducción
Este proyecto es una API para la gestión de inventarios que permite ver productos, actualizar el stock, agregar productos y realizar órdenes. Está construido utilizando Docker y Makefile para facilitar la configuración y gestión del backend.

## Tabla de Contenidos
- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
- [Documentación](#documentación)
- [Tests](#tests)
- [Notas](#notas)

## Instalación
Para instalar y configurar el proyecto, asegúrate de tener `make` y Docker instalados en tu computadora.

1. Clona el repositorio y accede a la carpeta del proyecto:
    ```bash
    git clone https://github.com/ceedeliz117/bbb.git
    ```

2. Configura y levanta el backend:
    ```bash
    make setup-backend
    ```

## Uso
### Endpoints de la API
- **Obtener productos**
    - **GET** `http://localhost:8000/api/products`
    - Retorna la lista de productos disponibles.

- **Actualizar el stock de un producto**
    - **PUT** `http://localhost:8000/api/inventories/product/<product_id>`
    - Payload:
        ```json
        {
            "stock": 50
        }
        ```

- **Agregar un nuevo producto**
    - **POST** `http://localhost:8000/api/products`
    - Payload:
        ```json
        {
            "sku": "SKU12345",
            "name": "Test Product"
        }
        ```

- **Realizar una orden**
    - **POST** `http://localhost:8000/api/orders`
    - Payload:
        ```json
        {
            "product": "<product-id>", 
            "quantity": 10
        }
        ```

    
    - Nota: Al realizar una orden, se restará la cantidad correspondiente del stock.

### Documentación
La documentación completa de la API está disponible en:
- [Documentación Swagger](http://localhost:8000/swagger/)

### Tests
Para ejecutar los tests, usa el siguiente comando:
```bash
make test

