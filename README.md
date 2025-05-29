# 🌿 Sistema IVERN - Coordenação de Resposta a Queimadas

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 📋 Descrição

O **Sistema IVERN** é uma solução completa para coordenação e gerenciamento de resposta a queimadas florestais. Utilizando estruturas de dados avançadas e algoritmos otimizados, o sistema oferece funcionalidades para priorização de ocorrências, coordenação de equipes, planejamento de rotas e geração de relatórios em tempo real.

Desenvolvemos esta solução para a Global Solutions do segundo ano letivo da **FIAP** no curso de Engenharia de Software

### 🎯 Principais Características

- **Priorização Inteligente**: Sistema de fila de prioridade baseado em heap para atendimento por severidade
- **Otimização de Rotas**: Algoritmo de Dijkstra para cálculo de rotas mais eficientes
- **Histórico Completo**: Lista ligada para rastreamento detalhado de ações
- **Busca Eficiente**: Árvore binária para organização de regiões por prioridade
- **Planejamento Avançado**: Grafo de regiões para coordenação de atendimento múltiplo
- **Interface Intuitiva**: Menu interativo com simulações automatizadas

## 🏗️ Arquitetura do Sistema

### Estruturas de Dados Implementadas

| Estrutura | Uso | Complexidade |
|-----------|-----|--------------|
| **Heap (Priority Queue)** | Priorização de ocorrências | O(log n) inserção/remoção |
| **Lista Ligada** | Histórico de ações das equipes | O(1) inserção |
| **Árvore Binária** | Organização de regiões por prioridade | O(log n) busca |
| **Grafo** | Mapeamento de conexões entre regiões | O(V + E) para Dijkstra |
| **Hash Table (Dict)** | Busca rápida de ocorrências e equipes | O(1) acesso |
| **Pilha (Deque)** | Sistema de desfazer ações | O(1) push/pop |
| **Fila (Deque)** | Processamento sequencial | O(1) enqueue/dequeue |

### Algoritmos Utilizados

- **Dijkstra**: Cálculo de rotas otimizadas entre regiões
- **Busca Binária**: Localização eficiente de regiões na árvore
- **Percurso em Ordem**: Listagem ordenada de regiões por prioridade
- **Algoritmos de Heap**: Manutenção da fila de prioridade

## 🚀 Instalação e Execução

### Pré-requisitos

```bash
Python 3.7 ou superior
```

### Executando o Sistema

1. **Clone o repositório**:
```bash
git clone https://github.com/imneli/gs-dynamic.git
cd gs-dynamic
```

2. **Execute o sistema**:
```bash
python main.py
```

3. **Escolha o modo de execução**:
   - **1**: Menu interativo completo
   - **2**: Exemplo automatizado (demonstração)

## 📱 Funcionalidades

### 🆕 Gestão de Ocorrências
- Inserção de novas ocorrências com geolocalização
- Priorização automática por severidade (1-10)
- Atualização de status em tempo real
- Finalização e arquivamento de casos resolvidos

### 👥 Coordenação de Equipes
- Gestão de equipes especializadas (Terrestre, Aérea, Resgate)
- Alocação inteligente baseada em disponibilidade e especialização
- Histórico completo de ações por equipe
- Sistema de disponibilidade em tempo real

### 🗺️ Planejamento de Rotas
- Cálculo de rotas otimizadas entre regiões
- Planejamento de atendimento múltiplo a partir de base
- Estimativa de tempo e distância
- Visualização de conexões no mapa

### 📊 Relatórios e Analytics
- Relatórios por região com estatísticas detalhadas
- Status geral do sistema
- Busca por critérios específicos
- Histórico completo de ações

## 💻 Uso do Sistema

### Menu Principal

