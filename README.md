# Sistema de Gerenciamento de Combate a Queimadas

Disciplina: Algoritmos em Grafos  
Professor: Carlos Vinicius 
Aluno: Amanda Alves da Silva
Semestre: 2024.2  


Este projeto simula o combate a incêndios em áreas florestais usando algoritmos de grafos. 
Cada área é representada como um vértice e as conexões como arestas com custos. 
Brigadistas se deslocam para combater o fogo de forma otimizada, considerando a quantidade de água e o tempo de propagação do fogo.


## Vídeo de Apresentação


[Clique aqui para assistir no YouTube](https://youtu.be/FBwUHPYCcpw)



## 💻 Como Executar

1. Instale o Python 3 (se ainda não tiver instalado).
2. Clone este repositório ou baixe os arquivos `.py` e `.csv`.
3. Execute o arquivo `simulador_queimadas.py`:

```bash
python simulador_queimadas.py
```

# Relatório 

Para desenvolver o projeto, eu optei por usar a linguagem Python e modelar o problema com grafos. Cada local (como pontos de vegetação, postos de brigada e pontos de coleta de água) foi representado como um vértice, e as rotas entre esses locais como arestas com custos (esses custos simulam o esforço ou dificuldade de atravessar o terreno)
A propagação do fogo foi simulada com o algoritmo de Busca em Largura (BFS), porque ele trata bem a ideia de espalhar algo (como o fogo) por camadas a cada unidade de tempo.
Já para mover os brigadistas até os locais do incêndio e também até os pontos de água (quando necessário reabastecer), usei o algoritmo de Dijkstra, que é excelente para encontrar o caminho mais curto em grafos com pesos.
Também implementei um sistema para gerenciar a capacidade dos caminhões de água e a disponibilidade das equipes, garantindo que tudo fosse feito com os recursos disponíveis.
Por fim, automatizei as simulações para que o fogo começasse em diferentes vértices do grafo (exceto nos postos de brigadistas), e os resultados foram registrados em um arquivo CSV, para facilitar a análise posterior.

Análise dos Resultados
A cada simulação, o sistema registra:

O vértice onde o fogo começou;
Quantos locais foram salvos do incêndio;
Quanto tempo a operação levou;
Quanta água foi usada;
E quais caminhos os brigadistas seguiram;

Ao final, o programa também mostra no terminal qual simulação foi mais eficiente, ou seja, aquela que conseguiu salvar mais vértices.
Nos testes que realizei, percebi que o posicionamento dos postos de brigada e dos pontos de água faz bastante diferença no desempenho. 
Quando os brigadistas estão mais próximos do foco ou de um ponto de coleta, eles agem mais rápido e conseguem conter melhor o fogo.

Melhorias e Desafios

Desafios Enfrentados

Durante o desenvolvimento, alguns pontos deram um pouco mais de trabalho:
Sincronizar o tempo de chegada das equipes com o avanço do fogo exigiu atenção, para garantir que a simulação fizesse sentido.
Também precisei pensar bem em como liberar as equipes após apagarem um incêndio, para que pudessem ser reutilizadas em outros focos.
Outro desafio foi controlar o reabastecimento de água, especialmente em situações onde o caminhão precisava abastecer mais de uma vez no mesmo trajeto.

Melhorias

Adicionar uma interface visual, talvez com a biblioteca NetworkX, para mostrar a propagação do fogo e os caminhos dos brigadistas em tempo real.
Permitir que várias equipes atuassem ao mesmo tempo, em diferentes regiões do grafo.
Criar uma variação nas condições, como vento ou obstáculos, que afetassem a propagação do fogo.


