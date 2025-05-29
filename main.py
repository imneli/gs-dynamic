import heapq
import random
import datetime
from collections import deque
from typing import Dict, List, Optional, Tuple

class No:
    def __init__(self, dados):
        self.dados, self.proximo, self.esquerda, self.direita = dados, None, None, None

class ListaLigada:
    def __init__(self):
        self.cabeca, self.tamanho = None, 0
    
    def inserir_inicio(self, dados):
        novo_no = No(dados)
        novo_no.proximo, self.cabeca, self.tamanho = self.cabeca, novo_no, self.tamanho + 1
    
    def listar(self):
        elementos, atual = [], self.cabeca
        while atual:
            elementos.append(atual.dados)
            atual = atual.proximo
        return elementos

class ArvoreRegiao:
    def __init__(self):
        self.raiz = None
    
    def inserir(self, regiao, prioridade):
        if not self.raiz:
            self.raiz = No({'regiao': regiao, 'prioridade': prioridade})
        else:
            self._inserir_recursivo(self.raiz, regiao, prioridade)
    
    def _inserir_recursivo(self, no, regiao, prioridade):
        lado = 'esquerda' if prioridade < no.dados['prioridade'] else 'direita'
        if getattr(no, lado) is None:
            setattr(no, lado, No({'regiao': regiao, 'prioridade': prioridade}))
        else:
            self._inserir_recursivo(getattr(no, lado), regiao, prioridade)
    
    def busca_binaria_regiao(self, prioridade_alvo):
        return self._buscar_recursivo(self.raiz, prioridade_alvo)
    
    def _buscar_recursivo(self, no, prioridade_alvo):
        if not no: return None
        if no.dados['prioridade'] == prioridade_alvo: return no.dados
        return self._buscar_recursivo(no.esquerda if prioridade_alvo < no.dados['prioridade'] else no.direita, prioridade_alvo)
    
    def listar_em_ordem(self):
        resultado = []
        self._em_ordem_recursivo(self.raiz, resultado)
        return resultado
    
    def _em_ordem_recursivo(self, no, resultado):
        if no:
            self._em_ordem_recursivo(no.esquerda, resultado)
            resultado.append(no.dados)
            self._em_ordem_recursivo(no.direita, resultado)

class GrafoRegioes:
    def __init__(self):
        self.vertices, self.coordenadas = {}, {}
    
    def adicionar_vertice(self, regiao, coordenadas=None):
        if regiao not in self.vertices:
            self.vertices[regiao] = {}
            if coordenadas: self.coordenadas[regiao] = coordenadas
    
    def adicionar_aresta(self, regiao1, regiao2, peso):
        self.adicionar_vertice(regiao1), self.adicionar_vertice(regiao2)
        self.vertices[regiao1][regiao2] = self.vertices[regiao2][regiao1] = peso
    
    def dijkstra(self, origem, destino):
        if origem not in self.vertices or destino not in self.vertices: return None, float('inf')
        
        distancias, predecessores, visitados = {v: float('inf') for v in self.vertices}, {v: None for v in self.vertices}, set()
        distancias[origem], heap = 0, [(0, origem)]
        
        while heap:
            dist_atual, vertice_atual = heapq.heappop(heap)
            if vertice_atual in visitados: continue
            visitados.add(vertice_atual)
            if vertice_atual == destino: break
            
            for vizinho, peso in self.vertices[vertice_atual].items():
                if vizinho not in visitados and (nova_dist := dist_atual + peso) < distancias[vizinho]:
                    distancias[vizinho], predecessores[vizinho] = nova_dist, vertice_atual
                    heapq.heappush(heap, (nova_dist, vizinho))
        
        caminho, vertice_atual = [], destino
        while vertice_atual is not None:
            caminho.append(vertice_atual)
            vertice_atual = predecessores[vertice_atual]
        
        return (caminho[::-1], distancias[destino]) if caminho and caminho[0] == origem else (None, float('inf'))
    
    def listar_conexoes(self):
        print("\n🗺️ MAPA DE CONEXÕES ENTRE REGIÕES:\n" + "-" * 50)
        for regiao, conexoes in self.vertices.items():
            print(f"📍 {regiao}:")
            for vizinho, peso in conexoes.items():
                print(f"   → {vizinho} (distância: {peso} unidades)")
            print()

class Ocorrencia:
    def __init__(self, id_ocorrencia, regiao, severidade, coordenadas, descricao=""):
        self.id, self.regiao, self.severidade = id_ocorrencia, regiao, severidade
        self.coordenadas, self.descricao = coordenadas, descricao
        self.timestamp, self.status = datetime.datetime.now(), "PENDENTE"
        self.equipe_responsavel, self.acoes_realizadas = None, []
    
    def __lt__(self, other): return self.severidade > other.severidade
    def __str__(self): return f"Ocorrência {self.id} - {self.regiao} (Severidade: {self.severidade})"

