SELECT 
  categoria, 
  COUNT(*) AS total_vendas, 
  SUM(valor) AS valor_total
FROM vendas
GROUP BY categoria
ORDER BY valor_total DESC;