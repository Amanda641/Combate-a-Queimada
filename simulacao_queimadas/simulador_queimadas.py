import heapq
import csv
import random
from collections import deque, defaultdict

class Grafo:
    def __init__(self):
        self.adjacencias = defaultdict(list)
        self.pesos = dict()
        self.requisitos = dict()
        self.vertices = set()

    def adicionar_aresta(self, origem, destino, custo):
        self.adjacencias[origem].append(destino)
        self.adjacencias[destino].append(origem)
        self.pesos[(origem, destino)] = self.pesos[(destino, origem)] = custo
        self.vertices.update([origem, destino])

    def definir_requisitos(self, local, agua, equipes):
        self.requisitos[local] = (agua, equipes)

    def vizinhos(self, local):
        return self.adjacencias[local]

    def custo(self, origem, destino):
        return self.pesos[(origem, destino)]


class SimuladorCombate:
    def __init__(self, grafo, postos_brigada, pontos_agua, capacidade_agua, inicio_foco, equipes_por_posto=1):
        self.grafo = grafo
        self.postos_brigada = postos_brigada
        self.pontos_agua = pontos_agua + postos_brigada
        self.capacidade_maxima = capacidade_agua
        self.inicio_foco = inicio_foco
        self.status_vertices = {v: 'seguro' for v in grafo.vertices}
        self.tempo_propagacao = dict()
        self.movimentos_equipes = []
        self.total_agua_usada = 0
        self.tempo_total_operacao = 0
        self.equipes_disponiveis = {posto: equipes_por_posto for posto in postos_brigada}

    def propagar_fogo(self):
        fila = deque([(self.inicio_foco, 0)])
        self.status_vertices[self.inicio_foco] = 'em_chamas'
        self.tempo_propagacao[self.inicio_foco] = 0

        while fila:
            atual, tempo = fila.popleft()
            for vizinho in self.grafo.vizinhos(atual):
                if self.status_vertices[vizinho] == 'seguro':
                    self.status_vertices[vizinho] = 'em_chamas'
                    self.tempo_propagacao[vizinho] = tempo + 1
                    fila.append((vizinho, tempo + 1))

    def dijkstra(self, origem):
        distancias = {v: float('inf') for v in self.grafo.vertices}
        anteriores = {v: None for v in self.grafo.vertices}
        distancias[origem] = 0
        fila = [(0, origem)]

        while fila:
            distancia_atual, atual = heapq.heappop(fila)
            if distancia_atual > distancias[atual]:
                continue
            for vizinho in self.grafo.vizinhos(atual):
                novo_custo = distancia_atual + self.grafo.custo(atual, vizinho)
                if novo_custo < distancias[vizinho]:
                    distancias[vizinho] = novo_custo
                    anteriores[vizinho] = atual
                    heapq.heappush(fila, (novo_custo, vizinho))

        return distancias, anteriores

    def reconstruir_caminho(self, anteriores, destino):
        caminho = []
        atual = destino
        while atual:
            caminho.append(atual)
            atual = anteriores[atual]
        return caminho[::-1]

    def ponto_coleta_mais_proximo(self, origem):
        distancias, anteriores = self.dijkstra(origem)
        melhor_ponto = min(self.pontos_agua, key=lambda x: distancias[x])
        return melhor_ponto, self.reconstruir_caminho(anteriores, melhor_ponto)

    def executar_simulacao(self):
        self.propagar_fogo()
        for local in sorted(self.tempo_propagacao, key=lambda x: self.tempo_propagacao[x]):
            agua_necessaria, equipes_necessarias = self.grafo.requisitos.get(local, (0, 0))
            if agua_necessaria == 0 or self.status_vertices[local] != 'em_chamas':
                continue
            opcoes_postos = [(posto, self.dijkstra(posto)[0][local]) for posto in self.postos_brigada if self.equipes_disponiveis[posto] > 0]
            if not opcoes_postos:
                continue
            melhor_posto, _ = min(opcoes_postos, key=lambda x: x[1])
            distancias, anteriores = self.dijkstra(melhor_posto)
            caminho_para_foco = self.reconstruir_caminho(anteriores, local)
            agua_disponivel = self.capacidade_maxima
            caminho_completo = []
            posicao_atual = melhor_posto

            while agua_necessaria > agua_disponivel:
                ponto, caminho_ate_agua = self.ponto_coleta_mais_proximo(posicao_atual)
                caminho_completo.extend(caminho_ate_agua[1:])
                agua_disponivel = self.capacidade_maxima
                posicao_atual = ponto

            caminho_completo.extend(caminho_para_foco[1:])
            self.status_vertices[local] = 'contido'
            self.total_agua_usada += agua_necessaria
            tempo_chegada = distancias[local]
            tempo_final = max(tempo_chegada, self.tempo_propagacao[local])
            self.tempo_total_operacao = max(self.tempo_total_operacao, tempo_final)
            self.movimentos_equipes.append((melhor_posto, local, caminho_completo))
            self.equipes_disponiveis[melhor_posto] -= 1
            self.equipes_disponiveis[melhor_posto] += 1

    def gerar_relatorio(self):
        locais_salvos = [v for v in self.status_vertices if self.status_vertices[v] != 'em_chamas']
        return {
            'foco': self.inicio_foco,
            'vertices_salvos': len(locais_salvos),
            'tempo_total': self.tempo_total_operacao,
            'agua_usada': self.total_agua_usada,
            'status': self.status_vertices,
            'movimentos': self.movimentos_equipes
        }


def rodar_todas_simulacoes():
    grafo = Grafo()
    grafo.adicionar_aresta('A', 'B', 1)
    grafo.adicionar_aresta('B', 'C', 2)
    grafo.adicionar_aresta('C', 'D', 2)
    grafo.adicionar_aresta('A', 'D', 5)
    grafo.adicionar_aresta('C', 'E', 3)
    grafo.adicionar_aresta('E', 'F', 2)

    grafo.definir_requisitos('B', agua=3, equipes=1)
    grafo.definir_requisitos('C', agua=2, equipes=1)
    grafo.definir_requisitos('D', agua=4, equipes=2)
    grafo.definir_requisitos('E', agua=5, equipes=2)
    grafo.definir_requisitos('F', agua=3, equipes=1)

    postos = random.sample(list(grafo.vertices), 3)
    pontos_agua = random.sample([v for v in grafo.vertices if v not in postos], 2)
    resultados = []

    for foco in [v for v in grafo.vertices if v not in postos]:
        simulador = SimuladorCombate(grafo, postos, pontos_agua, 5, foco, equipes_por_posto=2)
        simulador.executar_simulacao()
        resultado = simulador.gerar_relatorio()
        resultados.append(resultado)

    with open("relatorio_simulacoes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Foco", "Vertices Salvos", "Tempo Total", "Agua Usada", "Movimentos"])
        for r in resultados:
            movimentos_formatados = "; ".join([f"{m[0]}->{m[1]}: {m[2]}" for m in r['movimentos']])
            writer.writerow([r['foco'], r['vertices_salvos'], r['tempo_total'], r['agua_usada'], movimentos_formatados])

    melhor = max(resultados, key=lambda x: x['vertices_salvos'])
    print(f"Melhor Simulacao:")
    print(f"Foco: {melhor['foco']}")
    print(f"Salvos: {melhor['vertices_salvos']}")
    print(f"Tempo: {melhor['tempo_total']}")
    print(f"Agua: {melhor['agua_usada']}")


if __name__ == '__main__':
    rodar_todas_simulacoes()

