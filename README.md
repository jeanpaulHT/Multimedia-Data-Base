


# Text-Retrieval
literalmente el tercer proyecto de bede-II

## Integrantes

- Esteban Villacorta  201910336
- Jean Paul Huby Tuesta 201910194
- Daniela Abril Vento Bustamante 201910331

## Descripción

El objetivo del proyecto será la implementación de un buscador de imágenes usando la estructura de R-tree. La colección de imágenes usadas fueron sacadas de    [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) : una coleccion de mas de 13 mil imágenes para propósitos de desarrollo de software.

Para la búsqueda de estas imágenes se debe hacer uso las funciones knn  y búsqueda por rango para el R-tree.


# Construcción del índice R-tree



## Encoding de imagen

Para poder hacer uso de una imagen en un Rtree necesitamos representarla como un punto en un espacio de K dimensiones. Por lo que tenemos que procesar la imagen de alguna manera para obtener un vector. Este vector obtener será el vector característico de la imagen. 

Obtenemos este vector usando la librería `face_recognition` la cual procesa unan imagen para devolver un vector de de tamaño 128. 

Sin embargo todo este proceso es bastante lento como para ser calculado en run-time cada vez que se corra el código. Por lo que se hace todo el peso de este calculo en una etapa de preprocesamiento.



## preprocesamiento

Antes de crear el el index del R-tree primero debemos calcular los vectores característicos de la imagen. Lo cual es una operación pesada considerando que se tiene que hacer para 13 mil imágenes. Por lo hace necesario esta etapa de preprocesamiento.

El procesamiento simplemente se calcula los vectores caracteristicos de la imagen. Estos luego son guardados para luego ser escritos en un archivo csv. Este proceso puede durar hasta `1 hora`. 

Sin embargo la ventajas de no solo una lectura de un csv comparado con encodear las imágenes es abismal. Siendo necesario si queremos hacer el proceso aceptablemente rápido.



## Construcción del índice

La manera de como construimos el índice es indicando el numero de imágenes que se insertan deben insertar.

Para reducir la maldición de la dimensionalidad aplicamos pca decomposition dado por la librería de `sklearn`. Esta recibe por input los vectores característicos de la imagen, y reduce la cantidad de dimensiones. En nuestro caso se redujo las dimensiones para tener una precisión de 90%. Logrando reducir de 128 dimensiones originales a 49 dimensiones.

Estos nuevos vectores de imágenes que fueron reducidos luego son insertados al índice. Teniendo guardando información útil, como el path de la imagen.


# Algoritmo de búsqueda KNN

El algoritmo de Knn tiene una implementación trivial. Debido a la librería `rtree` ,  usada para el R-tree contiene la función `nearest` la cual implementa la búsqueda por Knn.  Por defecto nuestra implementación tiene un k de 8.

Lo que retornamos con la función Knn es la coordenadas del vector/punto y su key (el path a la imagen).



# Algoritmo de búsqueda por Rango

A comparación de la búsqueda Knn este no usa el índex del Rtree para poder encontrar los puntos mas cercanos.

Luego recorre e inserta los puntos que estén dentro de la distancia propuesta, ordenándolo por esta con un heapify.

Al igual que el Knn retorna  el punto/vector y el path a la imagen.




# Análisis y discusión de la experimentación


Aplicacacion el KNN-RTree y el KNN-secuencial haciendo crecer el tamaño de la colección (N) para comparar la eficiencia en tiempos de ejecución:

| Tiempo|      KNN-RTree|  KNN-Secuencial|
|----------|:-------------:|------:|
|100       |               |       |
|200       |               |       |
|400       |               |       |
|800       |               |       |
|1600      |               |       |
|3200      |               |       |
|6400      |               |       |
|12800     |               |       |



# Requisitos

- Flask 
- python3
- face_recognition
- pandas
- rtree
- numpy

## Pruebas de uso y presentación

- [Vídeo del proyecto](https://drive.google.com/drive/folders/1vCWJYOEFpJduP1AZBpRjJouA5BNZIWBy?usp=sharing)
