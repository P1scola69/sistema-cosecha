 Sistema de Gestión de Cosechas (CosechaWebb)
Este proyecto es una solución integral para el control de pesajes y gestión de fundos agrícolas. Utiliza una arquitectura moderna basada en contenedores Docker y despliegue en la nube de Amazon Web Services (AWS).

 1 Arquitectura del Sistema
El sistema se diseñó bajo una arquitectura distribuida para asegurar la seguridad y la persistencia de los datos:

Backend: Desarrollado en Python 3.12 con el framework Django. Maneja la lógica de negocio y el Dashboard de visualización.

Contenedorización: Se utiliza Docker para empaquetar la aplicación y sus dependencias, garantizando que el sistema funcione igual en cualquier entorno.

Base de Datos: Se utiliza Amazon RDS (MySQL) como motor gestionado, permitiendo que los datos vivan de forma independiente al servidor de aplicaciones.

Servidor de Aplicación: Instancia Amazon EC2 (Ubuntu) que aloja el contenedor de la aplicación.

Seguridad: Implementación de Security Groups para restringir accesos y uso de variables de entorno (.env) para proteger credenciales sensibles.

2 Instrucciones de Despliegue
Requisitos Previos
Instancia EC2 con Docker instalado.

Acceso a la consola de AWS para configurar el Security Group (puertos 8000 y 3306).

Pasos para el Despliegue
Clonar el repositorio:

Bash
git clone https://github.com/P1scola69/sistema-cosecha.git
cd sistema-cosecha
Configurar Variables de Entorno:
Por seguridad, se debe crear un archivo .env en la raíz (este archivo está ignorado en Git):

Bash
nano .env
Pegar los datos de conexión de la base de datos RDS y la Secret Key de Django.

Construir la imagen de Docker:

Bash
sudo docker build -t sistema-cosecha .
Lanzar el contenedor:

Bash
sudo docker run -d -p 8000:8000 --name app-cosecha sistema-cosecha
Ejecutar Migraciones:

Bash
sudo docker exec app-cosecha python manage.py migrate
 3 Planes de Contingencia y Continuidad
Plan de Recuperación ante Desastres (DRP)
Falla de Servidor: Ante una caída de la EC2, el sistema puede ser restaurado en menos de 15 minutos redesplegando el contenedor desde GitHub.

Respaldos: Se utilizan Snapshots automáticos de Amazon RDS, lo que permite restaurar la base de datos a un punto específico en el tiempo si ocurre una pérdida de datos.

Plan de Continuidad del Negocio (BCP)
Operación Manual: Si el sistema web no está disponible por problemas de conectividad en el fundo, se activa el registro en Planillas de Papel. Una vez restablecido el servicio, se realiza la carga masiva de los datos.

Mitigación: La separación de la base de datos (RDS) de la aplicación (EC2) garantiza que una falla en el servidor web no afecte la integridad de la información histórica de las cosechas.

 Tecnologías Utilizadas
Lenguaje: Python 3.12 / Django

Base de Datos: MySQL (Amazon RDS)

Infraestructura: AWS (EC2, VPC, Security Groups)

DevOps: Docker, Git/GitHub