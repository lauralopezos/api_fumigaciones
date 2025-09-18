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

## 🚀 Arquitectura

```mermaid
flowchart LR
    subgraph Client["Cliente (Postman / Frontend)"]
        CGET["GET /story/order/{orderId}?email=..."]
    end

    CGET --> AGW["API Gateway (HTTP API)"]
    AGW --> LBD["AWS Lambda (story_api)\nHandler: lambda_function.lambda_handler\nEnv: ORDERS_BASE_URL, FUMI_BASE_URL"]
    
    LBD -->|GET /orders/{id}| ORDERS["Orders API\n(http://18.191.171.234:3002/api)"]
    LBD -->|POST /consumidores| FUMI["Fumigaciones API\n(http://3.23.103.38/api)"]

    LBD --> CW["Amazon CloudWatch Logs"]
    LBD -->|JSON Unificado| AGW --> CGET

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

[Cliente (Postman/Frontend)]
            |
            v
   +--------------------------+
   |  API Gateway (HTTP API) |
   +-----------+--------------+
               |
               v
     +----------------------+
     |  AWS Lambda          |
     |  function: story_api |
     |  handler:            |
     |  lambda_function.    |
     |  lambda_handler      |
     +----+-----------+-----+
          |           |
   GET /orders/{id}   |   POST /consumidores
          |           |
          v           v
+----------------+  +----------------------+
|  Orders API    |  | Fumigaciones API     |
| http://18...   |  | http://3.23.../api   |
|  /api          |  |  /consumidores       |
+----------------+  +----------------------+
          \           /
           \         /
            v       v
         +-------------+
         |  Respuesta  |
         |  unificada  |
         +-------------+

(Logs y métricas en Amazon CloudWatch)
