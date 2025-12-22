import random

facil = [
    {
        "pergunta": "Qual é a principal característica de um modelo dinâmico de um sistema?",
        "alternativas": [
            "As variáveis do sistema permanecem sempre constantes.",
            "O modelo é representado por equações algébricas simples.",
            "As variáveis do sistema podem mudar e evoluir com o passar \n do tempo.",
            "O modelo só pode ser resolvido por métodos analíticos."
        ],
        "correta": 2,
        "ajuda": "Modelos dinâmicos descrevem sistemas cujas variáveis mudam com o tempo."
    },
    {
        "pergunta": "O que é simulação no contexto da engenharia de processos?",
        "alternativas": [
            "A construção de uma planta piloto em escala real.",
            "Obtenção da resposta de um modelo matemático \n ao longo do tempo para certas entradas.",
            "A coleta de dados operacionais de um processo existente.",
            "A otimização de custos de produção usando planilhas."
        ],
        "correta": 1,
        "ajuda": "Simulação envolve prever o comportamento do sistema usando modelos matemáticos."
    },
    {
        "pergunta": "Um modelo matemático que despreza as variações espaciais e trata as propriedades como homogêneas é chamado de:",
        "alternativas": [
            "Modelo a parâmetros distribuídos",
            "Modelo a parâmetros concentrados",
            "Modelo estocástico",
            "Modelo empírico"
        ],
        "correta": 1,
        "ajuda": "Modelos a parâmetros concentrados assumem propriedades uniformes no sistema."
    },
    {
        "pergunta": "Um modelo matemático que as variáveis dependentes ou suas derivadas aparecem apenas no 1° grau, ele é classificado como:",
        "alternativas": [
            "Não-linear",
            "Linear",
            "Dinâmico",
            "Estático"
        ],
        "correta": 1,
        "ajuda": "Modelos lineares têm variáveis e derivadas apenas no primeiro grau."
    },
    {
        "pergunta": "Qual método de modelagem é baseado fundamentalmente em princípios da física e da química?",
        "alternativas": [
            "Método empírico ou heurístico",
            "Método por analogia",
            "Método teórico",
            "Método estatístico"
        ],
        "correta": 2,
        "ajuda": "O método teórico utiliza leis físicas e químicas para modelar sistemas."
    },
    {
        "pergunta": "Um modelo que descreve um sistema em regime permanente, onde as variáveis não mudam com o tempo, é chamado de:",
        "alternativas": [
            "Modelo dinâmico",
            "Modelo transiente",
            "Modelo estático ou estacionário",
            "Modelo discreto"
        ],
        "correta": 2,
        "ajuda": "Modelos estáticos descrevem sistemas em equilíbrio, sem variação temporal."
    },
    {
        "pergunta": "Qual tipo de equação diferencial geralmente descreve um modelo a parâmetros distribuídos?",
        "alternativas": [
            "Equações Algébricas",
            "Equações Diferenciais Parciais",
            "Equações Diferenciais Ordinárias",
            "Equações de Estado"
        ],
        "correta": 1,
        "ajuda": "Modelos distribuídos usam equações diferenciais parciais."
    },
    {
        "pergunta": '"É um sistema de equações, cuja solução, dado um conjunto de entradas, fornece a resposta temporal das variáveis de interesse do sistema."(Denn, 1986)',
        "alternativas": [
            "Modelo matemático",
            "Modelo físico",
            "Modelo conceitual",
            "Modelo estático"
        ],
        "correta": 0,
        "ajuda": "Modelos matemáticos fornecem respostas temporais para variáveis do sistema."
    },
    {
        "pergunta": "Modelos que são obtidos correlacionando dados de entrada e saída de um processo, sem se aprofundar nos fenômenos físicos, são chamados de:",
        "alternativas": [
            "Modelos teóricos",
            "Modelos empíricos",
            "Modelos de parâmetros distribuídos",
            "Modelos de primeira ordem"
        ],
        "correta": 1,
        "ajuda": "Modelos empíricos são baseados em dados experimentais."
    },
    {
        "pergunta": "Para que serve a etapa de 'Validação do Modelo' no estudo da dinâmica de sistemas?",
        "alternativas": [
            "Para vender o modelo matemático para outra empresa.",
            "Para publicar o modelo em um artigo científico.",
            "Para comparar a resposta do modelo com dados \n reais e corrigir possíveis erros.",
            "Para garantir que o modelo seja sempre linear \n e de primeira ordem."
        ],
        "correta": 2,
        "ajuda": "A validação compara o modelo com dados reais para garantir precisão."
    },
    {
        "pergunta": "Qual é o principal objetivo da modelagem matemática de um processo?",
        "alternativas": [
            "Substituir completamente o processo físico real.",
            "Compreender e prever o comportamento do sistema.",
            "Eliminar a necessidade de experimentos.",
            "Gerar equações complexas para o sistema."
        ],
        "correta": 1,
        "ajuda": "A modelagem permite entender e prever como o sistema reage a diferentes condições."
    },
    {
        "pergunta": "Os modelos podem ser de natureza:",
        "alternativas": [
            "Física e matemática.",
            "Física, matemática, gráfica e mapas.",
            "Apenas teórica.",
            "Apenas empírica."
        ],
        "correta": 1,
        "ajuda": "Os modelos podem representar sistemas por meio físico, matemático ou visual (mapas, diagramas)."
    },
    {
        "pergunta": "Na modelagem teórica, as equações podem ser baseadas em quais leis fundamentais?",
        "alternativas": [
            "Leis de Newton e Kirchhoff, conservação e relações constitutivas.",
            "Somente nas leis de Ohm e Hooke.",
            "Nas leis estatísticas dos dados observados.",
            "Em princípios exclusivamente químicos."
        ],
        "correta": 0,
        "ajuda": "A abordagem teórica usa leis físicas fundamentais para descrever o sistema matematicamente."
    },
    {
        "pergunta": "O que caracteriza um modelo dinâmico?",
        "alternativas": [
            "O modelo é independente das entradas.",
            "As variáveis mudam com o tempo.",
            "Não existem equações diferenciais.",
            "O sistema está sempre em equilíbrio."
        ],
        "correta": 1,
        "ajuda": "Modelos dinâmicos descrevem a evolução das variáveis ao longo do tempo."
    },
    {
        "pergunta": "A Primeira Lei de Kirchhoff trata da conservação de:",
        "alternativas": [
            "Energia.",
            "Potência.",
            "Carga elétrica.",
            "Tensão elétrica."
        ],
        "correta": 2,
        "ajuda": "A Primeira Lei de Kirchhoff afirma que a soma das correntes em um nó é igual a zero."
    },
    {
        "pergunta": "De acordo com a Segunda Lei de Kirchhoff, a soma das tensões em uma malha fechada é:",
        "alternativas": [
            "Maior que zero.",
            "Igual a zero.",
            "Menor que zero.",
            "Indeterminada."
        ],
        "correta": 1,
        "ajuda": "A Segunda Lei de Kirchhoff expressa a conservação de energia elétrica na malha."
    },
    {
        "pergunta": "Na relação constitutiva de um capacitor ideal, a carga é proporcional a:",
        "alternativas": [
            "A tensão no resistor.",
            "A corrente na bobina.",
            "A tensão no capacitor.",
            "O tempo de operação."
        ],
        "correta": 2,
        "ajuda": "No capacitor ideal, q = C·Vc — a carga é proporcional à tensão aplicada."
    },
    {
        "pergunta": "A Lei de Ohm relaciona tensão, corrente e:",
        "alternativas": [
            "Indutância.",
            "Resistência.",
            "Capacitância.",
            "Condutância térmica."
        ],
        "correta": 1,
        "ajuda": "A relação básica é V = R·i, válida para resistores ôhmicos ideais."
    },
    {
        "pergunta": "Em um circuito RC, a constante de tempo do sistema é dada por:",
        "alternativas": [
            "R/C",
            "RC",
            "1/(RC)",
            "R + C"
        ],
        "correta": 1,
        "ajuda": "A constante de tempo τ = R·C define a velocidade de carga e descarga do capacitor."
    },
    {
        "pergunta": "Qual elemento elétrico é responsável por armazenar energia em forma de campo magnético?",
        "alternativas": [
            "Resistor.",
            "Indutor.",
            "Capacitor.",
            "Diodo."
        ],
        "correta": 1,
        "ajuda": "O indutor armazena energia em um campo magnético proporcional à corrente."
    },
    {
        "pergunta": "A Segunda Lei de Newton afirma que:",
        "alternativas": [
            "A força é inversamente proporcional à aceleração.",
            "A força é igual à massa vezes a aceleração.",
            "A força é independente da massa.",
            "A força depende da velocidade."
        ],
        "correta": 1,
        "ajuda": "F = m·a é a base da modelagem de sistemas mecânicos lineares."
    },
    {
        "pergunta": "O momento linear é definido como:",
        "alternativas": [
            "p = F/t",
            "p = mv",
            "p = m/a",
            "p = E/v"
        ],
        "correta": 1,
        "ajuda": "O momento linear expressa a quantidade de movimento de um corpo em translação."
    },
    {
        "pergunta": "A Lei de Hooke expressa a relação entre:",
        "alternativas": [
            "Força e deslocamento em uma mola.",
            "Força e aceleração.",
            "Velocidade e massa.",
            "Energia e temperatura."
        ],
        "correta": 0,
        "ajuda": "Para molas ideais, F = k·x — força elástica proporcional ao deslocamento."
    },
    {
        "pergunta": "Na modelagem mecânica, a mola ideal representa qual tipo de energia?",
        "alternativas": [
            "Cinética.",
            "Elástica.",
            "Elétrica.",
            "Térmica."
        ],
        "correta": 1,
        "ajuda": "A energia potencial elástica é armazenada no alongamento da mola."
    },
    {
        "pergunta": "A unidade do coeficiente de amortecimento (c) em um sistema mecânico é:",
        "alternativas": [
            "N/m",
            "N⋅s/m",
            "kg⋅m/s²",
            "N⋅m"
        ],
        "correta": 1,
        "ajuda": "O coeficiente c relaciona força e velocidade: F = c·v, medido em N·s/m."
    },
    {
        "pergunta": "O movimento oscilatório de um sistema massa–mola é caracterizado por:",
        "alternativas": [
            "Movimento uniforme retilíneo.",
            "Movimento harmônico simples.",
            "Movimento aleatório.",
            "Movimento exponencial crescente."
        ],
        "correta": 1,
        "ajuda": "O sistema massa–mola apresenta oscilação senoidal em torno da posição de equilíbrio."
    },
    {
        "pergunta": "Em sistemas mecânicos, o termo 'ξ' representa:",
        "alternativas": [
            "A constante de mola.",
            "O fator de amortecimento.",
            "O tempo característico.",
            "A massa equivalente."
        ],
        "correta": 1,
        "ajuda": "ξ indica o grau de amortecimento — define se o sistema é sub, super ou criticamente amortecido."
    }
]

