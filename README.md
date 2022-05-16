# Sistemas de Informação DECSI - UFOP
## CSI105 Algoritmos e Estruturas de Dados III 2021/2

Professor: Dr. George Henrique Godim da Fonseca

Aluna: [Juliana Mara Lemos](https://github.com/julianamlemos)

### Descrição
O trabalho consiste em implementar algoritmos para resolver problemas de caminho mínimo em grafos.
O projeto [Grafos](https://github.com/georgehgfonseca/Grafos), disponibilizado no GitHub,
deve ser adaptado com a implementação dos seguintes algoritmos para caminho mínimo:
- Busca Largura (para grafos não ponderados)
- Dijkstra e Bellman-Ford (para grafos com arestas de peso negativo).

Um conjunto de grafos de teste foi disponibilizado para avaliar os trabalho [Datasets](https://github.com/julianamlemos/AEDS_3/Datasets).
O seu programa deve, dadas as características do grafo de entrada:
- Escolher automaticamente o algoritmo mais eficiente para resolvê-lo
- Escolher a melhor estrutura de dados para representá-lo.

Ao executar o arquivo main.py, os seguintes dados devem ser informados:
```python

# Arquivo no formato DIMACS presente na pasta /Datasets
arquivo = input("Informe o nome do arquivo e sua extensão (Ex: nome.txt): ")

# Vértice de origem do grafo
origem = int(input("Informe o vértice de origem: "))

# Vértice de destino do grafo
destino = int(input("Informe o vértice de destino: "))
```

Abaixo um exemplo da resposta que deve ser retornada como saída após a execução do programa:

![Exemplo de saída do programa após a execução do mesmo](https://github.com/julianamlemos/AEDS_3/blob/main/Print%20ex_execu%C3%A7%C3%A3o.PNG)

### Fontes
- Notas de Aula - CSI105 Algoritmos e Estruturas de Dados III 2021/2
- [Canal Professor: Dr. George Henrique Godim da Fonseca ](https://www.youtube.com/playlist?list=PLsfh2zkrGs9lf7im2y6ZDlbIrspKBdVD3)
- [Canal Programação descomplicada - Prof. Dr André Backes](https://www.youtube.com/playlist?list=PL8iN9FQ7_jt5TITT-3c4L6xNSmQMx1T4e)
- [Hora de Codar](https://www.horadecodar.com.br/category/python/)
- [Algoritmos em Python](https://algoritmosempython.com.br/cursos/algoritmos-python/intro/)



