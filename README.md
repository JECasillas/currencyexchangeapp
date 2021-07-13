# README #


### Description ###

* This repository is an implementation for a currency exchange app challenge. The Este repositorio es una implementación demostrativa de la funcionalidad del cálculo de distancias semánticas entre dos textos cualesquiera usando sorensen en una función serverless.
Consiste en una función:
    + **distance**, la estipulada en el handler de `calculate_distance.py`: Vectoriza dos textos y realiza una cálculo de cercanía semántica.
* Version 0.0

### Implementación ###

* Instala los paquetes de npm requeridos
```shell
$ npm install
```
* Instala serverless
```shell
$ npm install -g serverless@1.48.2
```
* Configura tu instalación de serverless a tu cuenta o usuario de Amazon
* Especifica los paquetes de python requeridos en `requirements.txt`
* Deploy
```shell
$ sls deploy --stage dev
```

### Uso ###

###### processIntent
Para interactuar con la API de **distance** y obtener la distancia entre 2 textos:
    * API: [https://mk3l8tdck3.execute-api.us-west-2.amazonaws.com/dev/processDistance](URL).
    * Se envía en el body del POST la siguiente información:
```    
    {
     "requestText":"quisiera hablar con un ejecutivo",
     "responseText":"me gustaria hablar con un ejecutivo"
    }
```
    * los request y response text son los textos de los cuales hay que extraer distancia.

La respuesta contiene el valor de la distancia entre ambos textos:
```
    {
    "distance": 0.1578947368421053
    }
```

### Especificaciones técnicas ###

##### src/calculate_distance.py
El handler de dicho archivo se especifica como la función lambda con nombre **distance** en la configuración dentro de `serverless.yml` y obtiene la distancia entre dos textos. Referente a la figura (2.2) en nuestro diagrama de arquitectura.

![Alt text](https://referencias-documentacion.s3-us-west-2.amazonaws.com/2.2.png)  

##### preprocessing.py
Antes del cálculo de distancias se realiza un preprocesamiento de los textos y una conversión a sus representaciones vectoriales.

1. **Remoción de Stopwords** `removeStopwords(text)`: Quitamos todas las palabras del texto que consideramos no tienen peso semántico y diluyen el índice calculado, como artículos y pronombres.
2. **Stemización del Texto** `stemIt(text)`: Se extraen los lexemas según el algoritmo de Snowball. Es necesario que el vectorizador pueda contar dos palabras con el mismo lexema como la misma para atribuir los pesos correctos a cada palabra.
3. **Vectorización del Texto** `vectorizeText(text)`: Para representar a un texto como un vector vamos a contar ciertas particularidades del texto, esas particularidades etiquetan a las “cajas” de los vectores. Por ejemplo, algo muy común es contar las palabras de un texto, cada palabra se convierte en un **índice** del vector y la cantidad de veces que aparece esa palabra se le denomina el **escalr** del vector, el cual, al modificarlo, pasa a ser un **peso**. Para nuestro caso, nuestros vectores no sólo representan los pesos independientemente de la palabra; dado que tenemos que poder relacionar el mismo lexema al mismo peso en el vector a comparar, asociamos los escalares con sus respectivos pesos de la siguiente manera: [["lexema1",int2],["lexema2",int2],["lexema3",int3]]

Una vez expuestos como función lambda y como servicio por medio de API gateway, serán referentes a la figura (4) en nuestro diagrama de arquitectura.
![Alt text](https://referencias-documentacion.s3-us-west-2.amazonaws.com/4.png)  

##### src/distance.py
Incluye el algoritmo de la función del cálculo de la distancia de Sorensen.
La fórmula de Dice-Sorensen es un cálculo de similitud entre 2 conjuntos cualesquiera X y Y:  

![Alt text](https://referencias-documentacion.s3-us-west-2.amazonaws.com/sorensen.png)  

La fórmula como hemos de calcularla algorítmicamente:  
**D_{sorensen}(X,Y) = 1 - { 2* \sum x_i \land y_i \over \sum x_j \land 1 + \sum y_k \land 1 }**

Especificada para dos textos X y Y:  
![Alt text](https://referencias-documentacion.s3-us-west-2.amazonaws.com/sorensen_string.png)


### Contacto y autoría ###

* Jose Eduardo Casillas (jose.e.casillas@gmail.com)