medio = [
    {
        "pergunta": "O 'atraso de transferência' (lag) em um processo industrial é resultado do efeito combinado de quais duas propriedades?",
        "alternativas": [
            "Inércia e Ganho",
            "Resistência e Capacitância",
            "Atraso de transporte e Atraso de transferência",
            "Massa e Aceleração"
        ],
        "correta": 1,
        "ajuda": "O atraso de transferência é modelado como o efeito conjunto de resistência (R) e capacitância (C)."
    },
    {
        "pergunta": "Qual a principal diferença entre um modelo teórico (ou analítico) e um modelo empírico?",
        "alternativas": [
            "O teórico usa equações diferenciais e o empírico usa algébricas",
            "O teórico é desenvolvido com base em princípios da Física/Química e o empírico com base em dados observados",
            "O teórico é sempre linear e o empírico é sempre não-linear",
            "O teórico é para sistemas mecânicos e o empírico para sistemas químicos"
        ],
        "correta": 1,
        "ajuda": "Modelos teóricos usam leis fundamentais; empíricos ajustam dados observados experimentalmente."
    },
    {
        "pergunta": "Em um sistema mecânico translacional ideal, qual elemento é responsável por armazenar energia potencial?",
        "alternativas": [
            "A massa",
            "O amortecedor",
            "A mola",
            "A força externa"
        ],
        "correta": 2,
        "ajuda": "A mola ideal acumula energia potencial proporcional ao deslocamento elástico."
    },
    {
        "pergunta": "Em um sistema com dois tanques em cascata, o que caracteriza uma configuração de 'capacitâncias interativas'?",
        "alternativas": [
            "A vazão de saída do primeiro tanque independe do nível do segundo",
            "A vazão de saída do primeiro tanque depende do nível do segundo",
            "Os dois tanques são idênticos em volume",
            "O fluido é transportado por uma bomba entre os tanques"
        ],
        "correta": 1,
        "ajuda": "Quando o nível de um tanque influencia o outro, há interação entre as capacitâncias hidráulicas."
    },
    {
        "pergunta": "Qual elemento ideal de um sistema mecânico translacional é análogo a um resistor em um sistema elétrico (considerando a segunda analogia Tensão ↔ Força)?",
        "alternativas": [
            "Massa",
            "Mola",
            "Amortecedor",
            "Força externa"
        ],
        "correta": 2,
        "ajuda": "O amortecedor representa dissipação de energia mecânica, assim como o resistor dissipa energia elétrica."
    },
    {
        "pergunta": "O processo de comparar os valores simulados de um modelo com dados reais do sistema para detectar e corrigir erros é denominado:",
        "alternativas": [
            "Calibração do Modelo",
            "Validação do Modelo",
            "Linearização do Modelo",
            "Otimização do Modelo"
        ],
        "correta": 1,
        "ajuda": "A validação garante que o modelo representa corretamente o comportamento real do sistema."
    },
    {
        "pergunta": "Qual a relação matemática fundamental (Lei de Hooke) para uma mola ideal de constante k?",
        "alternativas": [
            "F = k ⋅ v",
            "F = k ⋅ x²",
            "F = k ⋅ x",
            "F = k / x"
        ],
        "correta": 2,
        "ajuda": "A força elástica é diretamente proporcional ao deslocamento: F = k·x."
    },
    {
        "pergunta": "Qual é a função primária de um amortecedor ideal em um sistema mecânico?",
        "alternativas": [
            "Armazenar energia cinética",
            "Armazenar energia potencial",
            "Dissipar energia",
            "Gerar movimento"
        ],
        "correta": 2,
        "ajuda": "Amortecedores transformam energia mecânica em calor, estabilizando o movimento."
    },
    {
        "pergunta": "Considerando a primeira analogia (Força ↔ Corrente), o análogo elétrico de uma massa (m) é um:",
        "alternativas": [
            "Resistor (R)",
            "Indutor (L)",
            "Fonte de Tensão (V)",
            "Capacitor (C)"
        ],
        "correta": 1,
        "ajuda": "A massa armazena energia cinética, assim como o indutor armazena energia magnética."
    },
    {
        "pergunta": "A principal simplificação ao se modelar um sistema com parâmetros concentrados em vez de distribuídos é:",
        "alternativas": [
            "Desprezar a variação das propriedades no tempo",
            "Assumir que todas as relações são lineares",
            "Desprezar as variações espaciais das propriedades",
            "Considerar o sistema em regime permanente"
        ],
        "correta": 2,
        "ajuda": "Modelos concentrados assumem que variáveis são uniformes em todo o domínio físico."
    },
    {
        "pergunta": "Em um circuito RLC, o termo R/L na equação diferencial representa:",
        "alternativas": [
            "O ganho do sistema.",
            "A taxa de amortecimento elétrico.",
            "O tempo de carga do capacitor.",
            "A energia armazenada no indutor."
        ],
        "correta": 1,
        "ajuda": "R/L controla o amortecimento da corrente no circuito — comportamento análogo ao atrito mecânico."
    },
    {
        "pergunta": "No sistema massa–mola–amortecedor, a razão c/m define:",
        "alternativas": [
            "A frequência natural do sistema.",
            "A velocidade inicial do movimento.",
            "O coeficiente de amortecimento normalizado.",
            "A força resultante aplicada."
        ],
        "correta": 2,
        "ajuda": "A razão c/m influencia a rapidez com que o sistema retorna ao equilíbrio após uma perturbação."
    },
    {
        "pergunta": "Na modelagem mecânica, o termo k/m influencia diretamente:",
        "alternativas": [
            "A frequência natural do sistema.",
            "A dissipação de energia.",
            "A amplitude inicial.",
            "A constante de tempo térmica."
        ],
        "correta": 0,
        "ajuda": "A relação k/m determina a frequência natural das oscilações do sistema massa–mola."
    },
    {
        "pergunta": "Quando ξ = 1, o sistema massa–mola–amortecedor é classificado como:",
        "alternativas": [
            "Superamortecido",
            "Criticamente amortecido",
            "Subamortecido",
            "Sem amortecimento"
        ],
        "correta": 1,
        "ajuda": "No amortecimento crítico o sistema retorna ao equilíbrio no menor tempo possível sem oscilar."
    },
    {
        "pergunta": "Na Segunda Lei de Kirchhoff, se a soma das tensões for diferente de zero, isso indica:",
        "alternativas": [
            "Violação da conservação de energia.",
            "Circuito em regime permanente.",
            "Equilíbrio dinâmico do sistema.",
            "Resistores ideais."
        ],
        "correta": 0,
        "ajuda": "Se ΣV ≠ 0, há perda ou ganho não previsto de energia — o circuito não obedece à lei de conservação."
    },
    {
        "pergunta": "Em um sistema rotacional, o análogo da massa (m) é:",
        "alternativas": [
            "O torque aplicado.",
            "O momento de inércia (J).",
            "A velocidade angular (ω).",
            "A energia potencial."
        ],
        "correta": 1,
        "ajuda": "O momento de inércia mede a resistência à variação da velocidade angular, como m faz na translação."
    },
    {
        "pergunta": "Qual grandeza está associada à conservação de momento angular?",
        "alternativas": [
            "Torque.",
            "Energia cinética.",
            "Força centrípeta.",
            "Velocidade linear."
        ],
        "correta": 0,
        "ajuda": "O torque é a causa da variação do momento angular de um corpo em rotação."
    },
    {
        "pergunta": "Em um circuito RC, o tempo necessário para o capacitor atingir 63% da carga final é chamado de:",
        "alternativas": [
            "Tempo de resposta.",
            "Constante de tempo (τ).",
            "Tempo de amortecimento.",
            "Tempo de atraso."
        ],
        "correta": 1,
        "ajuda": "A constante de tempo τ indica o tempo para o capacitor atingir 63,2% da tensão final."
    },
    {
        "pergunta": "A conservação de energia mecânica é válida apenas quando:",
        "alternativas": [
            "Há dissipação por atrito.",
            "Não há forças não-conservativas.",
            "A massa é constante.",
            "O sistema é linear."
        ],
        "correta": 1,
        "ajuda": "A energia mecânica total se conserva apenas na ausência de forças dissipativas, como atrito ou amortecimento."
    },
    {
        "pergunta": "A equação m·ẍ + c·ẋ + kx = 0 representa:",
        "alternativas": [
            "Um sistema elétrico RLC paralelo.",
            "Um sistema massa–mola–amortecedor livre.",
            "Um sistema oscilatório forçado.",
            "Um modelo térmico com perdas."
        ],
        "correta": 1,
        "ajuda": "Essa equação diferencial descreve o comportamento livre (sem força externa) de um sistema massa–mola–amortecedor."
    }
]

