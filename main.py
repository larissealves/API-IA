from random import random

melhores_solucoes = []

class Produto():
    def __init__(self, nome, bonus, grau_dificuldade):
        self.nome = nome
        self.bonus = bonus
        self.grau_dificuldade = grau_dificuldade
        

class Individuo():
    def __init__(self, nome, bonus, grau_dificuldade, geracao = 0,):
        self.nome = nome
        self.bonus = bonus
        self.grau_dificuldade = grau_dificuldade
        #self.limite = limite
        self.geracao = geracao
        self.nota_avaliacao = 0
        
        self.cromossomo = []
       
        #Inicializa o cromosso de acordo com o valor de range gerado o individou pode recber o valor '1' ou '0' 

        for i in range(len(nome)):
            if random() < 0.5:
               self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")

    # Cada gene do cromossomo com valor '1' tem seu Grau de Dificuldade somado e esta se torna a nota de avaliacao do Cromossomo

    def avaliar_cromossomo(self):
        grau_dificuldade_cromossomo_1 = 0
        bonus_cromossomo_1 = 0
        produtos_1_cromossomo = []

        for i in range(len(self.cromossomo)):
            
            if(self.cromossomo[i] == '1'):
                
                grau_dificuldade_cromossomo_1 += int(self.grau_dificuldade[i])
                bonus_cromossomo_1 += int(self.bonus[i])

        # Depois de atribuido uma nota ao Cromossomo, este pode recebe pode receber um valor extra ou perder ponto de acordo com seu Grau de Dificuldade:
        if grau_dificuldade_cromossomo_1 == 25:
            self.nota_avaliacao = bonus_cromossomo_1 - 0.02
        if grau_dificuldade_cromossomo_1 > 25:
            self.nota_avaliacao = 0.75
        if grau_dificuldade_cromossomo_1 < 25:
            self.nota_avaliacao = bonus_cromossomo_1 + 0.25
        

    # O ponto de corte do Crossover é realizado a partir de um valor aleatório gerado pelo Random e basea no tamanho do cromossomo
    # Os filhos são formados pela parte inicial de seu primeiro Pai[0] até o valor definido pelo ponto de corte e em sequência, 
    # é atribuido o os genes do segundo Pai a partir do ponto de corte até a posição final;

    def crossover(self, outro_individuo):
        
        corte = round(random()  * len(self.cromossomo))
           
        filho1 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
            
        filhos = [Individuo(self.nome, self.bonus, self.grau_dificuldade, self.geracao + 1),
                  Individuo(self.nome, self.bonus, self.grau_dificuldade, self.geracao + 1)]

        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
       
        return filhos

    
    # A mutação de um gene é realizada de forma aleatoria e com menos frequência de acordo com uma taxa 
    # já pré definida. 
    
    def mutacao(self, taxa_mutacao):
        for i in range(len(self.cromossomo)):
            if random() < taxa_mutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        
    # De acordo com o valor informado vários individuos saõ adicionados a população;
    
    def inicializar_populacaoo(self, nome, bonus, grau_dificuldade):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(nome, bonus, grau_dificuldade))
        self.melhor_solucao = self.populacao[0]

    # Ordena os individuos da populacao de acordo com suas Notas de Avalicao 

    def ordena_populacao(self):
        
        self.populacao = sorted(self.populacao, 
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True )
        
    # Identifica o melhor individou da populacao e reserva na self.melhor_solucao

    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo

    #Soma todas as notas dos individou da população, gerando assim um valor base para aplicação do metodo Roleta para escolha dos Pais da nova geração

    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
           soma += individuo.nota_avaliacao
        return soma

    # Com base na nota geral da população, um valor randomico é multiplicado pela nota de avaliacao geral da população, 
    # em seguida, se busca por um individou que tenha uma nota avaliacao proxima ao valor gerado anteriormente. Este é selecionado para ser um dos pais da próixima geração;

    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random() * soma_avaliacao
        soma = 0
        i = 0
        while i < len (self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai


    def visualiza_geracao(self):
        melhor = self.populacao[0]
 
        print("\nG:%s -> Nota: %s Cromossomo: %s" % (self.populacao[0].geracao,
                                                    melhor.nota_avaliacao,
                                                    melhor.cromossomo))

    def resolver_problema (self, taxa_mitacao, numero_geracoes, nome, bonus, grau_dificuldade):
        self.inicializar_populacaoo(nome, bonus, grau_dificuldade)

        for individuo in self.populacao:
            individuo.avaliar_cromossomo()
        
        self.ordena_populacao()
        self.visualiza_geracao()

        for geracao in range(numero_geracoes): # Gera novas populações de acordo com o valor informado
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            # seleciona os dois inividuos para o processo de seleção dos pais da nova. Em seguida, estes pais
            # passarão pelo processo de cruzamento e mutação

            for individuos_gerados in range (0, self.tamanho_populacao, 2): 
            
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2]) 
                
                nova_populacao.append(filhos[0].mutacao(taxa_mitacao))  
                nova_populacao.append(filhos[1].mutacao(taxa_mitacao))
            
            self.populacao = list (nova_populacao)
            
            # A nova população é gerada e o processo repetido

            for individuo in self.populacao:
                individuo.avaliar_cromossomo()
                            
                        
            self.ordena_populacao()
            self.visualiza_geracao()
                                
            melhor = self.populacao[0]
            self.melhor_individuo(melhor)

        print("\nMELHOR SOLUCAO: \n G: %s Nota: %s Cromossomo: %s" % 
        (self.melhor_solucao.geracao,
            self.melhor_solucao.nota_avaliacao,
            self.melhor_solucao.cromossomo))
        

        return self.melhor_solucao.cromossomo
        
                
