import pandas as pd
import sys

class Graph:

    def __init__(self, num_vet=0, num_edg=0, mat_adj=None, list_adj: list = None): #iniciando a matriz
        self.num_vet = num_vet
        self.num_edg = num_edg

        if mat_adj is None:
            self.mat_adj = [[0 for _ in range(num_vet)] for _ in range(num_vet)]
        else:
            self.mat_adj = mat_adj

        if list_adj is None:
            self.list_adj = [[] for _ in range(num_vet)]
        else:
            self.list_adj = list_adj

        self.subjects_index = {}
        self.teachers_index = {}
        self.num_of_classes = None
        self.edges_list = []
        self.away_teachers = []

    def reset(self, num_vet=0, num_edg=0, mat_adj: list = None, list_adj: list = None) -> None:
  
        self.num_vet = num_vet
        self.num_edg = num_edg

        if mat_adj is None:
            self.mat_adj = [[0 for _ in range(num_vet)] for _ in range(num_vet)]
        else:
            self.mat_adj = mat_adj

        if list_adj is None:
            self.list_adj = [[] for _ in range(num_vet)]
        else:
            self.list_adj = list_adj

        self.subjects_index = {}
        self.teachers_index = {}
        self.num_of_classes = None
        self.edges_list = []
        self.away_teachers = []

    def addEdge(self, source, sink, capacity=float("inf"), flow=0) -> None: #adicionando aresta

        if source < self.num_vet and sink < self.num_vet:
            self.mat_adj[source][sink] = [flow, capacity]
            self.list_adj[source].append((sink, [flow, capacity]))
            self.num_edg += 1
        else:
            sys.exit("Aresta inválida")

    def removeEdge(self, source, sink) -> None: #removendo aresta

        if source < self.num_vet and sink < self.num_vet:
            if self.mat_adj[source][sink] != 0:
                self.num_edg -= 1
                self.mat_adj[source][sink] = 0

                for (v, w) in self.list_adj[source]:
                    if v == sink:
                        self.list_adj[source].remove((v, w))
                        break

                self.num_edg += 1
        else:
            sys.exit("Aresta inválida")

    def setEdgesList(self) -> None:

        for i in range(0, len(self.mat_adj)):
            for j in range(0, len(self.mat_adj[i])):
                if self.mat_adj[i][j] != 0:
                    [flow, _] = self.mat_adj[i][j]
                    self.edges_list.append((i, j, flow))

    @staticmethod
    def cleanSubjects(subjects) -> list:

        new_subjects = []
        for item in subjects:
            new_subjects.append([subject for subject in item if str(subject) != 'nan'])

        new_subjects.pop(-1)

        return new_subjects

    def readTeachers(self, filename: str) -> tuple: #lendo professores

        try:
            df = pd.read_csv("C:/Users/camar/Downloads/AEDS3/TP2/base/" + filename, sep=";")

            teachers = df.iloc[:, 0].dropna().values.tolist() 

            subjects_offered = df.iloc[:, 1].values.tolist()

            subjects_offered.pop(-1) 

            subjects = df.iloc[:, [2, 3, 4, 5, 6]].values.tolist() 

            subjects = self.cleanSubjects(subjects)  

            return teachers, subjects_offered, subjects

        except IOError:
            sys.exit("Arquivo não existente na pasta /base")

    def readSubjects(self, filename: str) -> tuple: #lendo disciplinas
    
        try:
            df = pd.read_csv("C:/Users/camar/Downloads/AEDS3/TP2/base/" + filename, sep=";")

            data = df.iloc[:, ].values.tolist() 

            num_of_classes = data.pop(-1)[2] 

            self.num_of_classes = num_of_classes

            total_of_subjects = len(df.iloc[:, 0].dropna().values.tolist()) 

            return data, num_of_classes, total_of_subjects

        except IOError:
            sys.exit("Arquivo não existente na pasta /base")

    def setTeachersAndSubjectsIndexes(self, subjects_initial_vertex: int, subjects_info: list, teachers_data: tuple) -> None:

        (teachers, num_of_subject_offered, subjects_offered) = teachers_data

        for i in range(0, len(teachers)):
            self.teachers_index[i + 1] = (teachers[i], num_of_subject_offered[i], subjects_offered[i])

        for j in range(subjects_initial_vertex, self.num_vet - 1):
            for subject in subjects_info:
                self.subjects_index[j] = subject
                subjects_info.remove(subject)
                break

    def setSourceEdges(self, teachers: list, subjects_offered: list) -> None:

        source = self.mat_adj[0]
        copy = [0]
        copy = copy + subjects_offered.copy()

        for i in range(0, len(teachers) + 1):
            sink_teacher = i
            teacher_capacity = copy[i]
            self.addEdge(source[i], sink_teacher, teacher_capacity)

    def setSinkEdges(self, initial_vertex: int, subjects_info: list) -> None:

        subjects_capacities = [c[2] for c in subjects_info]
        sink = self.num_vet - 1
        subject_capacity = None

        for i in range(initial_vertex, self.num_vet - 1):
            source_subject = i
            for c in subjects_capacities:
                subject_capacity = c
                subjects_capacities.remove(c)
                break
            self.addEdge(source_subject, sink, subject_capacity)

    def setTeachersToSubjectsEdges(self) -> None:

        teachers_indexes = self.teachers_index
        subjects_indexes = self.subjects_index

        flow = [0, 3, 5, 8, 10]

        for key, (name, classes_offered, [*subjects]) in teachers_indexes.items():
            total_classes_offered = 0
            for subjectKey, (subjectId, _, classes) in subjects_indexes.items():
                if total_classes_offered == len(subjects):
                    break
                if classes_offered == 0:
                    self.away_teachers.append(name)
                    break
                if subjectId in subjects:
                    if subjectId == 'CSI000': 
                        classes = 1
                    self.addEdge(key, subjectKey, classes, flow[subjects.index(subjectId)])
                    total_classes_offered += 1

    def setInitialData(self, teachers_data: tuple, subjects_data: tuple) -> None:

        (teachers, subjects_offered, subjects) = teachers_data
        (subjects_info, num_of_classes, total_of_subjects) = subjects_data

        self.num_vet = 2 + len(teachers) + total_of_subjects

        self.mat_adj = [[0 for _ in range(self.num_vet)] for _ in range(self.num_vet)]
        self.list_adj = [[] for _ in range(self.num_vet)]

        self.setSourceEdges(teachers, subjects_offered)

        self.setSinkEdges(len(teachers) + 1, subjects_info)

        self.setTeachersAndSubjectsIndexes(len(teachers) + 1, subjects_info, teachers_data)

        self.setTeachersToSubjectsEdges()
     
        self.setEdgesList()

    def bellmanFord(self, s: int, v: int) -> list:

        dist = [float("inf") for _ in range(len(self.list_adj))]
        pred = [None for _ in range(len(self.list_adj))]
        edges = self.edges_list

        dist[s] = 0

        for i in range(0, len(self.list_adj) - 1):
            trade = False
            for source, sink, flow in edges:  
                if dist[sink] > dist[source] + flow:
                    dist[sink] = dist[source] + flow
                    pred[sink] = source
                    trade = True

            if trade is False:
                break

        shortest_path = [v]
        i = pred[v]
        while i in pred:
            if i is None:
                break
            shortest_path.append(i)
            i = pred[i]

        if len(shortest_path) == 1:
            shortest_path.clear()
            return shortest_path

        shortest_path.reverse()

        return shortest_path

    def getFlowByVertex(self) -> list:

        b = [self.num_of_classes]

        for _, [_, flow, [*_]] in self.teachers_index.items():
            b.append(flow)

        for _, [_, _, flow] in self.subjects_index.items():
            b.append(flow)

        b.append(-self.num_of_classes)

        return b

    def getFlowAndCapacityOfEachEdge(self) -> tuple:

        flow_of_edge = [[0 for _ in range(len(self.mat_adj))] for _ in range(len(self.mat_adj))]
        capacity_of_edges = [[0 for _ in range(len(self.mat_adj))] for _ in range(len(self.mat_adj))]

        for i in range(0, len(self.mat_adj)):
            for j in range(0, len(self.mat_adj[i])):
                if self.mat_adj[i][j] != 0:
                    [flow, capacity] = self.mat_adj[i][j]
                    flow_of_edge[i][j] = flow
                    capacity_of_edges[i][j] = capacity

        return flow_of_edge, capacity_of_edges

    def successfulShortestPaths(self, s: int, t: int) -> list:

        F = [[0 for _ in range(len(self.mat_adj))] for _ in range(len(self.mat_adj))]

        flow_for_vertex = self.getFlowByVertex()  
        flow_of_edges, capacity_of_edges = self.getFlowAndCapacityOfEachEdge()

        shortest_path = self.bellmanFord(s, t)  
        while len(shortest_path) != 0 and flow_for_vertex[s] != 0:
            max_flow = float("inf")
            for i in range(1, len(shortest_path)):  
                u = shortest_path[i - 1]  
                v = shortest_path[i]  

                if capacity_of_edges[u][v] < max_flow:  
                    max_flow = capacity_of_edges[u][v]  

            for i in range(1, len(shortest_path)):  
                u = shortest_path[i - 1]  
                v = shortest_path[i]  
                F[u][v] += max_flow  
                capacity_of_edges[u][v] -= max_flow  

                if capacity_of_edges[u][v] == 0:  
                    self.mat_adj[u][v] = 0  
                    self.edges_list.remove((u, v, flow_of_edges[u][v]))  

                if self.mat_adj[v][u] == 0:  
                    self.mat_adj[v][u] = 1  
                    self.edges_list.append((v, u, -flow_of_edges[u][v]))  
                    flow_of_edges[v][u] = -flow_of_edges[u][v]  

                capacity_of_edges[v][u] += max_flow  

                if F[v][u] != 0:  
                    F[v][u] -= max_flow  

            flow_for_vertex[s] -= max_flow  
            flow_for_vertex[t] += max_flow  

            shortest_path = self.bellmanFord(s, t)  

        return F

    def formatData(self, final_matrix: list) -> None:

        teachers_keys = self.teachers_index.keys()
        subjects_keys = self.subjects_index.keys()
        edges = []
        costs = [0, 3, 5, 8, 10]  
        total_cost = 0
        total_classes = 0

        for i in range(0, len(final_matrix)):
            for j in range(0, len(final_matrix[i])):
                if final_matrix[i][j] != 0:  
                    if i in teachers_keys or j in subjects_keys:
                        edges.append((i, j, final_matrix[i][j])) 

        print("\n")
        print("{:<20} {:<20} {:<40} {:<40} {:<40}".format('Teacher', 'Subject', 'Name', 'Classes', 'Cost'))
        for teacher, subject, classes in edges:

            subject_id = self.subjects_index[subject][0]
            teacher_subjects = self.teachers_index[teacher][2]
            subject_cost = teacher_subjects.index(subject_id)

            print("{:<20} {:<20} {:<40} {:<40} {:<40}"
                  .format(self.teachers_index[teacher][0], 
                          subject_id,  
                          self.subjects_index[subject][1],  
                          classes,  
                          costs[subject_cost] * classes))  

            total_cost += costs[subject_cost] * classes  
            total_classes += classes  

        print(f"\nO custo total é {total_cost}")
        print(f"Total de turmas alocadas: {total_classes}")

        if len(self.away_teachers) != 0:
            print(f"\nEsses professores não ofertam nenhuma disciplina:")
            print(*self.away_teachers, sep=", ")
        else:
            print("\nTodos os professores oferecem pelo menos uma disciplina")

    def menu(self) -> None:

        print("\nMENU\nEscolha uma das opções abaixo para iniciar:\n")
        option = None
        
        while option != '2':

            option = input("1 - Para iniciar\n"
                           "2 - Para sair da aplicação\n")

            if option == '1':
                self.run("professores.csv", "disciplinas.csv")
                self.reset()

            elif option == '2':
                print("\nSaindo...\n Tchau! :D")
                break

            else:
                print("\nOpção inválida. \nPor favor, escolha uma das opções válidas.")

    def run(self, teachers_file: str, subjects_file: str) -> None:

        self.setInitialData(self.readTeachers(teachers_file), self.readSubjects(subjects_file))
        self.formatData(self.successfulShortestPaths(0, self.num_vet - 1))