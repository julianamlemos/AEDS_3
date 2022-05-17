from grafo import Grafo
import time

grafo = Grafo()
arquivo = input("\nInforme o nome do arquivo e sua extensão (Ex: nome.txt): ")
origem = int(input("Informe o vértice de origem: "))
destino = int(input("Informe o vértice de destino: "))
start = time.process_time()
print("\nProcessando...\n")

grafo.caminhoMinimo(arquivo, origem, destino)
end = time.process_time()
tempo = end- start
temp_format = "{:.3f}".format(tempo) #formatação para o tempo aparecer com 3 casas decimais
print("Tempo: " + temp_format + "s\n")

