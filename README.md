# API Fumigaciones

Este proyecto es una API REST hecha en **Python (Flask)** para la gestión de servicios de fumigación.  
Ingeniería de Sistemas - Enfasis 1. DevOps. Se despliega en la nube.

## Tecnologías
- Python 3
- Flask
- MySQL / PostgreSQL
- Render (despliegue inicial)
- AWS (Secrets Manager, RDS)



## Entidades principales
- **Consumidores**
- **Técnicos**
- **Administradores**

Despliegue

La API está actualmente en Render:
🔗 https://api-fumigaciones.onrender.com

## Versionado
Se utiliza versionado semántico:  
- **v1.0.0** → Entrega inicial de la API  (src/)
- **v2.0.0** → (Entrega 2) Mejoras, integración con AWS y actualizaciones.   

Historia de Integración de APIs

## Despliegue en AWS (Laura):
http://3.23.103.38/ui/

## Historia oficial:
“Cuando una Orden queda pagada en la tienda, se envía un webhook al conector. El conector crea/actualiza un Consumidor en la API de fumigaciones con los datos básicos del comprador y registra la intención de servicio en un campo libre.”

# Story API

Este servicio implementa un **microservicio puente** entre la API de **Orders** y la API de **Fumigaciones**.  
Dado un `orderId`, consulta la orden en la API de Orders y asegura la creación de un consumidor en la API de Fumigaciones, devolviendo una respuesta unificada con trazabilidad.

---

## Variables de entorno

ORDERS_BASE_URL → http://18.191.171.234:3002/api
FUMI_BASE_URL → http://3.23.103.38/api

## Despliegue en AWS

# Lambda:

Nombre: story_api

Runtime: Python 3.13

Handler: lambda_function.lambda_handler

Timeout: 15 segundos

Memory: 128 MB

# API Gateway (HTTP API):

Route: GET /story/order/{orderId}

Integración: Lambda story_api

Deployment: Stage prod (o el que definas)

# CloudWatch Logs:

Guarda todos los intentos de GET/POST y excepciones.

Muy útil para depurar problemas de path o payload.

## Diagrama

                    +---------------------------+
                    |   Cliente (Postman / UI)  |
                    +-------------+-------------+
                                  |
                                  v
                    +-------------+-------------+
                    |     API Gateway (HTTP)    |
                    +-------------+-------------+
                                  |
                                  v
                    +-------------+-------------+
                    |   AWS Lambda: story_api   |
                    | handler: lambda_function. |
                    |          lambda_handler   |
                    | env: ORDERS_BASE_URL,     |
                    |      FUMI_BASE_URL        |
                    +------+------+-------------+
                           |      \
                           |       \  POST /consumidores
                           |        \
                           |         v
                           |   +-----+------------------+
                           |   |   Fumigaciones API     |
                           |   | http://3.23.103.38/api |
                           |   |   (/consumidores)      |
                           |   +------------------------+
                           |
                           |  GET /orders/{id}
                           v
                    +------+--------------------+
                    |        Orders API         |
                    | http://18.191.171.234:3002|
                    |           /api            |
                    |      (/orders/{id})       |
                    +---------------------------+

                                   |
                                   v
                         +---------+----------+
                         |  Respuesta unificada|
                         +---------------------+

(Logs y métricas: AWS Lambda → CloudWatch Logs)
