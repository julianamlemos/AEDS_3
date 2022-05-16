#Sistemas de Informação DECSI - UFOP
#CSI105 Algoritmos e Estruturas de Dados III 2021/2
Professor: Dr. George Henrique Godim da Fonseca

##Aluna: [Juliana Mara Lemos] (https://github.com/julianamlemos)

##Descrição
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
```json
{
  "Arquivo de origem": "toy.txt",
  "Origem": 0,
  "Destino": 3,
  "Caminho": [0, 2, 1, 4],
  "Custo": 5,
  "Tempo": 0.003s
}
```




