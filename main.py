import heapq
import random
import datetime
from collections import deque
from typing import Dict, List, Optional, Tuple
import json

# ==================== ESTRUTURAS DE DADOS ====================

class No:
    """Nó para lista ligada e árvore"""
    def __init__(self, dados):
        self.dados = dados
        self.proximo = None
        self.esquerda = None
        self.direita = None

class ListaLigada:
    """Lista ligada para histórico de ações"""
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0
    
    def inserir_inicio(self, dados):
        novo_no = No(dados)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no
        self.tamanho += 1
    
    def listar(self):
        elementos = []
        atual = self.cabeca
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos
    
    def buscar(self, criterio):
        """Busca elementos que atendem ao critério"""
        atual = self.cabeca
        resultados = []
        while atual:
            if criterio(atual.dados):
                resultados.append(atual.dados)
            atual = atual.proximo
        return resultados

class ArvoreRegiao:
    """Árvore binária para organizar regiões por prioridade"""
    def __init__(self):
        self.raiz = None
    
    def inserir(self, regiao, prioridade):
        if not self.raiz:
            self.raiz = No({'regiao': regiao, 'prioridade': prioridade})
        else:
            self._inserir_recursivo(self.raiz, regiao, prioridade)
    
    def _inserir_recursivo(self, no, regiao, prioridade):
        if prioridade < no.dados['prioridade']:
            if no.esquerda is None:
                no.esquerda = No({'regiao': regiao, 'prioridade': prioridade})
            else:
                self._inserir_recursivo(no.esquerda, regiao, prioridade)
        else:
            if no.direita is None:
                no.direita = No({'regiao': regiao, 'prioridade': prioridade})
            else:
                self._inserir_recursivo(no.direita, regiao, prioridade)
    
    def busca_binaria_regiao(self, prioridade_alvo):
        """Busca binária por prioridade na árvore"""
        return self._buscar_recursivo(self.raiz, prioridade_alvo)
    
    def _buscar_recursivo(self, no, prioridade_alvo):
        if not no:
            return None
        
        if no.dados['prioridade'] == prioridade_alvo:
            return no.dados
        elif prioridade_alvo < no.dados['prioridade']:
            return self._buscar_recursivo(no.esquerda, prioridade_alvo)
        else:
            return self._buscar_recursivo(no.direita, prioridade_alvo)
    
    def listar_em_ordem(self):
        """Percurso em ordem da árvore"""
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _em_ordem_recursivo(self, no, resultado):
        if no:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append(no.dados)
            self._em_ordem_recursivo(no.direita, resultado)

