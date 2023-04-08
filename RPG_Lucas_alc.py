# Bem vindo ao meu RPG!
# É um projeto simples apenas para praticar minha habilidade no Python e por puro lazer
# Ainda estou no começo da minha trajetória de Python, então muitas coisas ainda podem mudar com o tempo..
# Espero que se divirta usando!

from time import sleep
import random
delay = 0.8
efeitos = {}
contador_rodada = 0
class bcolors:
    reset = '\033[0m'
    vermelho = '\033[0;31m' 
    verde = '\033[0;32m'
    amarelo = '\033[0;33m'
    roxo = '\033[0;34m'
    ciano = '\033[0;36m'
    lilas = '\033[0;35m'
    cinza = '\033[0;37m'

def efeitos_rodada():
    global contador_rodada
    contador_rodada += 1
    global efeitos
    efeitos_copia = efeitos.copy()
    print(f'{bcolors.amarelo}x','--'*15,'x\n',' '*11,f'Rodada {contador_rodada}{bcolors.reset}\n')
    print(f'{bcolors.roxo}Efeitos ativos:{bcolors.reset}', end=' ')
    if len(efeitos) == 0:
        print('Nenhum efeito ativo no momento\n')
    if len(efeitos) > 0:
        efeitos_copia = efeitos.copy()

# o For a seguir recebe o tempo restante dos efeitos e diminui por 1
# caso já seja 1, ele deleta o efeito da lista de efeitos ativos, pois a partir de 0, o efeito é anulado
# para diminuir, é usado uma cópia dos efeitos atuais, já que não é permitido alterar os valores de um dicionário enquanto está num iterador
# Depois disso, a lista de efeitos original recebe os valores modificados da cópia.
        for k,v in efeitos.items():
            if  v > 1:
                efeitos_copia[k] -= 1
                print(f'\n{k}: {v-1} rodada(s)')
            if v == 1:
                efeitos_copia[k] -= 0
                del efeitos_copia[k]
                print(f'\n{k}: efeito zerado')        
        efeitos = efeitos_copia
        print('')

def calculo_buff():
# Usado para calcular o valor adicional de dano por efeitos ativos em uma rodada
    global buff
    buff = 0
    try:
        if efeitos['poção de dano'] > 0:
            buff += 10
    except KeyError:
        None

def escolher():
# Usado para receber a escolha de ação do jogador
    while True:
            escolha = str(input(f'''{bcolors.verde}É o seu turno, o que deseja fazer?{bcolors.reset}
{bcolors.lilas}[atacar] [magia] [item]{bcolors.reset}
-> '''))
            if escolha not in ['atacar','magia','item']:
                print('Escolha não existente, tente novamente. \n')
            else:
                return escolha

def batalha(classe,PV,PVM,nome_inimigo,vida_inimigo,dano_inimigo,mochila={},armadura=0,arma=0):
# A função recebe 9 parâmetros
# classe -> classe escolhida pelo jogador | PV -> Vida atual do jogador | PVM -> Vida máxima do jogador
# Nome_inimigo -> Nome customizável do inimigo | vida_inimigo -> Vida total do inimigo | dano_inimigo -> lista de possíveis danos do inimigo
# Mochila -> Quais itens o jogador possui atualmente | Armadura -> Quantidade fixa de dano negado | arma -> quantidade fixa de dano aplicado
    print(f'Um {nome_inimigo} apareceu!\n')  

# É apresentado os possíveis danos do personagem dependendo de sua classe
    possibilidades_guerreiro = [7, 8, 9, 11, 12, 13]
    flechas = [1, 2, 3, 5, 6, 7, 8]
    possibilidades_mago = list(range(2,36,2))
    while vida_inimigo > 0:
        if PV <= 0:
            break

# Então é usado funções para calcular os efeitos atuais e a escolha do jogador        
        efeitos_rodada()
        escolha = escolher()

        while True:             
            if escolha == 'atacar':
