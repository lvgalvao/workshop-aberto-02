CREATE TABLE vendas_calculado (
  venda_id SERIAL PRIMARY KEY,
  data_venda DATE NOT NULL,
  valor DECIMAL(10, 2) NOT NULL,
  quantidade INT NOT NULL,
  cliente_id INT NOT NULL,
  categoria VARCHAR(255) NOT null,
  total_vendas DECIMAL(10, 2) NOT NULL
);

INSERT INTO vendas_calculado (data_venda, valor, quantidade, cliente_id, categoria, total_vendas)
SELECT data_venda, valor, quantidade, cliente_id, categoria, (valor * quantidade) AS total_vendas
FROM vendas;
