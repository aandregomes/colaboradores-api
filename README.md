# aquarela-users-api

### Requisitos:
* Postgres 14
* Python 3.9.6
* Flask 2.0.3

### Configurações iniciais:
* Criação de um ambiente virtual

`python3 -m venv <nome-do-ambiente>`

*  Instalação das dependências

`pip install -r requirements.txt`

* No postgres rodar

```sql
create database aquarelausers;
create database aquarelauserstest;
```
* Criar um usuário com permissões de admin no Postgres
* Criar um arquivo `.env` na raiz do projeto e siga o exemplo

```env
FLASK_ENV=development
POSTGRES_URL=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=senha-segura-aqui
POSTGRES_DB=aquarelausers
POSTGRES_DB_TEST=aquarelauserstest
```
* Adicione permissão para executar o arquivo `run-migrations.sh`
```shell script
chmod +x run-migrations.sh
```
 * Rode o script com `source ./run-migrations.sh`

### Rodando a aplicação Local
Basta executar o seguinte comando: `python main.py `

### Testes
Para rodar os testes basta executar o comando: `python -m pytest`

### Documentação
Rodando o projeto a documentação estará disponivel em `http://127.0.0.1:5000/#docs`

### Funcionamento
Para criar um novo colaborador é necessário que exista um cargo para atribuir