# Caso o jogador decida atacar, é perguntado se deseja rodar os dados ou não
# Se o jogador aceitar, um dano aleatório é escolhido
# Se o jogador negar, um dano mediano fixo é escolhido
# as possibilidades de dano variam a partir da classe escolhida        
                escolha_ataque = str(input(f'\n{bcolors.verde}Deseja rodar os dados?{bcolors.reset} {bcolors.lilas}[s/n]{bcolors.reset}: '))
                
                if escolha_ataque == 's':  
                    for i in range(0,3):
                        print('Rodando os dados'+'.'*i)
                        sleep(delay)
                
                if escolha_ataque == 's' and classe == 'guerreiro':
                    sleep(delay)
                    resultado = random.choice(possibilidades_guerreiro)

                if escolha_ataque == 's' and classe == 'arqueiro':
                    sleep(delay)
                    resultado = (random.choice(flechas) * 4)

                if escolha_ataque == 's' and classe == 'mago':
                    sleep(delay)
                    resultado = random.choice(possibilidades_mago)

                if escolha_ataque == 'n' and classe == 'guerreiro':
                    sleep(delay)
                    resultado = 10

                if escolha_ataque == 'n' and classe == 'arqueiro':
                    sleep(delay)
                    resultado = 4 * 4
                    
                if escolha_ataque == 'n' and classe == 'mago':
                    sleep(delay)
                    resultado = 16
                
                
# Cálculo do dano, que depende do resultado, da arma escolhida e dos efeitos ativos
                print('')
                calculo_buff()
                print(f'O resultado é: {bcolors.ciano}{resultado} + {arma + buff} de dano.{bcolors.reset}')
                sleep(delay)
                vida_inimigo -= (resultado + arma + buff) 
                if vida_inimigo <= 0:
                    break
                print(f'''O inimigo possui {bcolors.vermelho}{vida_inimigo}{bcolors.reset} de vida\n''')
                sleep(1.5)
                break
            
            if escolha == 'item' and len(mochila) == 0:
# Caso o jogador não possua nada na mochila, ele irá retornar ao menu de escolha 
                            print('Sua mochila está vazia..\n')
                            escolha = escolher()  
            
            if escolha == 'item' and len(mochila) > 0:
# Caso o jogador escolha usar um item, é apresentado os itens e as suas quantidades
                print(f'{bcolors.verde}\nDeseja usar que item?{bcolors.reset}')
                while True: 
                    for k,v in mochila.items():
                        print(f'Item: {k:15} | quantidade = {v}')
                    print(f'{bcolors.lilas}[voltar]{bcolors.reset}')
                    escolha_item = input('\n-> ')
                    if escolha_item not in mochila.keys() and escolha_item != 'voltar':
                        print(f'você não possui esse item.. tente novamente\n')
                    else:
                        break

                if escolha_item == 'voltar':
                    print('')
                    escolha = escolher()

                if escolha_item != 'voltar' and mochila[escolha_item] == 0:
                    print(f'Você não possui {escolha_item}.')

                if escolha_item == 'poção de vida':
# Caso o jogador use uma poção de vida, irá recuperar 30 de vida.
                    certeza_item = input(f'Recupera 30 de vida, {bcolors.verde}deseja utilizar? {bcolors.lilas}[s/n]{bcolors.reset} ')
                    if certeza_item == 's':
                        if PV == PVM:
                            print('\nNão é possível aumentar sua vida.')
                        if mochila[escolha_item] >= 1 and PV != PVM:
                            mochila['poção de vida'] -= 1
                            PV += 30
                            if PV > PVM:
                                Vida_sobra = PV - PVM
                                PV -= Vida_sobra
                            print(f'você usou {escolha_item}, {mochila[escolha_item]} restante(s)\n')
                            print(f'Você agora possui {PV} de vida')
                            break

                if escolha_item == 'poção de dano':
# Caso escolha uma poção de dano, ele causará 10 de dano fixo por 3 rodadas
                    certeza_item = input(f'Aumenta 10 de dano por 3 rodadas, {bcolors.verde}deseja utilizar? {bcolors.lilas}[s/n]{bcolors.reset} ')
                    if certeza_item == 's': 
                        if 'poção de dano' in efeitos.keys():
                            print(f'Você já está sobre o efeito da {escolha_item}')
                        else:
                            efeitos['poção de dano'] = 4
                            mochila[escolha_item] -= 1
                            print(f'você usou {escolha_item}, {mochila[escolha_item]} restante(s)\n')
                            break        
        
            if escolha == 'magia':
