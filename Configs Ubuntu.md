# Passo a Passo


## MariaDB

### Instalação e configuração do banco de dados MariaDB

```bash
sudo apt update
sudo apt install mariadb-server
sudo systemctl start mariadb.service
sudo mysql_secure_installation
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Adicionar ao arquivo: `bind-address = 0.0.0.0`


### Criar uma database e um usuário

```bash
sudo mariadb
CREATE DATABASE mydb;
CREATE USER luan@'%' IDENTIFIED BY '123';
GRANT ALL ON *.* TO 'luan'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'luan'@'%';
exit
```

### Criando tabelas

```sql
create table sensors(
    indice int auto_increment,
    id int not null,
    datahora timestamp,
    temperatura int,
    primary key(indice)
);
commit;
```

### Teste de insert
```sql
insert into sensors(id, datahora, temperatura)
values(0001, "2022-10-19 21:13:07", 24);
commit;
```


### Fontes

https://www.digitalocean.com/community/tutorials/how-to-install-mariadb-on-ubuntu-20-04
https://mariadb.com/kb/en/configuring-mariadb-for-remote-client-access/
https://www.daniloaz.com/en/how-to-create-a-user-in-mysql-mariadb-and-grant-permissions-on-a-specific-database/




## MariaDB Connector para Python3

### Instalar o connector
```bash
sudo apt-get install -y libmariadb-dev
pip3 install mariadb==1.0.11
```

### Fontes

https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/


## Broker Mosquitto

```bash

```

## Paho MQTT Client para Python

```bash
pip3 install paho-mqtt
```