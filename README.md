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

## Despliegue en AWS:
http://3.23.103.38/ui/

## Historia oficial:
“Cuando una Orden queda pagada en la tienda, se envía un webhook al conector. El conector crea/actualiza un Consumidor en la API de fumigaciones con los datos básicos del comprador y registra la intención de servicio en un campo libre.”


