SELECT 
  data_venda, 
  COUNT(*) AS total_vendas, 
  SUM(valor) AS valor_total
FROM vendas
GROUP BY data_venda
ORDER BY data_venda;