class Equipe:
    def __init__(self, id_equipe, nome, especializacao):
        self.id, self.nome, self.especializacao = id_equipe, nome, especializacao
        self.disponivel, self.localizacao_atual, self.historico_acoes = True, None, ListaLigada()
    
    def registrar_acao(self, acao):
        self.historico_acoes.inserir_inicio({
            'timestamp': datetime.datetime.now(),
            'acao': acao,
            'equipe_id': self.id
        })

class SistemaIVERN:
    def __init__(self):
        self.fila_prioridade, self.pilha_desfazer, self.fila_processamento = [], deque(), deque()
        self.arvore_regioes, self.grafo_regioes = ArvoreRegiao(), GrafoRegioes()
        self.ocorrencias_ativas, self.equipes, self.regioes_risco = {}, {}, {}
        self.proximo_id_ocorrencia, self.proximo_id_equipe = 1, 1
        self._inicializar_sistema()
    
    def _inicializar_sistema(self):
        for nome, esp in [("Brigada Florestal Alpha", "TERRESTRE"), ("Squadrão Aéreo Beta", "AEREA"), ("Equipe Resgate Gamma", "RESGATE")]:
            self.adicionar_equipe(nome, esp)
        
        for regiao, prioridade in [("Mata Atlântica Sul", 8), ("Cerrado Central", 6), ("Amazônia Norte", 9), ("Pantanal", 7), ("Caatinga", 5)]:
            self.regioes_risco[regiao], self.arvore_regioes.inserir(regiao, prioridade)
        
        regioes_coords = {
            "Mata Atlântica Sul": (-23.5, -46.6),
            "Cerrado Central": (-15.8, -47.9),
            "Amazônia Norte": (-3.1, -60.0),
            "Pantanal": (-19.9, -56.1),
            "Caatinga": (-9.7, -40.5)
        }
        
        for regiao, coords in regioes_coords.items():
            self.grafo_regioes.adicionar_vertice(regiao, coords)
        
        for regiao1, regiao2, distancia in [
            ("Mata Atlântica Sul", "Cerrado Central", 12),
            ("Cerrado Central", "Pantanal", 8),
            ("Cerrado Central", "Amazônia Norte", 15),
            ("Amazônia Norte", "Caatinga", 20),
            ("Pantanal", "Caatinga", 18),
            ("Mata Atlântica Sul", "Pantanal", 10),
            ("Cerrado Central", "Caatinga", 14)
        ]:
            self.grafo_regioes.adicionar_aresta(regiao1, regiao2, distancia)
    
    def inserir_nova_ocorrencia(self, regiao, severidade, coordenadas, descricao=""):
        ocorrencia = Ocorrencia(self.proximo_id_ocorrencia, regiao, severidade, coordenadas, descricao)
        heapq.heappush(self.fila_prioridade, ocorrencia)
        self.fila_processamento.append(ocorrencia)
        self.ocorrencias_ativas[ocorrencia.id] = ocorrencia
        self.pilha_desfazer.append(('INSERIR_OCORRENCIA', ocorrencia.id))
        self.proximo_id_ocorrencia += 1
        print(f"✅ Nova ocorrência registrada: {ocorrencia}")
        return ocorrencia.id
    
    def atender_proxima_ocorrencia(self):
        if not self.fila_prioridade:
            print("❌ Não há ocorrências pendentes")
            return None
        
        ocorrencia = heapq.heappop(self.fila_prioridade)
        if not (equipe := self._encontrar_melhor_equipe(ocorrencia)):
            heapq.heappush(self.fila_prioridade, ocorrencia)
            print("⚠️ Nenhuma equipe disponível no momento")
            return None
        
        ocorrencia.status, ocorrencia.equipe_responsavel = "EM_ATENDIMENTO", equipe.id
        equipe.disponivel = False
        equipe.registrar_acao(f"Iniciado atendimento da ocorrência {ocorrencia.id} em {ocorrencia.regiao}")
        self.pilha_desfazer.append(('ATENDER_OCORRENCIA', ocorrencia.id, equipe.id))
        print(f"🚨 Atendimento iniciado: {ocorrencia} por {equipe.nome}")
        return ocorrencia.id
    
    def _encontrar_melhor_equipe(self, ocorrencia):
        equipes_disponiveis = [e for e in self.equipes.values() if e.disponivel]
        return next((e for e in equipes_disponiveis if 
                   (ocorrencia.severidade >= 8 and e.especializacao == "AEREA") or
                   (ocorrencia.severidade >= 6 and e.especializacao == "TERRESTRE")), 
                   equipes_disponiveis[0] if equipes_disponiveis else None)

    def registrar_acoes_realizadas(self, id_ocorrencia, acoes):
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        ocorrencia.acoes_realizadas.extend(acoes)
        
        if ocorrencia.equipe_responsavel:
            for acao in acoes:
                self.equipes[ocorrencia.equipe_responsavel].registrar_acao(f"Ocorrência {id_ocorrencia}: {acao}")
        
        print(f"📝 Ações registradas para ocorrência {id_ocorrencia}")
        return True
    
    def finalizar_ocorrencia(self, id_ocorrencia):
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        ocorrencia.status = "RESOLVIDO"
        
        if ocorrencia.equipe_responsavel:
            equipe = self.equipes[ocorrencia.equipe_responsavel]
            equipe.disponivel, equipe.registrar_acao = True, f"Finalizada ocorrência {id_ocorrencia}"
        
        del self.ocorrencias_ativas[id_ocorrencia]
        print(f"✅ Ocorrência {id_ocorrencia} finalizada")
        return True
    
    def listar_historico_equipe(self, id_equipe):
        if id_equipe not in self.equipes:
            print(f"❌ Equipe {id_equipe} não encontrada")
            return []
        
        historico = self.equipes[id_equipe].historico_acoes.listar()
        print(f"\n📋 Histórico da {self.equipes[id_equipe].nome}:\n" + "-" * 50)
        for i, registro in enumerate(historico, 1):
            print(f"{i}. [{registro['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}] {registro['acao']}")
        return historico
    
    def atualizar_status_ocorrencia(self, id_ocorrencia, novo_status):
        if id_ocorrencia not in self.ocorrencias_ativas:
            print(f"❌ Ocorrência {id_ocorrencia} não encontrada")
            return False
        
        if novo_status not in ["PENDENTE", "EM_ATENDIMENTO", "RESOLVIDO"]:
            print("❌ Status inválido. Use: PENDENTE, EM_ATENDIMENTO ou RESOLVIDO")
            return False
        
        ocorrencia = self.ocorrencias_ativas[id_ocorrencia]
        self.pilha_desfazer.append(('ATUALIZAR_STATUS', id_ocorrencia, ocorrencia.status))
        ocorrencia.status = novo_status
        print(f"🔄 Status da ocorrência {id_ocorrencia} atualizado: {ocorrencia.status}")
        return True
    
    def gerar_relatorio_regiao(self, regiao=None):
        print(f"\n📊 RELATÓRIO DE ATENDIMENTO{' - ' + regiao if regiao else ''}\n" + "=" * 60)
        contadores = {}
        
        for ocorrencia in self.ocorrencias_ativas.values():
            if regiao is None or ocorrencia.regiao == regiao:
                if ocorrencia.regiao not in contadores:
                    contadores[ocorrencia.regiao] = {'ativas': 0, 'total_severidade': 0}
                contadores[ocorrencia.regiao]['ativas'] += 1
                contadores[ocorrencia.regiao]['total_severidade'] += ocorrencia.severidade
        
        for reg, dados in contadores.items():
            risco = self.regioes_risco.get(reg, 0)
            print(f"🌍 {reg}:\n   • Ocorrências ativas: {dados['ativas']}\n   • Severidade média: {dados['total_severidade']/dados['ativas']:.1f}\n   • Nível de risco: {risco}/10\n")
        
        print(f"📈 Total de ocorrências ativas: {sum(d['ativas'] for d in contadores.values())}")
        print("\n👥 STATUS DAS EQUIPES:\n" + "-" * 30)
        for equipe in self.equipes.values():
            print(f"• {equipe.nome} ({equipe.especializacao}): {'🟢 Disponível' if equipe.disponivel else '🔴 Em atendimento'}")
    
    def simular_chamadas_aleatorias(self, quantidade=5):
        print(f"\n🎲 SIMULANDO {quantidade} CHAMADAS ALEATÓRIAS\n" + "=" * 50)
        for i in range(quantidade):
            regiao = random.choice(list(self.regioes_risco.keys()))
            severidade = min(10, 3 + i + random.randint(0, 2))
            coordenadas = (round(random.uniform(-30, 5), 6), round(random.uniform(-70, -35), 6))
            descricao = random.choice([
                "Fumaça avistada por morador local",
                "Foco de incêndio detectado por satélite",
                "Queimada não controlada reportada",
                "Incêndio florestal em expansão",
                "Emergência ambiental crítica"
            ])
            self.inserir_nova_ocorrencia(regiao, severidade, coordenadas, descricao)
    
    def adicionar_equipe(self, nome, especializacao):
        equipe = Equipe(self.proximo_id_equipe, nome, especializacao)
        self.equipes[equipe.id], self.proximo_id_equipe = equipe, self.proximo_id_equipe + 1
        return equipe.id
    
    def desfazer_ultima_acao(self):
        if not self.pilha_desfazer:
            print("❌ Nenhuma ação para desfazer")
            return False
        
        acao = self.pilha_desfazer.pop()
        if acao[0] == 'ATUALIZAR_STATUS' and acao[1] in self.ocorrencias_ativas:
            self.ocorrencias_ativas[acao[1]].status = acao[2]
            print(f"↩️ Status da ocorrência {acao[1]} revertido para {acao[2]}")
        return True
    
    def buscar_ocorrencias_por_regiao(self, regiao):
        ocorrencias_regiao = [occ for occ in self.ocorrencias_ativas.values() if occ.regiao == regiao]
        print(f"🔍 Encontradas {len(ocorrencias_regiao)} ocorrências em {regiao}")
        return ocorrencias_regiao
    
    def listar_regioes_por_prioridade(self):
        print("\n🗺️ REGIÕES POR PRIORIDADE:\n" + "-" * 40)
        for regiao_info in self.arvore_regioes.listar_em_ordem():
            print(f"• {regiao_info['regiao']} (Prioridade: {regiao_info['prioridade']})")
    
    def status_sistema(self):
        print("\n🖥️ STATUS DO SISTEMA IVERN\n" + "=" * 40)
        print(f"• Ocorrências ativas: {len(self.ocorrencias_ativas)}\n• Ocorrências na fila: {len(self.fila_prioridade)}")
        print(f"• Equipes disponíveis: {sum(1 for e in self.equipes.values() if e.disponivel)}\n• Total de equipes: {len(self.equipes)}")
        print(f"• Ações na pilha de desfazer: {len(self.pilha_desfazer)}")
    
    def calcular_rota_otima(self, regiao_origem, regiao_destino):
        caminho, distancia = self.grafo_regioes.dijkstra(regiao_origem, regiao_destino)
        if caminho is None:
            print(f"❌ Não há rota disponível entre {regiao_origem} e {regiao_destino}")
            return None
        
        print(f"\n🛣️ ROTA OTIMIZADA: {regiao_origem} → {regiao_destino}\n" + "=" * 60)
        print(f"📍 Caminho: {' → '.join(caminho)}\n📏 Distância total: {distancia} unidades")
        print(f"⏱️ Tempo estimado: {distancia * 0.5:.1f} horas\n🚁 Paradas intermediárias: {len(caminho) - 2}")
        return {'caminho': caminho, 'distancia': distancia, 'tempo_estimado': distancia * 0.5}
    
    def planejar_atendimento_multiplo(self, regiao_base):
        regioes_com_ocorrencias = list(set(occ.regiao for occ in self.ocorrencias_ativas.values() if occ.regiao != regiao_base))
        if not regioes_com_ocorrencias:
            print("❌ Não há ocorrências ativas para planejar rotas")
            return None
        
        if regiao_base not in self.grafo_regioes.vertices:
            print(f"❌ Região base {regiao_base} não encontrada no mapa")
            return None
        
        rotas = {regiao: {'rota': self.grafo_regioes.dijkstra(regiao_base, regiao)} for regiao in regioes_com_ocorrencias}
        rotas_priorizadas = []
        
        for regiao, rota_info in rotas.items():
            ocorrencias_regiao = [occ for occ in self.ocorrencias_ativas.values() if occ.regiao == regiao]
            severidade_media = sum(occ.severidade for occ in ocorrencias_regiao) / len(ocorrencias_regiao)
            rotas_priorizadas.append({
                'regiao': regiao,
                'rota': {'caminho': rota_info['rota'][0], 'distancia': rota_info['rota'][1]},
                'ocorrencias': len(ocorrencias_regiao),
                'severidade_media': severidade_media,
                'score': (severidade_media * 10) - rota_info['rota'][1]
            })
        
        rotas_priorizadas.sort(key=lambda x: x['score'], reverse=True)
        print(f"\n🗺️ PLANEJAMENTO DE ATENDIMENTO MÚLTIPLO\n📍 Base de operações: {regiao_base}\n" + "=" * 60)
        print("🎯 ORDEM DE ATENDIMENTO RECOMENDADA:\n" + "-" * 40)
        
        for i, info in enumerate(rotas_priorizadas, 1):
            print(f"{i}. {info['regiao']}\n   📍 Rota: {' → '.join(info['rota']['caminho'])}")
            print(f"   📏 Distância: {info['rota']['distancia']} unidades\n   ⏱️ Tempo: {info['rota']['distancia'] * 0.5:.1f}h")
            print(f"   🔥 Ocorrências: {info['ocorrencias']} (severidade média: {info['severidade_media']:.1f})\n   🎯 Score de prioridade: {info['score']:.1f}\n")
        
        return rotas_priorizadas
    
    def visualizar_mapa_conexoes(self):
        self.grafo_regioes.listar_conexoes()
        total_regioes = len(self.grafo_regioes.vertices)
        print(f"📊 ESTATÍSTICAS DO MAPA:\n   • Total de regiões: {total_regioes}")
        print(f"   • Total de conexões: {sum(len(c) for c in self.grafo_regioes.vertices.values()) // 2}")
        print(f"   • Conectividade média: {sum(len(c) for c in self.grafo_regioes.vertices.values()) / total_regioes:.1f} conexões por região")

