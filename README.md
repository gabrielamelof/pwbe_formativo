# Projeto Formativo 👩‍💻

O projeto formativo proposto para a disciplina de PWBE foi uma API para o gerenciamento de uma escola. O projeto desenvolvido permite a criação de usuários, login, gerenciamento dos usuários, salas, disciplinas e reservas de ambiente criadas. A aplicação foi desenvolvida utilizando Django RestFramework.

## Tutorial ✏️
Para que o projeto funcione de maneira correta e esperada em sua máquina, é necessário seguir alguns passos: 

### Instalações 🔧
É necessário que as seguintes aplicações estejam instaladas em sua máquina para que você possa testar ou modificar o projeto:
 - Python 3.9+
 - MySQL
 
Caso alguma das aplicações não esteja instalada em sua máquina, é possível fazer a instalação nos seguintes links:
- [Python](https://www.python.org/downloads/)
- [MySQL](https://www.mysql.com/downloads/)

***

### Para o projeto ⌨️
#### 1. Banco de Dados 📋
Para o funcionamento correto do banco de dados no MYSQL, ele deve ser configurado da seguinte maneira no arquivo `settings.py`:
````
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'formativo', #Nome do banco de dados
        'USER' : 'root', #Nome do usuário 
        'PASSWORD' : 'senai', #Senha do banco de dados
        'HOST' : 'localhost', #Endereço
        'PORT' : '3306' #Porta em que o banco será executado
    }
}
````
❗❗❗O banco de dados "formativo" precisa estar criado. É possível criá-lo no MySQL Workbench com o comando `CREATE DATABASE formativo; ` ❗❗❗
#### 2. Instalação do Ambiente de Desenvolvimento 😄
É necessário que um ambiente virtual com todas as instalações do projeto seja configurado a cada vez que alguma alteração ou teste tiver de ser feita.

Para iniciar um novo ambiente virtual de desenvolvimento é necessário dar o comando `python -m venv env`, certificando-se de que a pasta em que está é a do projeto. 

Com a env instalada, agora vamos a ativar. Para concluir essa etapa, é só dar o comando `.env/Scripts/activate`

Depois disso, basta dar o comando `pip install -r requirements.txt` para que todas as aplicações necessárias para o funcionamento do projeto sejam instaladas no ambiente virtual criado anteriormente.

#### 3. Modificações nos modelos ⚙️
Caso alguma mudança seja feita no arquivo `models.py`, é necessário dar os respectivos comandos: `python ./manage.py makemigrations` e `python ./manage.py migrate` para que as modificações sejam feitas no banco de dados.

#### 4. Criação de usuários 👩‍🦰
Para criar um novo usuário com acesso a todas as funcionalidades da aplicação, é preciso dar o comando `python manage.py createsuperuser` e preencher as informações pedidas, sendo tipo informado como **"G"**.

#### 5. Rodar o servidor 🏃‍♂️‍➡️
Para o último passo, é necessário rodar o servidor. Você pode fazer isso com o comando `python manage.py runserver`
### Com o projeto funcionando 🌟
Depois de seguir esses passos, o projeto foi configurado da maneira correta e está pronto para utilização.

Para qualquer dúvida, a documentação detalhada do projeto está disponível nesse link: [Postman](https://documenter.getpostman.com/view/41755085/2sB2qZDMwA#b4c430e2-882c-4fae-9c27-d24cecc24d5b).

Agora é só testar e modificar da forma que quiser! 🙃

Por **Gabriela Melo** 



