# RD Condominios - Gestão de Condomínios

UFCD 5425 - Projeto de tecnologias e programação de sistemas de informação

Formando: Renato Duarte | Formador: Ruben Ferreira 
___
## Sobre o projeto

O *RD Condomínios* é uma aplicação web para a gestão de condomínios. Permite
guardar num só local as moradias, os moradores, as quotas, as despesas comuns
e as obras, e consultá-las de forma simples.

É uma aplicação de uso pessoal, para um único utilizador e um único condomínio,
que corre localmente.

## Principais funcionalidades
- **Moradias:** registar, consultar, editar e apagar. A identificação é obrigatória e única. Não se apaga uma moradia que tenha moradores ou quotas.
- **Moradores:** registar proprietários e inquilinos associados a uma moradia. o NIF tem 9 algarismos e não se repete. Registo da data de entrada e da data de saída.
- **Quotas:** registar quptas por moradia, ano e mês. Com data de vencimento. Registo do pagamento. O estado é calculado pelas datas.
- **Despesas:** registar despesas por categoria. A parte por moradia é calculada dividindo o valor pelo número de moradias.
- **Obras:** registar obras e acompanhar o estado. Uma obra concluída tem de ter data de conclusão.
- Todos os registos podem ser editados e apagados, com confirmação ao apagar.
- Mensagens de erro e confirmação de sucesso em cada operação.

## Tecnologias
- **Python** - Linguagem de programação
- **Flask** - framework web
- **SQLite** - base de dados
- **HTML, CSS e Jinja2** - interface
- **Pytest** - testes automatizados

## Requisitos
- Python 3.12 ou superior
- As dependências do 'requirements.txt'

## Instalação
    1. Abrir um terminal na pasta do projeto.
    2. Criar o ambiente virtual:
        python -m venv .venv
    3. Ativar o ambiente virtual
        source .venv/Scripts/activate (Git Bash) (bin ou Scripts)
    4. Instalar as dependências
        pip install -r requirements.txt

## Base de dados
A base de dados é um ficheiro SQLite. Fica em '/data/condominio.db' e é criada
automaticamente, com todas as tabelas, quando a aplicação arranca pela primeira vez.
Não é preciso correr nenhum script.

## Executar a aplicação
Na pasta do projeto, com o ambiente virtual ativo:

    PYTHONPATH=src

    flask --app rd_condominios.app run --debug (Git Bash)

Abrir no browser: http://127.0.0.1:5000

Parar a aplicação: CTRL+C (no terminal)

## Testes
Os testes usam uma base de dados temporária e não alteram os dados da aplicação.
Cobrem a validação dos dados, as regras de duplicação, o estado das quotas, a 
parte por moradia e as regras das obras
(todos os dados são fictícios)

## Estrutura do projeto
rd_condominios/

    data/                       base de dados (criada ao arrancar)

    docs/schema.sql             script SQL das tabelas

    src/rd_condominios/

        app.py                  cria a aplicação e regista as rotas

        config.py               caminho da base de dados

        base_dados.py           ligação e criação das tabelas

        web/                    rotas Flask (um Blueprint por entidade)

        servicos/               coordenam as operações

        dominio/                classes, regras e validações

        repositorios/           único sítio com SQL

        templates/              páginas HTML (jinja2)

        static/css              estilos

    tests/                      testes automatizados


A aplicação tem quatro camadas:
    'web' chama 'servicos', que usam o 'dominio' (regras) e os 'repositorios' (SQL).
    Não há SQL nas rotas nem nos templates, e todas as consultas são parametrizadas.

## LIMITAÇÕES DO PROJETO
- O modelo assume um único condomínio.
- O NIF é único, por isso a mesma pessoa não pode ser registada duas vezes (ex: no registo de uma saída e logo depois nova entrada)
- Não tem autenticação, proteção nem registo de erros.
- Usa o servidor de desenvolvimento do Flask.
Não tem migrações da base de dados.