dificil = [
    {
        "pergunta": "Considere o modelo dinâmico de um tanque de mistura dado por: dC(t)/dt + 3C(t) = 2C_in(t), onde C é a concentração no tanque e C_in a concentração de entrada. Qual é a função de transferência G(s) = C(s)/C_in(s) associada a esse sistema?",
        "alternativas": [
            "G(s) = (s + 3) / 2",
            "G(s) = 2 / s",
            "G(s) = 2 / (s + 3)",
            "G(s) = s / (s + 3)"
        ],
        "correta": 2,
        "ajuda": "A função de transferência é obtida aplicando a Transformada de Laplace com condições iniciais nulas."
    },
    {
        "pergunta": "Considere o modelo fenomenológico de dois tanques interligados: ḣ₁ = −2h₁ + h₂ e ḣ₂ = 3h₁ − 4h₂. Qual é a matriz A do sistema no formato ẋ = Ax?",
        "alternativas": [
            "[[2, −1], [−3, 4]]",
            "[[−2, 1], [3, −4]]",
            "[[1, −2], [3, −4]]",
            "[[−2, 3], [1, −4]]"
        ],
        "correta": 1,
        "ajuda": "A matriz A é formada diretamente pelos coeficientes das variáveis de estado em cada equação."
    },
    {
        "pergunta": "Considere o modelo linearizado de um tanque esférico operando em torno de um ponto de operação, dado por: ẋ₁ = −2x₁ + x₂ e ẋ₂ = 3x₁ − 4x₂, onde x₁ e x₂ representam desvios do nível em dois pontos do sistema hidráulico. Para determinar se o ponto de operação é estável, o aluno utiliza o MATLAB para calcular os autovalores da matriz do sistema. Qual conclusão correta pode ser obtida a partir dessa análise?",
        "alternativas": [
            "O sistema é instável, pois possui pelo menos um autovalor positivo",
            "O sistema é marginalmente estável, pois possui autovalores nulos",
            "O sistema é assintoticamente estável, pois todos os autovalores possuem parte real negativa",
            "Não é possível determinar a estabilidade a partir dos autovalores"
        ],
        "correta": 2,
        "ajuda": "No MATLAB, use eig(A) para calcular os autovalores e analisar o sinal de suas partes reais."
    },
    {
        "pergunta": "Considere o modelo dinâmico de um sistema térmico concentrado dado por: dT(t)/dt + 5T(t) = 10T_in(t). Qual é a função de transferência G(s) = T(s)/T_in(s)?",
        "alternativas": [
            "G(s) = 5 / (s + 10)",
            "G(s) = 10 / s",
            "G(s) = 10 / (s + 5)",
            "G(s) = s / (s + 5)"
        ],
        "correta": 2,
        "ajuda": "Aplique a Transformada de Laplace assumindo condições iniciais nulas."
    },
    {
        "pergunta": "Considere o modelo de dois compartimentos térmicos: Ṫ₁ = −2T₁ + T₂ e Ṫ₂ = 3T₁ − 4T₂. Qual é a matriz A do sistema no formato ẋ = Ax?",
        "alternativas": [
            "[[2, −1], [−3, 4]]",
            "[[−2, 1], [3, −4]]",
            "[[1, −2], [3, −4]]",
            "[[−2, 3], [1, −4]]"
        ],
        "correta": 1,
        "ajuda": "Organize os coeficientes das variáveis de estado."
    },
    {
        "pergunta": "Em um tanque cilíndrico, a dinâmica do nível é descrita por: dh(t)/dt + 4h(t) = 8q(t). Qual é a função de transferência G(s) = H(s)/Q(s)?",
        "alternativas": [
            "G(s) = (s + 4) / 8",
            "G(s) = 8 / s",
            "G(s) = 8 / (s + 4)",
            "G(s) = s / (s + 4)"
        ],
        "correta": 2,
        "ajuda": "Identifique o termo de entrada e aplique Laplace."
    },
    {
        "pergunta": "Considere o modelo fenomenológico de um sistema hidráulico com duas variáveis de estado: ẋ₁ = −2x₁ + x₂ e ẋ₂ = 3x₁ − 4x₂. Qual é a matriz A associada?",
        "alternativas": [
            "[[2, −1], [−3, 4]]",
            "[[−2, 1], [3, −4]]",
            "[[1, −2], [3, −4]]",
            "[[−2, 3], [1, −4]]"
        ],
        "correta": 1,
        "ajuda": "Leia diretamente os coeficientes das equações."
    },
    {
        "pergunta": "Na modelagem de um escoamento em um tubo, são dadas as equações: (1) ∂ρ/∂t + ∂(ρv)/∂x = 0 e (2) ρ∂v/∂t + ρv∂v/∂x = −∂p/∂x. Qual equação representa o balanço de massa?",
        "alternativas": [
            "Equação (2)",
            "Equação (1)",
            "Ambas",
            "Nenhuma"
        ],
        "correta": 1,
        "ajuda": "O balanço de massa é dado pela equação da continuidade."
    },
    {
        "pergunta": "Considere o modelo dinâmico de um reator perfeitamente misturado dado por: dX(t)/dt + 6X(t) = 12X_in(t). Qual é a função de transferência G(s) = X(s)/X_in(s)?",
        "alternativas": [
            "G(s) = (s + 6) / 12",
            "G(s) = 12 / s",
            "G(s) = 12 / (s + 6)",
            "G(s) = s / (s + 6)"
        ],
        "correta": 2,
        "ajuda": "Use a Transformada de Laplace com condições iniciais nulas."
    },
    {
        "pergunta": "Considere o modelo fenomenológico de um sistema de armazenamento com duas variáveis: ẋ₁ = −2x₁ + x₂ e ẋ₂ = 3x₁ − 4x₂. Qual é a matriz A no formato ẋ = Ax?",
        "alternativas": [
            "[[2, −1], [−3, 4]]",
            "[[−2, 1], [3, −4]]",
            "[[1, −2], [3, −4]]",
            "[[−2, 3], [1, −4]]"
        ],
        "correta": 1,
        "ajuda": "A matriz A é formada pelos coeficientes das variáveis de estado."
    }
]



