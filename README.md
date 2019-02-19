# Alias chatbot for Google Hangouts Chat


Languages: 
[ English ](#english) - [ Português ](#português)

Table of content:

 - [Requirements & Installation](#requirements--installation)
 - [How it works](#how-it-works)
 - [How make code adjument](#how-to-change-the-code)
 - [Reference](#reference)

## English

Alias chatbot for Google Hangouts Chat to send a message to a list of members in a room, usage:

![alt text](https://raw.githubusercontent.com/renanpessoa/hangouts-chatbot-alias/master/1.png "Image")
![alt text](https://raw.githubusercontent.com/renanpessoa/hangouts-chatbot-alias/master/2.png "Image")

# Requirements & Installation

**Docker must be installed on the server**

-  Check if `docker-compose` is available:

```bash
$ docker-compose  -v
docker-compose version 1.23.2, build 1110ad0
$ 
```

- If not, install it:

```bash
pip3 install docker-compose
```

- Clone the repository and access chatbot dir

```bash
git clone https://github.com/renanpessoa/hangouts-chatbot-alias.git
cd hangouts-chatbot-alias
```

- Access this page https://console.developers.google.com/iam-admin/settings?authuser=1&organizationId=`$ORGANIZATIONID`&project=`$PROJECT_NAME` and add the project number of the bot in `application.py` like that: 

```bash
  PROJECT_NUMBER = ['0123456789']
``` 

- Build images: 

```bash
docker-compose build
``` 
- After build, start containers:

```bash
docker-compose up -d
``` 

# How it works

`docker-compose`  orchestrator will build two containers:
  - `app`
    - It has a [Python](https://www.python.org/)  application with microframework [Flask](http://flask.pocoo.org/) to handle  [Chat](https://chat.google.com/u/0/?pageId=none) post. Inside in this container we have also [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) to web server.
    - uWSGI will start 5 processes, to change it edit the `project.ini` file.
    - All data are stored in Redis container. 
  - `redis`
    - This container will be the database in memory using [Redis](https://redis.io/). 
    - The data are persistence in Docker volume called `redis_data`. 

# How to change the code

Don't make **`ANY`** change inside the container, **`all changes will be lost`**! 

All changes must be made in local files and then create a new build: 

  - Stop containers
  
	```bash
	docker-compose down
	```

  - Create new build

 	```bash
	docker-compose build
	```

  - Start

 	```bash
	docker-compose up -d
	```

## Reference
- [Hangouts Chat developer documentation](https://developers.google.com/hangouts/chat)


<a name="ptbr"></a>
## Português

Chatbot de alias para o Google Hangouts Chat, exemplo de uso:

![alt text](https://raw.githubusercontent.com/renanpessoa/hangouts-chatbot-alias/master/1.png "Image")
![alt text](https://raw.githubusercontent.com/renanpessoa/hangouts-chatbot-alias/master/2.png "Image")

# Requisitos e Instalação 

**É necessário ter o Docker instalado no servidor**

-  Verifique se o docker-compose está instalado com o comando abaixo:

```bash
$ docker-compose  -v
docker-compose version 1.23.2, build 1110ad0
$ 
```

- Se retornar  erro é necessário realizar a instalação: 

```bash
pip3 install docker-compose
```

- Clone o repositório e acesse o diretório da aplicação

```bash
git clone https://github.com/renanpessoa/hangouts-chatbot-alias.git
cd hangouts-chatbot-alias
```

- Acesse a página https://console.developers.google.com/iam-admin/settings?authuser=1&organizationId=`$ORGANIZATIONID`&project=`$PROJECT_NAME` e adicione o número do projeto do bot no arquivo `application.py` exemplo: 

```bash
  PROJECT_NUMBER = ['0123456789']
``` 

- Realize o build das imagens utilizando o comando abaixo, o procedimento pode levar alguns minutos.

```bash
docker-compose build
``` 
- Após o build os containers estão prontos para iniciar.

```bash
docker-compose up -d
``` 

# Como funciona

O orquestrador `docker-compose` vai subir dois containers:
  - `app`
    - Contem aplicação em [Python](https://www.python.org/) que foi criada utilizando o microframework [Flask](http://flask.pocoo.org/) para receber as requisições do [Chat](https://chat.google.com/u/0/?pageId=none) e retornar os dados solicitados, dentro do container também está instalado o [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) para servir como web server.
    - O uWSGI está configurado para inicializar 5 processos dentro do container para servir as requisições, caso seja necessário ajustar este valor basta editar o arquivo `project.ini`
    - Os dados utilizados pela aplicação são gerenciados pelo container redis. 
  - `redis`
    - Este container serve como banco de dados em memória utilizando o [Redis](https://redis.io/) por questões de desempenho. 
    - Apesar dos dados serem consultados na memória também é realizado a persistencia em disco no volume `redis_data` criado automáticamente pelo orquestrador docker compose, com isso não há risco dos dados serem perdidos quando o container for finalizado.


# Como realizar alterações no código da aplicação

Caso seja necessário realizar algum ajuste no código da aplicação ou nos arquivos de configuração **`NUNCA`** altere diretamente no container pois ele não armazena dados, qualquer alteração será **`PERDIDA`**!

Realize os ajustes nos arquivos locais, em seguida realize um novo build para gerar novas imagens utilizando o comando abaixo. 
  - Para os containers atuais

	```bash
	docker-compose down
	```
  - Realize o novo build

 	```bash
	docker-compose build
	```
  - Inicie os containers

 	```bash
	docker-compose up -d
	```

OBS: Não é necessário realizar um novo build para alterar as variaveis de ambiente do `docker-compose.yml`  como por exemplo o TOKEN, basta reiniciar os containers. 

## Referência
- [Hangouts Chat developer documentation](https://developers.google.com/hangouts/chat)
