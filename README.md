![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
# KUANTAZ TECH TEST 👾🖥

Esta es una pequeña API para gestionar datos de instituciones con sus respectivos proyectos y responsables


## Comenzando 🚀
_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

-   Docker 19.03^
-   Entorno linux 

---

## Instalación 🔧

### 1. Clonar el repositorio
```
git clone git@github.com:raebeb/kuantaz_technical_test.git
```
ó
```
git clone https://github.com/raebeb/kuantaz_technical_test.git
```
---

### 2. Levantar contenedores
```
sudo bash start.sh
```
> Si es primera vez que se levanta el proyecto, este se _buildeara_ e instalara todas las dependencias necesarias

Luego de ejecutar el comando de arriba en nuestra terminal apareceral algo como esto

```
[+] Building 1.6s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 38B                                                                                0.0s
 => [internal] load .dockerignore                                                                                  0.1s
 => => transferring context: 2B                                                                                    0.0s
 => [internal] load metadata for docker.io/tiangolo/uwsgi-nginx-flask:python3.8-alpine                             1.2s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 551B                                                                                  0.0s
 => [1/6] FROM docker.io/tiangolo/uwsgi-nginx-flask:python3.8-alpine@sha256:610f059fd273a9dc602ebd168092b8f156e33  0.0s
 => CACHED [2/6] RUN apk --update add bash nano                                                                    0.0s
 => CACHED [3/6] RUN apk add --no-cache postgresql-libs postgresql-dev gcc python3-dev musl-dev     && pip instal  0.0s
 => CACHED [4/6] COPY ./app /app                                                                                   0.0s
 => CACHED [5/6] COPY ./requirements.txt /var/www/requirements.txt                                                 0.0s
 => CACHED [6/6] RUN pip install -r /var/www/requirements.txt                                                      0.0s
 => exporting to image                                                                                             0.2s
 => => exporting layers                                                                                            0.0s
 => => writing image sha256:9d561a08c74eb29cfff09fe68c72438b6ca797f236899e000a2212e69da9f9d0                       0.0s
 => => naming to docker.io/library/mydockerapp                                                                     0.0s
da381833568a2b2cecee900461b02dbc0c4258e86f6868fe707cc62bcf491c53
7c1275a3101824d84f10dcc8600a790cb6e4f58ac813507f620d29cfe4416777
25ef376d757c2825891128d60fb2e2f200c19916b25bc91a3875ebb5ffa1fa44
```

Si es primera vez que se levanatan los contenedores es posible que ```mydockerapp``` falle, para correjir esto es necesario ejeutar ``` sudo docker stop mydockerapp && sudo docker start mydockerapp ``` esto reiniciara el contenedor
> Para detener completamente los contenedores es necesario ejecutar lo siguiente en nuestra terminal
> ``` sudo docker stop mydockerapp && sudo docker stop flask_db && sudo docker stop flask_test_db ```



### 3. Casos de prueba

En la raíz del proyecto se encuentra el archivo ```Kuantas Technical Test API.postman_collection.json``` el cual puede ser exportado a postman y tiene preparada las llamadas a todos los endpoints desarrol


## Ejecutando las pruebas ⚙
_El proyecto cuenta con una serie de tests unitarios, , para llevarlos a cabo se debe ejecutar el siguiente comando_
* Primero debemos entrar a la shell del contenedor ```mydockerapp``` para ello ejecutamos el siguiente comando
```
docker exec -it mydockerapp /bin/sh
```
* Dentro de la shell del contenedor navegamos hasta la carpeta ```/app```
```
cd app
```
* y dentro de esta carpeta ejecutamos lo suigiente para correr los test
```
python -m unittest test
```

***
## Construido con 🛠️
* [Python 3.8](https://www.python.org) - Lenguaje de programación
* [Docker](https://www.docker.com) - Gestor de contenedores
* [Postgresql](https://www.postgresql.org/) - Base de datos

***


## Autores ✒️
* [Francisca Osores](https://www.linkedin.com/in/francisca-osores-ortiz-152347149/) - Desarrollo completo de la aplicacion
* Ante cualquier duda o comentario escribir a fmosoresortiz@gmail.com


## ⌨️ con ❤️ por [Francisca Osores](https://www.linkedin.com/in/francisca-osores-ortiz-152347149/) 👩‍💻

```
          ／＞　 フ
         | 　_　_| 
       ／` ミ＿xノ 
      /　　　　 |
     /　 ヽ　　 ﾉ
    │　　|　|　|
／￣|　　 |　|　|
(￣ヽ＿_  ヽ_)__)
＼二)
```
