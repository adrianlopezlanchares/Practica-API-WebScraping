# Practica-API-WebScraping
Adquisición de Datos: Practica Final

# Funcionamiento
El programa primero extrae datos de la web sobre el equipo de los Boston Celtics mediante una API y mediante técnicas de WebScraping. Estos datos son 
estadísticas del equipo y un pronóstico del próximo partido de los Boston Celtics. Es posible que no haya disponible un pronóstico del próximo partido.

Después, transforma los datos para que sean más fáciles de manejar, mediante una ETL.

Finalmente carga los datos en un reporte en formato PDF, donde se ven gráficas con las estadísticas clave del equipo en la temporada 2022-2023, además de 
la predicción del próximo partido, si se ha podido encontrar una.

Instrucciones de uso:
En la función extraerDatosEquipo(), que hace uso de la API, cambiar el campo de "X-RapidAPI-Key" de la variable 'headers' a su propia clave de la API 
de RapidAPI. Actualmente en ese campo pone "INSERTAR CLAVE"
