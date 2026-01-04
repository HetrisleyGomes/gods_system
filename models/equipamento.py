


nome da tabela: equipamento
valores: 'id' integer, primary key serial; 'nome' varchar(50); 'tipo de arma' varchar(36); 'tipo de dano' varchar(36); 'efeito' varchar(36); 'dano' varchar(10)
Preciso também de um relacionamento com ficha, onde uma ficha pode ter mais de um equipamento e um equipamento pode fazer parte de mais de uma ficha.

nome da tabela: mecha
valores: 'id' integer, primary key serial; 'nome' varchar(50); 'vida' integer; 'armadura': integer; 'combate': integer; 'pontaria': integer; 'defesa': integer; 'forca' integer; 'arma' varchar(36); 'dano': varchar(10) 'tipo' varchar(36); 'efeito' varchar(36); 'habilidades' text;
Preciso também de um relacionamento com ficha, onde uma ficha tem apenas um mecha, e um mecha pertence apenas a uma ficha.


CREATE TABLE equipamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    tipo_arma VARCHAR(36),
    tipo_dano VARCHAR(36),
    efeito VARCHAR(36),
    dano VARCHAR(10)
);

CREATE TABLE ficha_equipamento (
    ficha_id VARCHAR(36) NOT NULL,
    equipamento_id INTEGER NOT NULL,

    PRIMARY KEY (ficha_id, equipamento_id),

    FOREIGN KEY (ficha_id) REFERENCES ficha(id) ON DELETE CASCADE,
    FOREIGN KEY (equipamento_id) REFERENCES equipamento(id) ON DELETE CASCADE
);

CREATE TABLE mecha (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    vida INTEGER NOT NULL,
    armadura INTEGER NOT NULL,
    combate INTEGER NOT NULL,
    pontaria INTEGER NOT NULL,
    defesa INTEGER NOT NULL,
    forca INTEGER NOT NULL,
    arma VARCHAR(36),
    dano VARCHAR(10),
    tipo VARCHAR(36),
    efeito VARCHAR(36),
    habilidades TEXT,

    -- chave estrangeira 1:1
    ficha_id VARCHAR(36) UNIQUE,  
    FOREIGN KEY (ficha_id) REFERENCES ficha(id) ON DELETE SET NULL
);