# O sistema de magia ainda não foi implantado
                print('\nSistema ainda não funcional..\n')
                escolha = escolher()

        if vida_inimigo > 0:
# Caso o inimigo ainda esteja vivo, ele irá atacar o jogador
# O dano causado é aleatório, escolhido a partir de uma lista customizável de danos
# Caso o jogador possua alguma armadura, uma quantidade fixa de dano será negada
            print(f'''Agora é o turno do {bcolors.vermelho}inimigo!{bcolors.reset}''')
            sleep(delay)
            danosofrido = random.choice(dano_inimigo)
            print(f'O inimigo causou {bcolors.vermelho}{danosofrido}{bcolors.reset} a você!')
            print(f'Sua armadura bloqueou {armadura} de dano!')
            PV -= danosofrido - armadura
            sleep(delay)
            print(f'Você possui {bcolors.ciano}{PV}{bcolors.reset} de vida!\n')
            sleep(delay)
    if PV <= 0:
        print(f'{bcolors.amarelo}Infelizmente você morreu, tente outra vez!{bcolors.amarelo}')
    if vida_inimigo <= 0:
        print(f'{bcolors.amarelo}Você matou o inimigo, parabéns!{bcolors.reset}')
    contador_rodada = 0

nomejulgado=['Belo nome!','é um nome mediano, eu acho..','esse é o nome mais medíocre que eu já vi']
jogador=str(input(f'{bcolors.verde}Digite o seu nome, jogador: {bcolors.reset}'))

print(f'{bcolors.ciano}{jogador}{bcolors.reset}.. hmmm...{random.choice(nomejulgado)}')
sleep(1)

while True:
# Escolha de classe do jogador e suas características
    classe = input(f'''\nNeste mundo há diferentes caminhos que você pode escolher..
alguns são grandes guerreiros, poderosos magos ou até mesmo arqueiros furtivos!
E você? o que você será?

[{bcolors.ciano} Guerreiro {bcolors.reset}] ->   Dano baixo | vida alta  | mana baixa
[{bcolors.ciano}    Mago   {bcolors.reset}] ->   Dano alto  | vida baixa | mana alta
[{bcolors.ciano}  Arqueiro {bcolors.reset}] ->   Dano médio | vida média | mana média
{bcolors.cinza}-> {bcolors.reset}''')
# *Apesar de apresentar mana, o sistema de magia ainda não implantado
    classe = classe.lower()

    while classe not in ['guerreiro','mago','arqueiro']:
# Usado caso o jogador erre o nome da classe
        classe=input('Essa.. essa não é uma classe.. tente novamente: ')
    certeza=input(f'\nDeseja ser um {bcolors.ciano}{classe}{bcolors.reset}? {bcolors.lilas}[s/n]{bcolors.reset} ')
# Usado para confirmar a classe escolhida
    if certeza in 'Ss':
       break

# Apresentação das classes e a definição de seus status
if classe == 'guerreiro':
    print('Ah então você escolheu uma classe forte.. destemida!')
    PVM = PV = 120
    mana = manaMax = 30

if classe== 'mago':
    print('Uma classe conhecida por sua grande sabedoria.. e grande poder!')
    PVM = PV = 75
    mana = manaMax = 80

if classe== 'arqueiro':
    print('Treinados com o arco e flecha desde jovens, os arqueiros são ágeis e precisos!')
    PVM = PV = 90
    mana = manaMax = 50

print(f'\n{bcolors.verde}Muito bem', end='')
sleep(0.3)
for i in range(0,3):
    print('.'*i,end='')
    sleep(0.6)
print(f' a sua jornada como um {classe} começa agora!{bcolors.reset}\n')
#fim da customização de personagem

# Exemplo de uma batalha
sleep(1.5)
print('Você está andando numa floresta..')
sleep(1.5)
batalha(classe,PV,PVM,'goblin',50,[5,10,15],{'poção de vida':2,'poção de dano':2})