if __name__ == '__main__':
   
    lista_produtos = []
    lista_produtos.append(Produto("Cachorro Quente", '3', '4'))
    lista_produtos.append(Produto("Chambari", '8', '5'))
    lista_produtos.append(Produto("Cuscuz", '7', '4'))
    lista_produtos.append(Produto("Guaraná Jesus", '3', '7'))
    lista_produtos.append(Produto("Hamburguer", '6', '6'))
    lista_produtos.append(Produto("Pizza", '6', '5'))
    lista_produtos.append(Produto("Sarapel", '5', '3'))
    lista_produtos.append(Produto("Tapioca", '5', '4'))

    nome = []
    bonus = []
    grau_dificuldade = []
    limite = 25
    nota_avaliacao = 0
    tamanho_populacao = 6
    taxa_mitacao = 0.05
    numero_geracoes = 10
    
    solucao = []

    for produto in lista_produtos:
        nome.append(produto.nome)
        bonus.append(produto.bonus)
        grau_dificuldade.append(produto.grau_dificuldade)

    ag = AlgoritmoGenetico(tamanho_populacao)
    resultado = ag.resolver_problema(taxa_mitacao, numero_geracoes, nome, bonus, grau_dificuldade)
    print('\n', '*' *  70)
    for i in range(len(lista_produtos)):
        if resultado[i] == '1':
            #solucao.append(lista_produtos[i].nome)
            #print("\n\n",lista_produtos[i].nome, "| Bônus", lista_produtos[i].bonus, "| Grau Dificuldade", lista_produtos[i].grau_dificuldade)
            
            print("\n\n",lista_produtos[i].nome, "| Bônus", lista_produtos[i].bonus, "| Grau Dificuldade", lista_produtos[i].grau_dificuldade)
     
    '''individuo1 = Individuo(nome, bonus, grau_dificuldade, tamanho_populacao)
    individuo1.avaliar_cromossomo()

    individuo2 = Individuo(nome, bonus, grau_dificuldade, tamanho_populacao)
    individuo2.avaliar_cromossomo()

    individuo1.crossover(individuo2)

    individuo1.mutacao(0.05)
    individuo2.mutacao(0.05)'''
