def menu_principal():
    sistema = SistemaIVERN()
    while True:
        print("\n" + "="*60 + "\n🌿 SISTEMA IVERN - COORDENAÇÃO DE QUEIMADAS 🌿\n" + "="*60)
        print("1. 🆕 Inserir nova ocorrência\n2. 🚨 Atender próxima ocorrência\n3. 📝 Registrar ações realizadas")
        print("4. 📋 Listar histórico de equipe\n5. 🔄 Atualizar status de ocorrência\n6. 📊 Gerar relatório por região")
        print("7. 🎲 Simular chamadas aleatórias\n8. ✅ Finalizar ocorrência\n9. 🔍 Buscar ocorrências por região")
        print("10. 🗺️ Listar regiões por prioridade\n11. ↩️ Desfazer última ação\n12. 🖥️ Status do sistema")
        print("13. 🛣️ Calcular rota otimizada\n14. 🗺️ Planejar atendimento múltiplo\n15. 🌐 Visualizar mapa de conexões\n0. 🚪 Sair")
        
        try:
            opcao = input("Escolha uma opção: ").strip()
            if opcao == "1":
                sistema.inserir_nova_ocorrencia(
                    input("Região: "),
                    int(input("Severidade (1-10): ")),
                    (float(input("Latitude: ")), float(input("Longitude: "))),
                    input("Descrição (opcional): ")
                )
            elif opcao == "2": sistema.atender_proxima_ocorrencia()
            elif opcao == "3": sistema.registrar_acoes_realizadas(int(input("ID da ocorrência: ")), [a.strip() for a in input("Ações realizadas (separadas por ;): ").split(';') if a.strip()])
            elif opcao == "4": sistema.listar_historico_equipe(int(input("ID da equipe: ")))
            elif opcao == "5": sistema.atualizar_status_ocorrencia(int(input("ID da ocorrência: ")), input("Novo status (PENDENTE/EM_ATENDIMENTO/RESOLVIDO): ").upper())
            elif opcao == "6": sistema.gerar_relatorio_regiao(input("Região (deixe vazio para todas): ").strip() or None)
            elif opcao == "7": sistema.simular_chamadas_aleatorias(int(input("Quantidade de chamadas para simular (padrão 5): ") or "5"))
            elif opcao == "8": sistema.finalizar_ocorrencia(int(input("ID da ocorrência para finalizar: ")))
            elif opcao == "9": sistema.buscar_ocorrencias_por_regiao(input("Nome da região para buscar: "))
            elif opcao == "10": sistema.listar_regioes_por_prioridade()
            elif opcao == "11": sistema.desfazer_ultima_acao()
            elif opcao == "12": sistema.status_sistema()
            elif opcao == "13": sistema.calcular_rota_otima(input("Região de origem: "), input("Região de destino: "))
            elif opcao == "14": sistema.planejar_atendimento_multiplo(input("Região base para planejamento: "))
            elif opcao == "15": sistema.visualizar_mapa_conexoes()
            elif opcao == "0": print("👋 Encerrando Sistema IVERN. Até logo!"); break
            else: print("❌ Opção inválida!")
        except ValueError: print("❌ Entrada inválida! Tente novamente.")
        except KeyboardInterrupt: print("\n👋 Sistema encerrado pelo usuário."); break
        except Exception as e: print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    print("🌿 BEM-VINDO AO SISTEMA IVERN 🌿\nSistema de Coordenação de Resposta a Queimadas")
    menu_principal() if input("Escolha o modo:\n1. Menu interativo\n2. Exemplo automatizado\nOpção: ").strip() == "1" else None