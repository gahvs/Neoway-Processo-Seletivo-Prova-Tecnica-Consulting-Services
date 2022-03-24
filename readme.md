# Neoway-Processo-Seletivo-Prova-Tecnica-Consulting-Services
## _Passo a passo de execução_
O código acima implementa um serviço de migração. O objetivo do mesmo é migrar informações contidas em um arquivo base (.txt) para um banco de dados PostgreSQL. Os detalhes sobre as tabelas para onde os dados serão migrados podem ser lidos [aqui](https://github.com/gahvs/Neoway-Processo-Seletivo-Prova-Tecnica-Consulting-Services/blob/main/Estrutura%20Relacional.pdf)

### _Instalação_

#### _1° Passo - Instalação do Docker_

Para execução do serviço é necessário possuir o docker instalado na máquina, você pode obter o Docker: 
- [Para Windows](https://docs.docker.com/desktop/windows/install/)
- [Para Linux](https://docs.docker.com/engine/install/ubuntu/)
- [Para Mac](https://docs.docker.com/desktop/mac/install/)

#### _2° Passo - Download do Código Fonte_
Com o Docker instalado o próximo passo é fazer o download do código fonte, isso pode ser feito de várias maneiras, como clonar o repositório usando o Git, mas vamos apenas baixar todos arquivos clicando [aqui](https://github.com/gahvs/Neoway-Processo-Seletivo-Prova-Tecnica-Consulting-Services/archive/refs/heads/main.zip).

#### _3° Passo - Descompactar Código Fonte_
Caso você tenha executado o download de forma diferente da anterior, por exemplo usando o Git, desconsidere esse passo. 
Assim que o download terminar você deve perceber que o código fonte vem compactado, portanto deve-se clicar com o botão direito e descompactar a pasta.

#### _4° Passo - Executar o serviço_
Neste ponto, você tem o Docker instalado e o código fonte baixado e descompactado. Isso é tudo o que é necessário para execução do serviço. Para executá-lo, basta então abrir um console em seu sistema operacional e navegar até a pasta do código fonte, especificamente deve-se navegar até a pasta que contém o arquivo **`docker-compose.yml`**.
Certo de que estamos na pasta acima, basta então digitarmos o comando:
```sh
docker-compose up
```
Este comando fará o Docker "buscar" o arquivo _docker-compose.yml_ e usá-lo para criar os containers onde a aplicação será executada. A partir disso não é necessário realizar mais nenhuma ação, apenas aguardar a mensagem na tela informando que o processo foi executado com sucesso.

**Observação**: Para melhorar a perfomance de execução o serviço não verifica se os dados do arquivo base já existem nas tabelas do banco de dados, portanto executar o comando acima duas vezes implicará em duplicação dos dados. Para testes é interessante limpar as tabelas antes da execução.
## Visualizar os dados
Para que possamos visualizar os dados migrados para o nosso PostgreSQL que está dentro do container Docker precisamos usar os seguindos comandos no terminal:

```sh
docker exec -it neoway-db-1 /bin/bash
```
Este comando fará com que o seu terminal passe a se comportar como o terminal do container do PostgreSQL (identificado pelo nome neoway-db-1). Dentro do container nós temos uma instância do PostgreSQL em execução e podemos acessá-la com o comando psql. Para isso devemos digitar:
```sh
# psql -h db -U postgres -W
```
Neste comando estamos dizendo que queremos acessar o banco em "db" como usuário "postgres" (as definições de host, user, password, etc do banco estão escritas no arquivo _docker-compose.yml_).

Uma vez acessado, podemos manipular o banco de dados com os comandos do psql ou com queries SQL. Experminte digitar **`\d`** para listar as tabelas do banco de dados ou **`SELECT * FROM CLIENTE LIMIT 5`** para visualizar as 5 primeiras tuplas da tabela CLIENTE.

Opcionalmente, você pode usar um scritp python que está dentro do código fonte para visualizar os dados de forma mais simples. Para isso **é necessário ter o Python instalado na sua máquina**

Acesse a pasta `service` do código fonte pelo terminal do seu S.O
Crie um ambiente virtual do Python com o comando:
```sh
py -m venv env
```
E ative o ambiente virtual
```sh
env\Scripts\activate
```
Instale as dependências do ambiente:
```sh
pip install -r requirements.txt
```
E então digite `py` no terminal para entrar no prompt interativo do python dentro da pasta `service`.

Dentro da pasta há o scritp `psql.py`, que implementa a classe `Interface`, essa classe fornece uma forma fácil de visualizar os dados do nosso banco de dados.
Para usá-la digite no prompt do Python:

```
from psql import Interface
ps = Interface(user="postgres", password="postgres", host="localhost", port=5432, database="postgres")
```
A partir disso podemos usar o objeto `ps` para realizar diversar operações no banco, as principais são:

```
ps.tables()  # mostra uma lista das tabelas do banco
ps.columns("table_name")  # mostra as colunas da tabela
ps.delete("table_name")  # apaga todos os registros da tabela
ps.drop("table_name")  # exclui a tabela do banco de dados
ps.size("table_name")  # retorna a quantidade de registros da tabela
ps.head("table_name")  # retorna os 5 primeiros registros da tabela
ps.get("table_name", ID)  # retorna o registro correspondente ao ID na tabela
ps.exec("SQL_QUERY")  # executa a sentença SQL no banco de dados
```