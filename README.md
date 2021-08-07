
# Multimedia-Data-Base
literalmente el tercer proyecto de bede-II

## Integrantes

- Esteban Villacorta  201910336
- Jean Paul Huby Tuesta 201910194
- Daniela Abril Vento Bustamante 201910331

## Descripción

El objetivo del proyecto será la implementación de un buscador de imágenes usando la estructura de R-tree. La colección de imágenes usadas fueron sacadas de    [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) : una colección de mas de 13 mil imágenes para propósitos de desarrollo de software.

Para la búsqueda de estas imágenes se debe hacer uso las funciones knn  y búsqueda por rango para el R-tree.


# Construcción del índice R-tree



## Encoding de imagen

Para poder hacer uso de una imagen en un Rtree necesitamos representarla como un punto en un espacio de K dimensiones. Por lo que tenemos que procesar la imagen de alguna manera para obtener un vector. Este vector obtener será el vector característico de la imagen. 

Obtenemos este vector usando la librería `face_recognition` la cual procesa unan imagen para devolver un vector de de tamaño 128. 

Sin embargo todo este proceso es bastante lento como para ser calculado en run-time cada vez que se corra el código. Por lo que se hace todo el peso de este calculo en una etapa de preprocesamiento.



## Preprocesamiento

Antes de crear el ]index del R-tree primero debemos calcular los vectores característicos de la imagen. Lo cual es una operación pesada considerando que se tiene que hacer para 13 mil imágenes. Por lo hace necesario esta etapa de preprocesamiento.

El procesamiento simplemente se calcula los vectores característicos de la imagen. Estos luego son guardados para luego ser escritos en un archivo csv. Este proceso puede durar hasta `1 hora`. 

Sin embargo la ventajas de no solo una lectura de un csv comparado con encodear las imágenes es abismal. Siendo necesario si queremos hacer el proceso aceptablemente rápido.



## Construcción del índice

La manera de como construimos el índice es indicando el numero de imágenes que se insertan deben insertar.

Para reducir la maldición de la dimensionalidad aplicamos pca decomposition dado por la librería de `sklearn`. Esta recibe por input los vectores característicos de la imagen, y reduce la cantidad de dimensiones. En nuestro caso se redujo las dimensiones para tener una precisión de 90%. Logrando reducir de 128 dimensiones originales a 49 dimensiones.

Estos nuevos vectores de imágenes que fueron reducidos luego son insertados al índice. Teniendo guardando información útil, como el path de la imagen.


#### diagrama:

![diagrama de flujo](https://media.discordapp.net/attachments/840221207172350003/873360416842059816/Untitled_Diagram.png)


# Algoritmo de búsqueda KNN

Se realizaron dos implementaciones para KNN de acuerdo a lo requerido. Estas consisten en una implementación por nearest neighbors de un RTree y un sequential scan. Por defecto nuestra implementación tiene un k de 8.

- **Utilizando RTrees:** El algoritmo de Knn tiene una implementación trivial. Debido a la librería `rtree` ,  usada para el R-tree contiene la función `nearest` la cual implementa la búsqueda por Knn.  

- **Utiliando Sequential Scan:** Se utiliza un sequential scan con ayuda de un Max-Heap (implementado con `heapq`). Se agregan inicialmente los k primeros inputs a la heap. Tras ello, se siguen agregando todos los restantees, pero en cada iteración se remueve el máximo de la heap para mantener la invariante de k elementos.

Lo que retornamos con la función Knn es una lista que contiene coordenadas del vector/punto y su key (el path a la imagen).



# Algoritmo de búsqueda por Rango

A comparación de la búsqueda Knn este no usa el índex del Rtree para poder encontrar los puntos mas cercanos. En cambio, utiliza la función `intersect` del index. Se coloca un bounding box desde (px_0 - d, px_1 - d, px_2 - d, ...) hasta (px_0 + d,  px_1 + d, px_2 + d, ...) y se filtran todos los posibles candidatos. Tras ello, se remueven todos aquellos puntos que estan en el bounding box, pero que no están dentro de la distancia d (es decir, todos los puntos fuera del hipercirculo que conforma el radio, pero dentro del hipercubo circunscrito a la misma).

El formato de retorno es el mismo que en el caso del KNN Search, por lo que pueden usarse intercambiablemente.




# Análisis y discusión de la experimentación


Aplicacacion el KNN-RTree y el KNN-secuencial haciendo crecer el tamaño de la colección (N) para comparar la eficiencia en tiempos de ejecución en segundos (10 iteraciones):

| Tiempo|      KNN-RTree|  KNN-Secuencial|
|----------|:-------------:|------:|
|100       |  6.32         |6.21       |
|200       |  6.48         |6.38       |
|400       | 7.48          | 9.46      |
|800       |  6.53         | 7.42      |
|1600      |  6.02         |  6.39     |
|3200      |  6.11         |  6.99     |
|6400      |  6.63         |    7.70   |
|12800     |  7.30         |  8.72     |





# Requisitos

- Flask 
- python3
- face_recognition
- pandas
- rtree
- numpy

## Pruebas de uso y presentación

- [Vídeo del proyecto](https://drive.google.com/drive/folders/1vCWJYOEFpJduP1AZBpRjJouA5BNZIWBy?usp=sharing)

