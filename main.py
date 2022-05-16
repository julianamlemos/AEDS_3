from grafo import Grafo
import time

grafo = Grafo()
arquivo = input("Informe o nome do arquivo e sua extensão (Ex: nome.txt): ")
origem = int(input("Informe o vértice de origem: "))
destino = int(input("Informe o vértice de destino: "))
start = time.process_time()
print("Processando...")

grafo.caminhoMinimo(arquivo, origem, destino)
end = time.process_time()
tempo = end- start
temp_format = "{:.3f}".format(tempo)
print("Tempo: " + temp_format + " s")

