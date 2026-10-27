PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS "moradias" (
    "id_moradia"     INTEGER PRIMARY KEY,
    "identificacao"  VARCHAR(100) NOT NULL,
    "andar"          VARCHAR(50),
    "fracao"         VARCHAR(20),
    "observacoes"    TEXT
);

CREATE TABLE IF NOT EXISTS "moradores" (
    "id_moradores"   INTEGER PRIMARY KEY,
    "nome"           VARCHAR(100) NOT NULL,
    "nif"            VARCHAR(9) NOT NULL UNIQUE,
    "telefone"       VARCHAR(20),
    "email"          VARCHAR(100),
    -- proprietario ou inquilino
    "tipo"           VARCHAR(20) NOT NULL,
    "id_moradia"     INTEGER NOT NULL,
    FOREIGN KEY ("id_moradia") REFERENCES "moradias"("id_moradia")
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "quotas" (
    "id_quotas"       INTEGER PRIMARY KEY,
    "id_moradia"      INTEGER NOT NULL,
    "ano"             INTEGER NOT NULL,
    "mes"             INTEGER NOT NULL,
    "valor"           REAL NOT NULL,
    "data_vencimento" DATE NOT NULL,
    "data_pagamento"  DATE,
    -- pago; pendente; em atraso
    "estado"          VARCHAR(20) NOT NULL,
    FOREIGN KEY ("id_moradia") REFERENCES "moradias"("id_moradia")
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    -- impede duas quotas para a mesma moradia no mesmo mes e ano
    UNIQUE ("id_moradia", "ano", "mes")
);

CREATE TABLE IF NOT EXISTS "despesas" (
    "id_despesas"  INTEGER PRIMARY KEY,
    "descricao"    VARCHAR(200) NOT NULL,
    -- limpeza; seguro; agua; eletricidade; obra; outras
    "categoria"    VARCHAR(50) NOT NULL,
    "valor"        REAL NOT NULL,
    "data"         DATE NOT NULL,
    "fornecedor"   VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS "obras" (
    "id_obras"        INTEGER PRIMARY KEY,
    "descricao"       VARCHAR(200) NOT NULL,
    "data_pedido"     DATE NOT NULL,
    "data_conclusao"  DATE,
    -- pendente; em curso; concluida
    "estado"          VARCHAR(20) NOT NULL,
    "orcamento"       REAL,
    "custo_final"     REAL
);