import copy

def obter_perguntas_por_nivel(nivel, historico, limite=10):
    """
    Regras garantidas:
    1) Perguntas do nível atual vêm primeiro
    2) Não repete perguntas já respondidas (histórico)
    3) Se não completar `limite`, usa perguntas do próximo nível
    4) NÃO altera as listas base (facil, medio, dificil)
    """

    perguntas_por_nivel = {
        1: facil,
        2: medio,
        3: dificil
    }

    perguntas_jogo = []

    # ========= NÍVEL ATUAL =========
    perguntas_atual = perguntas_por_nivel.get(nivel, [])

    # valida histórico apenas contra o nível atual
    historico_atual = {
        i for i in historico
        if isinstance(i, int) and 0 <= i < len(perguntas_atual)
    }

    # perguntas não respondidas do nível atual (ORDEM PRESERVADA)
    for i, p in enumerate(perguntas_atual):
        if len(perguntas_jogo) >= limite:
            break
        if i in historico_atual:
            continue

        perguntas_jogo.append({
            **copy.deepcopy(p),
            "indice_global": i,
            "nivel": nivel
        })

    # ========= PRÓXIMO NÍVEL (SE PRECISAR) =========
    if len(perguntas_jogo) < limite and nivel < 3:
        prox_nivel = nivel + 1
        perguntas_prox = perguntas_por_nivel.get(prox_nivel, [])

        for i, p in enumerate(perguntas_prox):
            if len(perguntas_jogo) >= limite:
                break

            perguntas_jogo.append({
                **copy.deepcopy(p),
                "indice_global": i,
                "nivel": prox_nivel
            })

    return perguntas_jogo