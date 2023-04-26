2. Una vez tengáis todos los datos de la API, deberéis realizar una serie de procesos de limpieza, estos incluyen:

- Cambiad los nombres de las columnas para homogeneizarlas, tenemos columnas que tienen - y otras _. Unifícalo para que todo vaya con _.

- La columna de domains nos da una información similar a la de web_pages. Eliminad la columna domains.

3. Si exploramos la columna de web_pages, nos daremos cuenta que hay universidades, como por ejemplo la Universidad de "Cégep de Saint-Jérôme" de Canadá que en su columna de web_pages tiene más de un valor dentro de la lista. Esto es poco práctico y puede llegar a no tener sentido. el objetivo de este ejericio es que usando el método explode de pandas separéis cada elemento de la lista en una fila nueva. Aquí tenéis la documentación de este método.
Al final os quedará una tabla similar a la siguiente:

4. Una vez hayáis realizado el explode, chequead si tenéis duplicados basándonos unicamente en el nombre de la universidad, en caso de que si, eliminandlos.

5. Si exploramos la columna de state_province veremos que hay universidades cuyo valor para esta columna es None. Cread una función para reemplazar los None por nulos de numpy.

6. Después del último cambio, os habréis dado cuenta que tenemos muchos valores nulos dentro de la columna de state_province, por lo que nuestro jefe nos pide que reemplacemos esos nulos por "Unknow". No nos piden ningún método especifico, asi que podremos usar el método que queramos.

7. Ahora nuestros jefes nos piden que saquemos las coordenadas de las provincias donde están ubicadas las universidades. Para eso nos piden que usemos la librería de geopy que aprendimos el día del repaso, aquí la documentación. Para desarrollar este ejercicio deberéis:
- Sacar los valores únicos de la columna state_province.
- Algunos de los valores que tenemos están con siglas, y deberéis reemplazarlos por lo siguiente:
    - NV: reemplazalo por Nevada
    - TX: reemplazalo por Texas
    - IN: reemplazalo por Indianapolis
    - CA: reemplazalo por California
    - VA: reemplazalo por Virginia
    - NY: reemplazalo por New York
    - MI: reemplazalo por Michigan
    - GA: reemplazalo por Georgia
    - ND: reemplazalo por North Dakota
- Otros valores que tenemos más formateados son y que deberemos reemplazar:
    - New York, NY. Deberéis reemplazarlo por "New York".
    - 'Buenos Aires', 'Ciudad Autónoma de Buenos Aires'. En este caso deberéis poner en ambos casos "Buenos Aires"
- Una vez realizados los pasos anteriores, crea una lista con los valores únicos de las provincias de las universidades.
- Usando la API de geopy, extraed la latitud y la longitud de cada una de las provincias y almacenad los resultados en un dataframe.
- Una vez que tengáis los datos del ejercicio anterior en un dataframe, unidlo con el de las universidades que hemos sacado de la API.

8. Crea una BBDD en mysql que contenga las siguientes tablas:
- Tabla países: donde encontraremos las siguientes columnas:
    - idestado: primary key, integer, autoincremental
    - nombre_pais: varchar
    - nombre_provincia: varchar
    - latitud: decimal
    - longitud: decimal
- Tabla universidades: donde encontraremos las siguientes columnas:
    - iduniversidades: primary key, integer, autoincremental
    - nombre_universidad: varchar
    - pagina_web: varchar
    - paises_idestado: foreing key

9. Introduce todo el código que habéis ido creando en funciones, siguiendo la misma lógica que hemos seguido en los pairs

10. BONUS
Introduce los datos en la BBDD de SQL.
Crea una clase con todo el código generado en esta evaluación.
