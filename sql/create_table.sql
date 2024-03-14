CREATE TABLE vendas (
  venda_id SERIAL PRIMARY KEY,
  data_venda DATE NOT NULL,
  valor DECIMAL(10, 2) NOT NULL,
  quantidade INT NOT NULL,
  cliente_id INT NOT NULL,
  categoria VARCHAR(255) NOT NULL
);

CREATE TABLE vendas_calculado (
  venda_id SERIAL PRIMARY KEY,
  data_venda DATE NOT NULL,
  valor DECIMAL(10, 2) NOT NULL,
  quantidade INT NOT NULL,
  cliente_id INT NOT NULL,
  categoria VARCHAR(255) NOT NULL
  total_vendas DECIMAL(10, 2) NOT NULL,
);