```
🌿 SISTEMA IVERN - COORDENAÇÃO DE QUEIMADAS 🌿
1. 🆕 Inserir nova ocorrência
2. 🚨 Atender próxima ocorrência (maior prioridade)
3. 📝 Registrar ações realizadas
4. 📋 Listar histórico de equipe
5. 🔄 Atualizar status de ocorrência
6. 📊 Gerar relatório por região
7. 🎲 Simular chamadas aleatórias
8. ✅ Finalizar ocorrência
9. 🔍 Buscar ocorrências por região
10. 🗺️ Listar regiões por prioridade
11. ↩️ Desfazer última ação
12. 🖥️ Status do sistema
13. 🛣️ Calcular rota otimizada entre regiões
14. 🗺️ Planejar atendimento múltiplo
15. 🌐 Visualizar mapa de conexões
0. 🚪 Sair
```

### Exemplo de Uso

```python
# Executar exemplo automatizado
python main.py
# Escolher opção 2 para demonstração automática

# Ou usar interativamente
sistema = SistemaIVERN()
id_ocorrencia = sistema.inserir_nova_ocorrencia(
    "Mata Atlântica Sul", 
    8, 
    (-23.5505, -46.6333), 
    "Incêndio de grande porte"
)
sistema.atender_proxima_ocorrencia()
```

## 🌍 Regiões Suportadas

O sistema inclui as seguintes regiões pré-configuradas:

- **Mata Atlântica Sul** (Prioridade: 8)
- **Cerrado Central** (Prioridade: 6)
- **Amazônia Norte** (Prioridade: 9)
- **Pantanal** (Prioridade: 7)
- **Caatinga** (Prioridade: 5)

### Mapa de Conexões

```
Mata Atlântica Sul ←→ Cerrado Central (12 unidades)
Cerrado Central ←→ Pantanal (8 unidades)
Cerrado Central ←→ Amazônia Norte (15 unidades)
Amazônia Norte ←→ Caatinga (20 unidades)
Pantanal ←→ Caatinga (18 unidades)
Mata Atlântica Sul ←→ Pantanal (10 unidades)
Cerrado Central ←→ Caatinga (14 unidades)
```

## 🔧 Estrutura do Código

```
main.py
├── Estruturas de Dados
│   ├── No (Nó para lista ligada e árvore)
│   ├── ListaLigada (Histórico de ações)
│   ├── ArvoreRegiao (Organização por prioridade)
│   └── GrafoRegioes (Conexões e rotas)
├── Classes Principais
│   ├── Ocorrencia (Representa uma queimada)
│   ├── Equipe (Equipe de combate)
│   └── SistemaIVERN (Sistema principal)
├── Funcionalidades
│   ├── Gestão de ocorrências
│   ├── Coordenação de equipes
│   ├── Planejamento de rotas
│   └── Geração de relatórios
└── Interface
    ├── Menu interativo
    └── Exemplo automatizado
```

## 📈 Complexidade Computacional

| Operação | Complexidade | Estrutura Utilizada |
|----------|-------------|-------------------|
| Inserir ocorrência | O(log n) | Heap |
| Atender próxima ocorrência | O(log n) | Heap |
| Buscar ocorrência por ID | O(1) | Hash Table |
| Buscar região por prioridade | O(log n) | Árvore Binária |
| Calcular rota otimizada | O(V² + E) | Grafo + Dijkstra |
| Registrar ação no histórico | O(1) | Lista Ligada |
| Desfazer ação | O(1) | Pilha |

## 🧪 Exemplo de Saída

```
🚨 Atendimento iniciado: Ocorrência 3 - Amazônia Norte (Severidade: 10) por Squadrão Aéreo Beta

🛣️ ROTA OTIMIZADA: Cerrado Central → Amazônia Norte
============================================================
📍 Caminho: Cerrado Central → Amazônia Norte
📏 Distância total: 15 unidades
⏱️ Tempo estimado: 7.5 horas
🚁 Paradas intermediárias: 0

📊 RELATÓRIO DE ATENDIMENTO
============================================================
🌍 Amazônia Norte:
   • Ocorrências ativas: 1
   • Severidade média: 10.0
   • Nível de risco: 9/10
```

## 👨‍💻 Autores

**Matheus Rivera Montovaneli**

**João Marcelo Furtado Romero**


---

<div align="center">
  <strong>🌿 Sistema IVERN - Global Solutions FIAP 2025 🌿</strong>
</div>