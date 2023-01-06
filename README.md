# XalDigital_Challenge

## RETO 1
Comunicacion con API de stackoverflow y analisis de datos pertinentes utilizando pandas.

Lee desde la API un Json que se procesa con Pandas para poder transformarlo y obtener las respuestas necesarias para el analisis

## RETO 2
Realizar queries para responder una serie de preguntas

Crea la base de datos PostgreSQL en un contenedor de Docker, para realizar las consultas a la base.

### COMANDOS PARA EJECUCION E INICIALIZACION
- make init : Se debe inicializar el proyecto, donde se crea la imagen de Docker, y levanta la base de datos con docker-compose.
- make run : Corre el codigo de ambos retos (Si "make init" no se corrio con anterioridad no se podra conectar a la base de datos el codigo)
- make stop: Para la ejecucion del docker-compose donde esta arriba la base de datos en PostgreSQL
