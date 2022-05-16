import sys


class Grafo:

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
        if source < self.num_vet and destiny < self.num_vet:
            self.lista_adj[source].append((destiny, value))
            self.mat_adj[destiny][source] = value
            self.num_arestas += 1
        else:
            print("Aresta Inválida")

    def ler_arquivo(self, nome_arq):
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
            sys.exit("O arquivo não pôde ser encontrado")

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
        dist = [float('inf') for _ in range(len(self.lista_adj))]
        pred = [None for _ in range(len(self.lista_adj))]

        dist[s] = 0
        Q = {v for v in range(len(self.lista_adj))}

        while len(Q) != 0:
            u = self.getMenorDistancia(Q, dist)
            Q.remove(u)
            for v in self.adjacentes_peso(u):
                peso = v[1]
                vertice = v[0]
                if dist[vertice] > dist[u] + peso:
                    dist[vertice] = dist[u] + peso
                    pred[vertice] = u

        return dist, pred, 'Dijkstra'

    def bellmanFord(self, s):
        dist = [float('inf') for _ in range(len(self.lista_adj))]
        pred = [None for _ in range(len(self.lista_adj))]
        vertices = [v for v in range(len(self.lista_adj))]
        arestas = []

        for el in vertices:
            for e in self.lista_adj[el]:
                arestas.append((el, e[0], e[1]))

        dist[s] = 0

        for i in range(0, len(self.lista_adj) - 1):
            trocou = False
            for e in arestas:
                origem = e[0]
                destino = e[1]
                peso = e[2]
                if dist[destino] > dist[origem] + peso:
                    dist[destino] = dist[origem] + peso
                    pred[destino] = origem
                    trocou = True

            if trocou is False:
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

        print(f"Arquivo de origem: {nome_arq}")
        print(f"Algoritmo usado: {name}")
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