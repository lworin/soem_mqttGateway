# Setup Ubuntu


## 1. Pré-requisitos

Instalar Python 3.8 e pip3.

```shell
sudo apt install python3.8
sudo apt install python3-pip
python3 --version
pip3 --version
```


## 2. Instalação do MariaDB Connector para Python3

```shell
sudo apt-get install -y libmariadb-dev
pip3 install mariadb==1.0.11
```


## 3. Instalação do Paho MQTT Client para Python3

```shell
pip3 install paho-mqtt
```


## 4. MariaDB

### 4.1 Instalação e configuração

Instalar o MariaDB e iniciar o serviço.

```shell
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb.service
sudo mysql_secure_installation
```

 Opcional: adicionar/alterar no arquivo de configuração *50-server.cnf* uma linha para permitir acessos externos.

```shell
 sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
 
 >bind-address = 0.0.0.0

### 4.2 Criar uma base de dados e um usuário administrador

Fazer o acesso ao MariaDB, criar uma database chamada *TempSensors*, e um usuário *admin* com todos os privilégios.

```shell
sudo mariadb
```

```sql
CREATE DATABASE TempSensors;
CREATE USER admin@localhost IDENTIFIED BY '123';
GRANT ALL ON *.* TO admin@localhost;
FLUSH PRIVILEGES;
```

Comandos úteis:

* Listar as bases de dados existentes: `SHOW DATABASES;`
* Listar os usuários existentes: `SELECT User FROM mysql.user;`
* Listar as permissões: `SHOW GRANTS FOR admin@localhost;`
* Sair do console MariaDB: `exit` ou `CTRL+C`

### 4.3 Acessar como administrador e criar tabela

Criamos uma tabela *ReceivedData* com as colunas:

* indice
* deviceid
* datahora
* temperatura

```shell
sudo mariadb -u admin -p
```

```sql
USE TempSensors
CREATE TABLE ReceivedData(
    indice INT auto_increment,
    deviceid INT NOT NULL,
    datahora TIMESTAMP,
    temperatura FLOAT,
    PRIMARY KEY(indice)
);
COMMIT;
```

### 4.4 Teste de insert

Nesse passo, inserimos uma linha para testar e consultamos.

```sql
INSERT INTO ReceivedData(deviceid, datahora, temperatura)
VALUES(3522, "2022-10-19 21:14:22", 24.3);
COMMIT;
SELECT * FROM ReceivedData;
DELETE FROM ReceivedData WHERE deviceid=3522;
```


## 5. Broker Mosquitto

### 5.1 Instalação e configuração

Instalar o Mosquitto e abrir o arquivo *my.conf*.

```shell
sudo apt-get install mosquitto mosquitto-clients
sudo nano /etc/mosquitto/conf.d/my.conf
```

No arquivo *my.conf* inserir as linhas:

>listener 1883  
allow_anonymous false  
acl_file /home/ubuntu/users/regras.txt  
password_file /home/ubuntu/users/senhas.txt

### 5.2 Autenticação e criação de usuário

Criar os arquivos *senhas.txt* e *regras.txt* que são referenciados no arquivo *my.conf*.

```shell
sudo touch /home/ubuntu/users/senhas.txt
sudo touch /home/ubuntu/users/regras.txt
```

Criar o usuário *device* com senha *dev123*.

```shell
sudo mosquitto_passwd -b /home/ubuntu/users/senhas.txt device dev123
```

No arquivo *regras.txt*, inserir as linhas abaixo para permitir acesso ao tópico *temperatura*.

```shell
sudo nano /home/ubuntu/users/regras.txt
```

>user device  
topic readwrite temperature

Reiniciar o serviço

```shell
sudo service mosquitto restart
```

### 5.3 Exemplo de publicação

```shell
sudo mosquitto_pub -h localhost -p 1883 -u device -P dev123 -t temperature -m '5589#25.7'
```