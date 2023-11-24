-- Apaga as tabelas caso existam.
-- Cuidado, isso destrói todos os dados do banco.
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS owner;

-- Cria a tabela 'owner'.

CREATE TABLE owner (
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_name TEXT, 
    owner_email TEXT, 
    owner_password TEXT, 
    owner_birth DATE,
    owner_status TEXT DEFAULT 'on',
    owner_field1 TEXT,
    owner_field2 TEXT
);

INSERT INTO owner (owner_id, owner_date, owner_name, owner_email, owner_password, owner_birth, owner_status)
VALUES
	('1', '2023-11-30 21:41:11', 'Joca da Silva', 'joca@silva.com', '123', '1988-08-20', 'on'),
	('2','2023-11-25 22:22:22','Maria Oliveira','maria@oliveira.com','abc','1995-05-20','on'),
	('3','2023-10-17 23:33:33','Carlos Santos','carlos@santos.com','xyz','1980-08-05','off'),
	('4','2023-04-27 00:44:44','Ana Pereira','ana@pereira.com','456','1992-03-10','on'),
	('5','2023-11-05 01:55:55','Ricardo Souza','ricardo@souza.com','789','1985-09-28','off'),
	('6','2023-07-07 02:06:06','Fernanda Lima','fernanda@lima.com','qwerty','1998-11-03','on'),
	('7','2023-05-29 03:17:17','Paulo Costa','paulo@costa.com','asdf','1982-07-15','off'),
	('8','2023-11-30 04:28:28','Beatriz Rocha','beatriz@rocha.com','zxcvbn','1990-12-22','on');

CREATE TABLE item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    item_name TEXT, 
    item_description TEXT, 
    item_location TEXT, 
    item_owner INTEGER,
    item_status TEXT DEFAULT 'on',
    item_field1 TEXT,
    item_field2 TEXT,
	FOREIGN KEY (item_owner) REFERENCES owner (owner_id)
);

-- Popula 'item' com dados 'fake' ' aleatórios.
INSERT INTO item (item_date, item_name, item_description, item_location, item_owner)
VALUES
  ('2023-05-12 14:15:00', 'Produto1', 'Descrição do Produto 1', 'Localização 1', 1),
  ('2023-06-21 23:24:25', 'Produto2', 'Descrição do Produto 2', 'Localização 2', 2),
  ('2023-10-01 08:09:00', 'Produto3', 'Descrição do Produto 3', 'Localização 3', 3);
