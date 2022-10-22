# Registro de configurações feitas no Ubuntu


## 0. Pré-requisitos

* Python 3.8
* pip3

```bash
sudo apt install python3.8
sudo apt install python3-pip
```


## 1. MariaDB

### 1.1 Instalação e configuração

Instalar o MariaDB, iniciar o serviço e adicionar/alterar no arquivo de configuração "50-server.cnf" uma linha para permitir acessos externos: `bind-address = 0.0.0.0`. [opcional]

```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb.service
sudo mysql_secure_installation
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

### 1.2 Criar uma base de dados e um usuário administrador

Fazer o acesso ao MariaDB, criar uma database chamada "temp_sensors", e um usuário "admin" com todos os privilégios.

```bash
sudo mariadb
```

```sql
CREATE DATABASE temp_sensors;
CREATE USER admin@localhost IDENTIFIED BY '123';
GRANT ALL ON *.* TO admin@localhost;
FLUSH PRIVILEGES;
```

Comandos úteis:

* Listar as bases de dados existentes: `SHOW DATABASES`
* Listar os usuários existentes: `SELECT User FROM mysql.user;`
* Listar as permissões: `SHOW GRANTS FOR admin@localhost;`
* Sair do console MariaDB: `exit` ou `CTRL+C`

### 1.3 Acessar como administrador e criar tabela

Criamos uma tabela "received_data" com as colunas:

* indice
* device_id
* data_hora
* temperatura

```bash
sudo mariadb -u admin -p
```

```sql
use temp_sensors
create table received_data(
    indice int auto_increment,
    device_id int not null,
    data_hora timestamp,
    temperatura float,
    primary key(indice)
);
commit;
```

### 1.4 Teste de insert

Nesse passo, inserimos uma linha para testar e consultamos.

```sql
insert into received_data(device_id, data_hora, temperatura)
values(3522, "2022-10-19 21:13:07", 24.0);
commit;
select * from received_data
```


## 2. Broker Mosquitto

## 2.1 Instalação e configuração

Instalar o Mosquitto e configurar um usuário para autenticação.

```bash
sudo apt-get install mosquitto mosquitto-clients
sudo nano /etc/mosquitto/conf.d/my.conf
```

No arquivo "my.conf" inserir as linhas:

`listener 1883`
`allow_anonymous false`
`acl_file /home/ubuntu/users/regras.txt`
`password_file /home/ubuntu/users/senhas.txt`

Criar os arquivos "regras.txt" e "senhas.txt" que são referenciados no arquivo "my.conf".

```bash
sudo nano /home/ubuntu/users/regras.txt
```

`user device`
`topic readwrite temperatura`
`topic readwrite teste`

```bash
sudo nano /home/ubuntu/users/senhas.txt
```



```bash
sudo service mosquitto stop
sudo service mosquitto start
```


## 3. Instalação do MariaDB Connector para Python3

```bash
sudo apt-get install -y libmariadb-dev
pip3 install mariadb==1.0.11
```

## 4. Instalação do Paho MQTT Client para Python

```bash
pip3 install paho-mqtt
```