class GrafoRegioes:
    """Grafo para representar conexões entre regiões e calcular rotas otimizadas"""
    def __init__(self):
        self.vertices = {}  # região -> {região_vizinha: distancia/tempo}
        self.coordenadas = {}  # região -> (lat, lon)
    
    def adicionar_vertice(self, regiao, coordenadas=None):
        """Adiciona uma região ao grafo"""
        if regiao not in self.vertices:
            self.vertices[regiao] = {}
            if coordenadas:
                self.coordenadas[regiao] = coordenadas
    
    def adicionar_aresta(self, regiao1, regiao2, peso):
        """Adiciona conexão entre duas regiões com peso (distância/tempo)"""
        if regiao1 not in self.vertices:
            self.adicionar_vertice(regiao1)
        if regiao2 not in self.vertices:
            self.adicionar_vertice(regiao2)
        
        # Grafo não direcionado
        self.vertices[regiao1][regiao2] = peso
        self.vertices[regiao2][regiao1] = peso
    
    def dijkstra(self, origem, destino):
        """Algoritmo de Dijkstra para encontrar o menor caminho"""
        if origem not in self.vertices or destino not in self.vertices:
            return None, float('inf')
        
        # Inicialização
        distancias = {vertice: float('inf') for vertice in self.vertices}
        distancias[origem] = 0
        predecessores = {vertice: None for vertice in self.vertices}
        visitados = set()
        
        # Heap de prioridade: (distância, vértice)
        heap = [(0, origem)]
        
        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            
            if vertice_atual in visitados:
                continue
                
            visitados.add(vertice_atual)
            
            if vertice_atual == destino:
                break
            
            # Examinar vizinhos
            for vizinho, peso in self.vertices[vertice_atual].items():
                if vizinho not in visitados:
                    nova_distancia = dist_atual + peso
                    
                    if nova_distancia < distancias[vizinho]:
                        distancias[vizinho] = nova_distancia
                        predecessores[vizinho] = vertice_atual
                        heapq.heappush(heap, (nova_distancia, vizinho))
        
        # Reconstruir caminho
        caminho = []
        vertice_atual = destino
        while vertice_atual is not None:
            caminho.append(vertice_atual)
            vertice_atual = predecessores[vertice_atual]
        
        caminho.reverse()
        
        if caminho[0] != origem:
            return None, float('inf')  # Não há caminho
        
        return caminho, distancias[destino]
    
    def encontrar_rotas_multiplas(self, origem, destinos):
        """Encontra rotas otimizadas para múltiplos destinos"""
        rotas = {}
        for destino in destinos:
            caminho, distancia = self.dijkstra(origem, destino)
            rotas[destino] = {
                'caminho': caminho,
                'distancia': distancia,
                'tempo_estimado': distancia * 0.5  # Estimativa: 0.5h por unidade
            }
        return rotas
    
    def listar_conexoes(self):
        """Lista todas as conexões do grafo"""
        print("\n🗺️ MAPA DE CONEXÕES ENTRE REGIÕES:")
        print("-" * 50)
        for regiao, conexoes in self.vertices.items():
            print(f"📍 {regiao}:")
            for vizinho, peso in conexoes.items():
                print(f"   → {vizinho} (distância: {peso} unidades)")
            print()

# ==================== CLASSES PRINCIPAIS ====================

class Ocorrencia:
    """Representa uma ocorrência de queimada"""
    def __init__(self, id_ocorrencia, regiao, severidade, coordenadas, descricao=""):
        self.id = id_ocorrencia
        self.regiao = regiao
        self.severidade = severidade  # 1-10 (10 = mais severo)
        self.coordenadas = coordenadas
        self.descricao = descricao
        self.timestamp = datetime.datetime.now()
        self.status = "PENDENTE"  # PENDENTE, EM_ATENDIMENTO, RESOLVIDO
        self.equipe_responsavel = None
        self.acoes_realizadas = []
    
    def __lt__(self, other):
        # Para heap de prioridade (menor valor = maior prioridade)
        return self.severidade > other.severidade
    
    def __str__(self):
        return f"Ocorrência {self.id} - {self.regiao} (Severidade: {self.severidade})"

class Equipe:
    """Representa uma equipe de combate"""
    def __init__(self, id_equipe, nome, especializacao):
        self.id = id_equipe
        self.nome = nome
        self.especializacao = especializacao  # "TERRESTRE", "AEREA", "RESGATE"
        self.disponivel = True
        self.localizacao_atual = None
        self.historico_acoes = ListaLigada()
    
    def registrar_acao(self, acao):
        """Registra uma ação no histórico da equipe"""
        registro = {
            'timestamp': datetime.datetime.now(),
            'acao': acao,
            'equipe_id': self.id
        }
        self.historico_acoes.inserir_inicio(registro)

