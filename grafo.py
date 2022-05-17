from asyncio.windows_events import NULL
import sys

class Grafo:
    #None é um objeto especial que significa que o valor é NULL ou não disponível. 
    def __init__(self, num_vet=0, num_arestas=0, lista_adj=None, mat_adj=None):
        self.num_vet = num_vet
        self.num_arestas = num_arestas

        if lista_adj is None:
            self.lista_adj = [[] for _ in range(num_vet)]
        else:
            self.lista_adj = lista_adj

        if mat_adj is None:
            self.mat_adj = [[0 for _ in range(num_vet)] for _ in range(num_vet)]
        else:
            self.mat_adj = mat_adj

    def addAresta(self, source, destiny, value=1):
        """Adiciona aresta de source a destiny com peso value"""

        if source < self.num_vet and destiny < self.num_vet:
            self.lista_adj[source].append((destiny, value))
            self.mat_adj[destiny][source] = value
            self.num_arestas += 1
        else:
            print("Aresta Inválida")

    def ler_arquivo(self, nome_arq):
        """Le arquivo de grafo no formato dimacs"""

        try:
            arq = open("Datasets/" + nome_arq)
            str = arq.readline()
            str = str.split(" ")
            self.num_vet = int(str[0])
            self.num_arestas = int(str[1])
            self.lista_adj = [[] for _ in range(self.num_vet)]
            self.mat_adj = [[0 for _ in range(self.num_vet)] for _ in range(self.num_vet)]

            for i in range(self.num_arestas):
                str = arq.readline()
                str = str.split(" ")
                source = int(str[0])
                destiny = int(str[1])
                value = int(str[2])
                self.addAresta(source, destiny, value)
        except IOError:
            print("O arquivo não pôde ser encontrado")

  
    def adjacentes_peso(self, u):
        """Retorna a lista dos vertices adjacentes a u no formato (v, w)"""
        return self.lista_adj[u]
    
    def ponderado(self) -> bool:
        for v in self.mat_adj:
            for i in v:
                if i != 1 and i != 0:
                    return True

        return False

    def arestaNegativa(self) -> bool:
        for v in self.mat_adj:
            for i in v:
                if i < 0:
                    return True

        return False

    @staticmethod
    def getMenorDistancia(lista_v, lista_dist):
        menorDistancia = float('inf')
        vertice = None

        for v in lista_v:
            if lista_dist[v] < menorDistancia:
                menorDistancia = lista_dist[v]
                vertice = v

        return vertice
    
    def busca_largura_menor_dist(self, s):
        dist = [float('inf') for _ in range(len(self.lista_adj))]
        pred = [None for _ in range(len(self.lista_adj))]
      
        Q = [s]
        dist[s] = 0

        while len(Q) != 0:
            u = Q.pop(0)
            for (v, w) in self.lista_adj[u]:
                if dist[v] == float('inf'):
                    Q.append(v)
                    dist[v] = dist[u] + 1
                    pred[v] = u

        return dist, pred, 'Busca em largura'

    def dijkstra(self, s):
    #para grafos ponderados com arestas de peso positivo

        dist = [float('inf') for _ in range(len(self.lista_adj))]
        pred = [None for _ in range(len(self.lista_adj))]

        dist[s] = 0 #Distancia inicializada como 0
        Q = {v for v in range(len(self.lista_adj))} #inicialização da lista como a lista de todos os vértices do grafo

        #laço principal - executa enquanto a lista não for nula
        while len(Q) != NULL:
            u = self.getMenorDistancia(Q, dist) #Salvando o elemento com a menor distancia na variável u
            Q.remove(u) #remove o elemento u salvo da lista Q

            #Processamento do vértice u
            for v in self.adjacentes_peso(u):
                peso = v[1]
                vertice = v[0]

                """caso a distancia do vértice for maior que a distancia de u + o peso da aresta de u até o vértice
                então temos um novo melhor caminho para o vértice a partir de u"""

                if dist[vertice] > dist[u] + peso:  
                    dist[vertice] = dist[u] + peso #distancia é atualizada
                    pred[vertice] = u #predecessor do vértice é atualizado

        return dist, pred, 'Dijkstra'

    def bellmanFord(self, s):
    #para grafos ponderados com arestas que contenham peso negativo, implementação melhorada

        dist = [float('inf') for _ in range(len(self.lista_adj))]
        pred = [None for _ in range(len(self.lista_adj))]
        vertices = [v for v in range(len(self.lista_adj))]
        arestas = []

        for el in vertices:
            for e in self.lista_adj[el]:
                arestas.append((el, e[0], e[1]))

        dist[s] = 0

        #Laço principal que será executado até o número de vértices -1 vezes
        for i in range(0, len(self.lista_adj) - 1):
            trocou = False #semáforo inicializado como false
            #Examina cada aresta e atualiza caso encontre uma melhor iteração
            for e in arestas:
                origem = e[0]
                destino = e[1]
                peso = e[2]
                if dist[destino] > dist[origem] + peso:
                    dist[destino] = dist[origem] + peso
                    pred[destino] = origem
                    trocou = True #Caso haja atualização

            if trocou is False: #Encerra prematuramente caso o semáforo continue como False
                break

        return dist, pred, 'Bellman Ford'

    @staticmethod
    def formatData(nome_arq, u, v, data: tuple):
        dist = data.__getitem__(0)
        pred = data.__getitem__(1)
        name = data.__getitem__(2)

        caminho = [v]
        dist = dist[v]

        i = pred[v]
        while i in pred:
            if i is None:
                break
            caminho.append(i)
            i = pred[i]

        caminho.reverse()

        print(f"Arquivo escolhido: {nome_arq}")
        print(f"Algoritmo utilizado: {name}")
        print(" ")
        print(f"Origem: {u}")
        print(f"Destino: {v}")
        print(f"Caminho: {caminho}")
        print(f"Custo: {dist}")

    def caminhoMinimo(self, nome_arq, u, v):
        self.ler_arquivo(nome_arq)

        if not self.ponderado():
            return self.formatData(nome_arq, u, v, self.busca_largura_menor_dist(u))

        if self.arestaNegativa():
            return self.formatData(nome_arq, u, v, self.bellmanFord(u))

        return self.formatData(nome_arq, u, v, self.dijkstra(u))
