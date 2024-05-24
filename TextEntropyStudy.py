# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:29:29 2023

@author: tc.vreginato
"""
from math import log2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import log

# criar classe: input de um texto, método automatico de corrigar acentos/cidilha etc...

class TextoEntropia():
    def __init__(self,nomeArquivo):
        with open(nomeArquivo, 'r',encoding='utf-8') as f:
            self.TextoStr = f.read()
        
        #Tratando o texto, tirando acentos e colocando em minusculoo
        self.TextoStr = self.TextoStr.lower().replace("\n"," ").replace("é","e").replace("ç","c").replace("ã","a").replace("ó","o").replace("õ","o").replace("à","a").replace("ô","o").replace("í","i")
        
        
        
        #inicialização do dicionario, a primeira coordenada é o número de aparições da letra, e segunda é a prob associada
        self.dicionarioContagem = {"a":[0,0],"b":[0,0],"c":[0,0],"d":[0,0],"e":[0,0],"f":[0,0],"g":[0,0],"h":[0,0],"i":[0,0]
                                   ,"j":[0,0],"k":[0,0],"l":[0,0],"m":[0,0],"n":[0,0],"o":[0,0],"p":[0,0],"q":[0,0]
                                   ,"r":[0,0],"s":[0,0],"t":[0,0],
                                   "u":[0,0],"v":[0,0],"w":[0,0],"x":[0,0],"y":[0,0],"z":[0,0]}
        
        self.totalLetras = 0
        
        self.textoSoComLetras = str()
        
        self.entropiaDaFonte = 0
        
        self.__gerarContagemEProbabilidade()
        
        
        self.dicionarioContagem = dict(sorted(self.dicionarioContagem.items(), key=lambda x: x[1]))
        
    
    def __gerarContagemEProbabilidade(self):
        for letra in self.TextoStr:
            if letra in self.dicionarioContagem:
                self.dicionarioContagem[letra][0] += 1
                self.totalLetras += 1
                self.textoSoComLetras += letra
                
        for letra in self.dicionarioContagem:
            self.dicionarioContagem[letra][1] += self.dicionarioContagem[letra][0]/self.totalLetras
            if self.dicionarioContagem[letra][1] != 0:
                self.entropiaDaFonte += -self.dicionarioContagem[letra][1]*log(self.dicionarioContagem[letra][1],2)
    
    def probSequencia(self,sequencia):

        contagemSequencia = 0
        
        totalSequencias = len(self.TextoStr) - len(sequencia) + 1
        totalSuposta = 0
        if type(sequencia) == str:
            
            for i in range(0,len(self.TextoStr)-len(sequencia)+1):
                if self.TextoStr[i:i+len(sequencia)] == sequencia:
                    contagemSequencia +=1
                totalSuposta += 1
                    
            probSequencia = contagemSequencia/totalSequencias
            #print(f"A Probabilidade da sequência '{sequencia}' é {probSequencia}")
            return probSequencia
            
        else:
            print("Entrada precisa ser uma string")
        
     # o primeiro argumento é a letra da sequencia condicionada,o segundo é letra que condiciona a sequencia e o terceiro é o booleano que pergunta se "letra" é a primeira letra da sequencia ou nao, True é o padrão       
    def probSequenciaCondionadaDeDuasLetras(self,letra, letraCondicional, primeiraLetra = True):

    
        if (primeiraLetra):
                probLetraCondicionada = 0
                seq = letra + letraCondicional
                for letraa in self.dicionarioContagem:
                    probLetraCondicionada += self.probSequencia(letraa + letraCondicional)
                probSeq = self.probSequencia(seq)/probLetraCondicionada
                print(f'Prob da letra "{letra}" ser o primeiro caractere da sequência dado que a segunda letra é ""{letraCondicional}"" (sequencia condionada)": {probSeq} ')

        else:
                probLetraCondicionada = 0
                seq = letraCondicional + letra
                for letraa in self.dicionarioContagem:
                    probLetraCondicionada += self.probSequencia(letraCondicional+letraa)
                probSeq = self.probSequencia(seq)/probLetraCondicionada
                print(f'Prob da letra "{letra}" dado que a primeira letra é "{letraCondicional}" (sequencia condionada)": {probSeq} ')
        return probSeq
        
        
    def gerarHistograma(self):
        fig, ax = plt.subplots()

        letras =list(self.dicionarioContagem.keys())
        counts = [self.dicionarioContagem[letra][0] for letra in self.dicionarioContagem]
        bar_labels = letras


        ax.bar(letras, counts)

        ax.set_ylabel('Número de aparições')
        ax.set_title(f"Número de ocorrência das letras do alfabeto em'Alice no País das Maravilhas' em Inglês")
        
    
    def printProbEnumeroletra(self,letra):
        for letraList in self.dicionarioContagem:
            if letraList == letra:
                print(f"Número de aparições da letra {letra} = {self.dicionarioContagem[letra][0]}\n")
                print(f"prob de apararição da letra {letra} = {self.dicionarioContagem[letra][1]} \n")
    
    def mostrarTodasAsLetrasEProbabilidades(self,dicionario):
        
        for letraList in dicionario:
            if len(dicionario[letraList]) == 2:
                print(f"{letraList}\t{dicionario[letraList][1]}")
            else:
                print(f"prob de apararição da sequência {letraList} = {dicionario[letraList]} \n")
                
        
    def achaSeqMaisProvavel(self):
        seqMaisProvavel = str()
        probSeqMaisProvavel = 0
        for primeiraLetra in self.dicionarioContagem:
            for segundaLetra in self.dicionarioContagem:
                seqAux = primeiraLetra + segundaLetra
                probAux = self.probSequencia(seqAux)
                if probAux>probSeqMaisProvavel:
                    seqMaisProvavel = seqAux
                    probSeqMaisProvavel = probAux
                    
        print(f'A sequencia mais provavel é "{seqMaisProvavel}" com probabilidade {probSeqMaisProvavel}')
            
        
        
textoIngles = TextoEntropia("AliceEmInglestxt.txt")
textoPortugues = TextoEntropia("AliceEmPortguestxt.txt")


#Histogramas
textoIngles.gerarHistograma()
textoPortugues.gerarHistograma()

#Acha sequencias mais provaveis (execução demorada)
textoIngles.achaSeqMaisProvavel()
textoPortugues.achaSeqMaisProvavel()

#Printa número e letra
textoIngles.mostrarTodasAsLetrasEProbabilidades(textoIngles.dicionarioContagem)
textoPortugues.mostrarTodasAsLetrasEProbabilidades(textoPortugues.dicionarioContagem)

#prob da letra r dado que a primeira letra anterior é a
textoPortugues.probSequenciaCondionadaDeDuasLetras("r", "a")
    