class SistemaIVERN:
    """Sistema principal de coordenação de resposta a queimadas"""
    
    def __init__(self):
        # Heap para priorização de ocorrências
        self.fila_prioridade = []
        
        # Pilha para ações de desfazer
        self.pilha_desfazer = deque()
        
        # Fila para processamento sequencial
        self.fila_processamento = deque()
        
        # Árvore para organização de regiões
        self.arvore_regioes = ArvoreRegiao()
        
        # Grafo para otimização de rotas
        self.grafo_regioes = GrafoRegioes()
        
        # Dicionários para busca eficiente O(1)
        self.ocorrencias_ativas = {}  # id -> Ocorrencia
        self.equipes = {}  # id -> Equipe
        self.regioes_risco = {}  # regiao -> nivel_risco
        
        # Contadores
        self.proximo_id_ocorrencia = 1
        self.proximo_id_equipe = 1
        
        # Inicializar dados de exemplo
        self._inicializar_sistema()
    
    def _inicializar_sistema(self):
        """Inicializa o sistema com dados de exemplo"""
        # Criar equipes
        self.adicionar_equipe("Brigada Florestal Alpha", "TERRESTRE")
        self.adicionar_equipe("Squadrão Aéreo Beta", "AEREA")
        self.adicionar_equipe("Equipe Resgate Gamma", "RESGATE")
        
        # Definir regiões de risco
        regioes = [
            ("Mata Atlântica Sul", 8),
            ("Cerrado Central", 6),
            ("Amazônia Norte", 9),
            ("Pantanal", 7),
            ("Caatinga", 5)
        ]
        
        for regiao, prioridade in regioes:
            self.regioes_risco[regiao] = prioridade
            self.arvore_regioes.inserir(regiao, prioridade)
        
        # Inicializar grafo de regiões
        self._inicializar_grafo_regioes()
    
    def _inicializar_grafo_regioes(self):
        """Inicializa o grafo com conexões entre regiões"""
        # Adicionar regiões com coordenadas aproximadas
        regioes_coords = {
            "Mata Atlântica Sul": (-23.5, -46.6),
            "Cerrado Central": (-15.8, -47.9),
            "Amazônia Norte": (-3.1, -60.0),
            "Pantanal": (-19.9, -56.1),
            "Caatinga": (-9.7, -40.5)
        }
        
        for regiao, coords in regioes_coords.items():
            self.grafo_regioes.adicionar_vertice(regiao, coords)
        
        # Adicionar conexões (distâncias aproximadas em unidades)
        conexoes = [
            ("Mata Atlântica Sul", "Cerrado Central", 12),
            ("Cerrado Central", "Pantanal", 8),
            ("Cerrado Central", "Amazônia Norte", 15),
            ("Amazônia Norte", "Caatinga", 20),
            ("Pantanal", "Caatinga", 18),
            ("Mata Atlântica Sul", "Pantanal", 10),
            ("Cerrado Central", "Caatinga", 14)
        ]
        
        for regiao1, regiao2, distancia in conexoes:
            self.grafo_regioes.adicionar_aresta(regiao1, regiao2, distancia)
    
    # ==================== OPERAÇÕES PRINCIPAIS ====================
    
    def inserir_nova_ocorrencia(self, regiao, severidade, coordenadas, descricao=""):
        """Insere nova ocorrência no sistema"""
        ocorrencia = Ocorrencia(
            self.proximo_id_ocorrencia,
            regiao,
            severidade,
            coordenadas,
            descricao
        )
        
        # Adicionar ao heap de prioridade
        heapq.heappush(self.fila_prioridade, ocorrencia)
        
        # Adicionar à fila de processamento
        self.fila_processamento.append(ocorrencia)
        
        # Adicionar ao dicionário para busca rápida
        self.ocorrencias_ativas[ocorrencia.id] = ocorrencia
        
        # Registrar ação na pilha de desfazer
        self.pilha_desfazer.append(('INSERIR_OCORRENCIA', ocorrencia.id))
        
        self.proximo_id_ocorrencia += 1
        
        print(f"✅ Nova ocorrência registrada: {ocorrencia}")
        return ocorrencia.id
    
    def atender_proxima_ocorrencia(self):
        """Atende a próxima ocorrência com maior prioridade"""
        if not self.fila_prioridade:
            print("❌ Não há ocorrências pendentes")
            return None
        
        # Pegar ocorrência de maior prioridade (heap)
        ocorrencia = heapq.heappop(self.fila_prioridade)
        
        # Buscar equipe disponível adequada
        equipe = self._encontrar_melhor_equipe(ocorrencia)
        
        if equipe:
            ocorrencia.status = "EM_ATENDIMENTO"
            ocorrencia.equipe_responsavel = equipe.id
            equipe.disponivel = False
            
            acao = f"Iniciado atendimento da ocorrência {ocorrencia.id} em {ocorrencia.regiao}"
            equipe.registrar_acao(acao)
            
            # Registrar na pilha de desfazer
            self.pilha_desfazer.append(('ATENDER_OCORRENCIA', ocorrencia.id, equipe.id))
            
            print(f"🚨 Atendimento iniciado: {ocorrencia} por {equipe.nome}")
            return ocorrencia.id
        else:
            # Recolocar na fila se não há equipe disponível
            heapq.heappush(self.fila_prioridade, ocorrencia)
            print("⚠️ Nenhuma equipe disponível no momento")
            return None
    
    def registrar_acoes_realizadas(self, id_ocorrencia, acoes):
        """Registra ações realizadas em uma ocorrência"""
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        ocorrencia.acoes_realizadas.extend(acoes)
        
        if ocorrencia.equipe_responsavel:
            equipe = self.equipes[ocorrencia.equipe_responsavel]
            for acao in acoes:
                equipe.registrar_acao(f"Ocorrência {id_ocorrencia}: {acao}")
        
        print(f"📝 Ações registradas para ocorrência {id_ocorrencia}")
        return True
    
    def finalizar_ocorrencia(self, id_ocorrencia):
        """Finaliza uma ocorrência e libera a equipe"""
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        ocorrencia.status = "RESOLVIDO"
        
        if ocorrencia.equipe_responsavel:
            equipe = self.equipes[ocorrencia.equipe_responsavel]
            equipe.disponivel = True
            equipe.registrar_acao(f"Finalizada ocorrência {id_ocorrencia}")
        
        # Remove da lista de ativas
        del self.ocorrencias_ativas[id_ocorrencia]
        
        print(f"✅ Ocorrência {id_ocorrencia} finalizada")
        return True
    
    def listar_historico_equipe(self, id_equipe):
        """Lista o histórico completo de uma equipe"""
        if id_equipe not in self.equipes:
            print(f"❌ Equipe {id_equipe} não encontrada")
            return []
        
        equipe = self.equipes[id_equipe]
        historico = equipe.historico_acoes.listar()
        
        print(f"\n📋 Histórico da {equipe.nome}:")
        print("-" * 50)
        for i, registro in enumerate(historico, 1):
            timestamp = registro['timestamp'].strftime("%d/%m/%Y %H:%M:%S")
            print(f"{i}. [{timestamp}] {registro['acao']}")
        
        return historico
    
    def atualizar_status_ocorrencia(self, id_ocorrencia, novo_status):
        """Atualiza o status de uma ocorrência"""
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        status_validos = ["PENDENTE", "EM_ATENDIMENTO", "RESOLVIDO"]
        if novo_status not in status_validos:
            print(f"❌ Status inválido. Use: {', '.join(status_validos)}")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        status_anterior = ocorrencia.status
        ocorrencia.status = novo_status
        
        self.pilha_desfazer.append(('ATUALIZAR_STATUS', id_ocorrencia, status_anterior))
        
        print(f"🔄 Status da ocorrência {id_ocorrencia} atualizado: {status_anterior} → {novo_status}")
        return True
    
    def gerar_relatorio_regiao(self, regiao=None):
        """Gera relatório de atendimento por região"""
        print(f"\n📊 RELATÓRIO DE ATENDIMENTO{' - ' + regiao if regiao else ''}")
        print("=" * 60)
        
        # Contar ocorrências por região
        contadores = {}
        total_ocorrencias = 0
        
        # Processar ocorrências ativas
        for ocorrencia in self.ocorrencias_ativas.values():
            if regiao is None or ocorrencia.regiao == regiao:
                if ocorrencia.regiao not in contadores:
                    contadores[ocorrencia.regiao] = {'ativas': 0, 'severidade_media': 0, 'total_severidade': 0}
                contadores[ocorrencia.regiao]['ativas'] += 1
                contadores[ocorrencia.regiao]['total_severidade'] += ocorrencia.severidade
                total_ocorrencias += 1
        
        # Calcular médias e exibir
        for reg, dados in contadores.items():
            if dados['ativas'] > 0:
                dados['severidade_media'] = dados['total_severidade'] / dados['ativas']
            
            risco = self.regioes_risco.get(reg, 0)
            print(f"🌍 {reg}:")
            print(f"   • Ocorrências ativas: {dados['ativas']}")
            print(f"   • Severidade média: {dados['severidade_media']:.1f}")
            print(f"   • Nível de risco: {risco}/10")
            print()
        
        print(f"📈 Total de ocorrências ativas: {total_ocorrencias}")
        
        # Mostrar estado das equipes
        print("\n👥 STATUS DAS EQUIPES:")
        print("-" * 30)
        for equipe in self.equipes.values():
            status = "🟢 Disponível" if equipe.disponivel else "🔴 Em atendimento"
            print(f"• {equipe.nome} ({equipe.especializacao}): {status}")
    
    def simular_chamadas_aleatorias(self, quantidade=5):
        """Simula chamadas aleatórias com severidade crescente"""
        print(f"\n🎲 SIMULANDO {quantidade} CHAMADAS ALEATÓRIAS")
        print("=" * 50)
        
        regioes_disponiveis = list(self.regioes_risco.keys())
        
        for i in range(quantidade):
            regiao = random.choice(regioes_disponiveis)
            # Severidade crescente com alguma aleatoriedade
            severidade = min(10, 3 + i + random.randint(0, 2))
            
            # Coordenadas aleatórias
            lat = round(random.uniform(-30, 5), 6)
            lon = round(random.uniform(-70, -35), 6)
            coordenadas = (lat, lon)
            
            descricoes = [
                "Fumaça avistada por morador local",
                "Foco de incêndio detectado por satélite",
                "Queimada não controlada reportada",
                "Incêndio florestal em expansão",
                "Emergência ambiental crítica"
            ]
            
            descricao = random.choice(descricoes)
            
            id_ocorrencia = self.inserir_nova_ocorrencia(regiao, severidade, coordenadas, descricao)
            
            # Simular delay entre chamadas
            if i < quantidade - 1:
                import time
                time.sleep(0.5)
    
    # ==================== OPERAÇÕES AUXILIARES ====================
    
    def adicionar_equipe(self, nome, especializacao):
        """Adiciona nova equipe ao sistema"""
        equipe = Equipe(self.proximo_id_equipe, nome, especializacao)
        self.equipes[equipe.id] = equipe
        self.proximo_id_equipe += 1
        return equipe.id
    
    def _encontrar_melhor_equipe(self, ocorrencia):
        """Encontra a melhor equipe disponível para a ocorrência"""
        equipes_disponiveis = [e for e in self.equipes.values() if e.disponivel]
        
        if not equipes_disponiveis:
            return None
        
        # Priorizar por especialização
        for equipe in equipes_disponiveis:
            if ocorrencia.severidade >= 8 and equipe.especializacao == "AEREA":
                return equipe
            elif ocorrencia.severidade >= 6 and equipe.especializacao == "TERRESTRE":
                return equipe
        
        # Retornar qualquer equipe disponível
        return equipes_disponiveis[0]
    
    def desfazer_ultima_acao(self):
        """Desfaz a última ação usando a pilha"""
        if not self.pilha_desfazer:
            print("❌ Nenhuma ação para desfazer")
            return False
        
        acao = self.pilha_desfazer.pop()
        
        if acao[0] == 'ATUALIZAR_STATUS':
            _, id_ocorrencia, status_anterior = acao
            if id_ocorrencia in self.ocorrencias_ativas:
                self.ocorrencias_ativas[id_ocorrencia].status = status_anterior
                print(f"↩️ Status da ocorrência {id_ocorrencia} revertido para {status_anterior}")
        
        # Adicionar mais casos conforme necessário
        return True
    
    def buscar_ocorrencias_por_regiao(self, regiao):
        """Busca ocorrências por região usando busca binária na árvore"""
        # Primeiro, encontrar a prioridade da região
        regiao_info = None
        for r, p in self.regioes_risco.items():
            if r == regiao:
                regiao_info = self.arvore_regioes.busca_binaria_regiao(p)
                break
        
        if not regiao_info:
            print(f"❌ Região {regiao} não encontrada")
            return []
        
        # Buscar ocorrências da região
        ocorrencias_regiao = [
            occ for occ in self.ocorrencias_ativas.values() 
            if occ.regiao == regiao
        ]
        
        print(f"🔍 Encontradas {len(ocorrencias_regiao)} ocorrências em {regiao}")
        return ocorrencias_regiao
    
    def listar_regioes_por_prioridade(self):
        """Lista regiões ordenadas por prioridade usando árvore"""
        regioes_ordenadas = self.arvore_regioes.listar_em_ordem()
        
        print("\n🗺️ REGIÕES POR PRIORIDADE:")
        print("-" * 40)
        for regiao_info in regioes_ordenadas:
            print(f"• {regiao_info['regiao']} (Prioridade: {regiao_info['prioridade']})")
    
    def status_sistema(self):
        """Exibe status geral do sistema"""
        print("\n🖥️ STATUS DO SISTEMA IVERN")
        print("=" * 40)
        print(f"• Ocorrências ativas: {len(self.ocorrencias_ativas)}")
        print(f"• Ocorrências na fila: {len(self.fila_prioridade)}")
        print(f"• Equipes disponíveis: {sum(1 for e in self.equipes.values() if e.disponivel)}")
        print(f"• Total de equipes: {len(self.equipes)}")
        print(f"• Ações na pilha de desfazer: {len(self.pilha_desfazer)}")
    
    def calcular_rota_otima(self, regiao_origem, regiao_destino):
        """Calcula a rota mais eficiente entre duas regiões"""
        caminho, distancia = self.grafo_regioes.dijkstra(regiao_origem, regiao_destino)
        
        if caminho is None:
            print(f"❌ Não há rota disponível entre {regiao_origem} e {regiao_destino}")
            return None
        
        tempo_estimado = distancia * 0.5  # 0.5 horas por unidade de distância
        
        print(f"\n🛣️ ROTA OTIMIZADA: {regiao_origem} → {regiao_destino}")
        print("=" * 60)
        print(f"📍 Caminho: {' → '.join(caminho)}")
        print(f"📏 Distância total: {distancia} unidades")
        print(f"⏱️ Tempo estimado: {tempo_estimado:.1f} horas")
        print(f"🚁 Paradas intermediárias: {len(caminho) - 2}")
        
        return {
            'caminho': caminho,
            'distancia': distancia,
            'tempo_estimado': tempo_estimado
        }
    
    def planejar_atendimento_multiplo(self, regiao_base):
        """Planeja rotas para atender múltiplas ocorrências a partir de uma base"""
        # Coletar regiões com ocorrências ativas
        regioes_com_ocorrencias = list(set(occ.regiao for occ in self.ocorrencias_ativas.values()))
        
        if not regioes_com_ocorrencias:
            print("❌ Não há ocorrências ativas para planejar rotas")
            return None
        
        if regiao_base not in self.grafo_regioes.vertices:
            print(f"❌ Região base {regiao_base} não encontrada no mapa")
            return None
        
        # Remover região base da lista se estiver presente
        if regiao_base in regioes_com_ocorrencias:
            regioes_com_ocorrencias.remove(regiao_base)
        
        if not regioes_com_ocorrencias:
            print("❌ Todas as ocorrências estão na região base")
            return None
        
        # Calcular rotas para todas as regiões
        rotas = self.grafo_regioes.encontrar_rotas_multiplas(regiao_base, regioes_com_ocorrencias)
        
        print(f"\n🗺️ PLANEJAMENTO DE ATENDIMENTO MÚLTIPLO")
        print(f"📍 Base de operações: {regiao_base}")
        print("=" * 60)
        
        # Ordenar por prioridade (distância + severidade das ocorrências)
        rotas_priorizadas = []
        for regiao, rota_info in rotas.items():
            # Calcular severidade média da região
            ocorrencias_regiao = [occ for occ in self.ocorrencias_ativas.values() if occ.regiao == regiao]
            severidade_media = sum(occ.severidade for occ in ocorrencias_regiao) / len(ocorrencias_regiao)
            
            # Score: maior severidade e menor distância = maior prioridade
            score = (severidade_media * 10) - rota_info['distancia']
            
            rotas_priorizadas.append({
                'regiao': regiao,
                'rota': rota_info,
                'ocorrencias': len(ocorrencias_regiao),
                'severidade_media': severidade_media,
                'score': score
            })
        
        # Ordenar por score (maior primeiro)
        rotas_priorizadas.sort(key=lambda x: x['score'], reverse=True)
        
        print("🎯 ORDEM DE ATENDIMENTO RECOMENDADA:")
        print("-" * 40)
        for i, info in enumerate(rotas_priorizadas, 1):
            print(f"{i}. {info['regiao']}")
            print(f"   📍 Rota: {' → '.join(info['rota']['caminho'])}")
            print(f"   📏 Distância: {info['rota']['distancia']} unidades")
            print(f"   ⏱️ Tempo: {info['rota']['tempo_estimado']:.1f}h")
            print(f"   🔥 Ocorrências: {info['ocorrencias']} (severidade média: {info['severidade_media']:.1f})")
            print(f"   🎯 Score de prioridade: {info['score']:.1f}")
            print()
        
        return rotas_priorizadas
    
    def visualizar_mapa_conexoes(self):
        """Visualiza o mapa de conexões entre regiões"""
        self.grafo_regioes.listar_conexoes()
        
        # Mostrar estatísticas do grafo
        total_regioes = len(self.grafo_regioes.vertices)
        total_conexoes = sum(len(conexoes) for conexoes in self.grafo_regioes.vertices.values()) // 2
        
        print(f"📊 ESTATÍSTICAS DO MAPA:")
        print(f"   • Total de regiões: {total_regioes}")
        print(f"   • Total de conexões: {total_conexoes}")
        print(f"   • Conectividade média: {total_conexoes * 2 / total_regioes:.1f} conexões por região")

# ==================== FUNÇÃO PRINCIPAL E MENU ====================

def menu_principal():
    """Menu interativo principal"""
    sistema = SistemaIVERN()
    
    while True:
        print("\n" + "="*60)
        print("🌿 SISTEMA IVERN - COORDENAÇÃO DE QUEIMADAS 🌿")
        print("="*60)
        print("1. 🆕 Inserir nova ocorrência")
        print("2. 🚨 Atender próxima ocorrência (maior prioridade)")
        print("3. 📝 Registrar ações realizadas")
        print("4. 📋 Listar histórico de equipe")
        print("5. 🔄 Atualizar status de ocorrência")
        print("6. 📊 Gerar relatório por região")
        print("7. 🎲 Simular chamadas aleatórias")
        print("8. ✅ Finalizar ocorrência")
        print("9. 🔍 Buscar ocorrências por região")
        print("10. 🗺️ Listar regiões por prioridade")
        print("11. ↩️ Desfazer última ação")
        print("12. 🖥️ Status do sistema")
        print("13. 🛣️ Calcular rota otimizada entre regiões")
        print("14. 🗺️ Planejar atendimento múltiplo")
        print("15. 🌐 Visualizar mapa de conexões")
        print("0. 🚪 Sair")
        print("-"*60)
        
        try:
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                print("\n--- NOVA OCORRÊNCIA ---")
                regiao = input("Região: ")
                severidade = int(input("Severidade (1-10): "))
                lat = float(input("Latitude: "))
                lon = float(input("Longitude: "))
                descricao = input("Descrição (opcional): ")
                
                sistema.inserir_nova_ocorrencia(regiao, severidade, (lat, lon), descricao)
            
            elif opcao == "2":
                sistema.atender_proxima_ocorrencia()
            
            elif opcao == "3":
                id_occ = int(input("ID da ocorrência: "))
                acoes = input("Ações realizadas (separadas por ;): ").split(';')
                acoes = [acao.strip() for acao in acoes if acao.strip()]
                sistema.registrar_acoes_realizadas(id_occ, acoes)
            
            elif opcao == "4":
                id_equipe = int(input("ID da equipe: "))
                sistema.listar_historico_equipe(id_equipe)
            
            elif opcao == "5":
                id_occ = int(input("ID da ocorrência: "))
                status = input("Novo status (PENDENTE/EM_ATENDIMENTO/RESOLVIDO): ").upper()
                sistema.atualizar_status_ocorrencia(id_occ, status)
            
            elif opcao == "6":
                regiao = input("Região (deixe vazio para todas): ").strip()
                if not regiao:
                    regiao = None
                sistema.gerar_relatorio_regiao(regiao)
            
            elif opcao == "7":
                qtd = int(input("Quantidade de chamadas para simular (padrão 5): ") or "5")
                sistema.simular_chamadas_aleatorias(qtd)
            
            elif opcao == "8":
                id_occ = int(input("ID da ocorrência para finalizar: "))
                sistema.finalizar_ocorrencia(id_occ)
            
            elif opcao == "9":
                regiao = input("Nome da região para buscar: ")
                sistema.buscar_ocorrencias_por_regiao(regiao)
            
            elif opcao == "10":
                sistema.listar_regioes_por_prioridade()
            
            elif opcao == "11":
                sistema.desfazer_ultima_acao()
            
            elif opcao == "12":
                sistema.status_sistema()
            
            elif opcao == "13":
                origem = input("Região de origem: ")
                destino = input("Região de destino: ")
                sistema.calcular_rota_otima(origem, destino)
            
            elif opcao == "14":
                base = input("Região base para planejamento: ")
                sistema.planejar_atendimento_multiplo(base)
            
            elif opcao == "15":
                sistema.visualizar_mapa_conexoes()
            
            elif opcao == "0":
                print("👋 Encerrando Sistema IVERN. Até logo!")
                break
            
            else:
                print("❌ Opção inválida!")
        
        except ValueError:
            print("❌ Entrada inválida! Tente novamente.")
        except KeyboardInterrupt:
            print("\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

# ==================== EXEMPLO DE USO AUTOMATIZADO ====================

def exemplo_automatizado():
    """Exemplo automatizado do sistema"""
    print("🚀 EXECUTANDO EXEMPLO AUTOMATIZADO DO SISTEMA IVERN")
    print("="*60)
    
    sistema = SistemaIVERN()
    
    # 1. Inserir algumas ocorrências
    print("\n1️⃣ Inserindo ocorrências...")
    sistema.inserir_nova_ocorrencia("Mata Atlântica Sul", 8, (-23.5505, -46.6333), "Incêndio de grande porte")
    sistema.inserir_nova_ocorrencia("Cerrado Central", 5, (-15.7942, -47.8822), "Queimada controlada descontrolada")
    sistema.inserir_nova_ocorrencia("Amazônia Norte", 10, (-3.1190, -60.0217), "Emergência crítica")
    
    # 2. Atender ocorrências
    print("\n2️⃣ Atendendo ocorrências por prioridade...")
    sistema.atender_proxima_ocorrencia()
    sistema.atender_proxima_ocorrencia()
    
    # 3. Registrar ações
    print("\n3️⃣ Registrando ações...")
    sistema.registrar_acoes_realizadas(1, ["Equipe deslocada", "Perímetro estabelecido", "Combate iniciado"])
    
    # 4. Relatório
    print("\n4️⃣ Gerando relatório...")
    sistema.gerar_relatorio_regiao()
    
    # 5. Histórico
    print("\n5️⃣ Consultando histórico...")
    sistema.listar_historico_equipe(1)
    
    # 6. Status do sistema
    sistema.status_sistema()
    
    # 7. Simular mais chamadas
    print("\n6️⃣ Simulando chamadas aleatórias...")
    sistema.simular_chamadas_aleatorias(3)
    
    print("\n✅ Exemplo automatizado concluído!")

if __name__ == "__main__":
    print("🌿 BEM-VINDO AO SISTEMA IVERN 🌿")
    print("Sistema de Coordenação de Resposta a Queimadas")
    print()
    
    modo = input("Escolha o modo:\n1. Menu interativo\n2. Exemplo automatizado\nOpção: ").strip()
    
    if modo == "2":
        exemplo_automatizado()
    else:
        menu_principal()