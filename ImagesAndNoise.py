# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:25:55 2023

@author: tc.vreginato
"""
import random
import numpy as np
from PIL import Image

ImagePath = r'C:\Users\tc.vreginato\OneDrive - Padtec\Área de Trabalho\Graduação\F349\Trab2\ImageLeao.png'  #mudar o caminho da imagem


def printImage(Image):
    Image.show() 
    
def image_to_matrix_boolean(image_path):
    with Image.open(image_path) as img:
        img = img.convert('1')
        matrix = np.array(img)
        #printImage(img)
    return matrix.astype(bool)


def matrix_boolean_to_Image(BooleanMatrix):
    ImagemDepoisCanalRuidoso = np.where(BooleanMatrix, 255, 0).astype('uint8')
    img = Image.fromarray(ImagemDepoisCanalRuidoso)
    return img

def aplicarCanalBinárioSimétrico(ImageBool,epsolon):
    ImagemRuidosaBool = [[False for k in range(len(ImageBool[0]))] for l in range(len(ImageBool))]
    if (epsolon <= 1 and epsolon > 0):
        for i in range(len(ImageBool)):
            for j in range(len(ImageBool[i])):
                    if(random.randrange(1000) > epsolon*1000):  # a função random.randrange(x) retorna (pseudo aleatoriamente) um numero entre 0 e x
                        ImagemRuidosaBool[i][j] = ImageBool[i][j]
                    else:
                        ImagemRuidosaBool[i][j] = not(ImageBool[i][j])
        #printImage(matrix_boolean_to_Image(ImagemRuidosaBool))
        return  ImagemRuidosaBool
        
    else:
         print("Epsolon precisa ser menor ou igual a 1 e maior que zero")
         

    



    
#def aplicarCorreçãoDeErroHamming(ImageRuidosa):
    
def calculaTaxaErro(ImagemBoolTransmitida,ImagemBoolRecebida):
     totalPixels = len(ImagemBoolTransmitida)*len(ImagemBoolTransmitida[0])
     erros = 0
     for i in range(len(ImagemBoolTransmitida)):
         for j in range(len(ImagemBoolTransmitida[i])):
             if ImagemBoolTransmitida[i][j] != ImagemBoolRecebida[i][j]:
                 erros += 1
     return erros/totalPixels            
    
def aplicarCorreçãoDeErroRepetição(nRepeticao,ImagemTransmitida,ProbErro):
    if(type(nRepeticao) == int and nRepeticao%2 == 1):
        
        MatrizCanalRepetido = [aplicarCanalBinárioSimétrico(ImagemTransmitida, ProbErro) for i in range(nRepeticao)] #matriz com a tramissão de nRepetição imagens transmitidas com ruido
        
        ImagemPósCorrecaoBoolean = [[False for k in range(len(ImagemTransmitida[0]))] for l in range(len(ImagemTransmitida))] #declarando a matriz associada a imagem corrigida
        
        for i in range(len(ImagemTransmitida)):
            for j in range(len(ImagemTransmitida[i])):
                nZeros = 0 #variável do número de "0" associado ao mesmo elemento de todas as matriz transmitidas através do canal ruidoso
                for k in range(nRepeticao):
                    if(not(MatrizCanalRepetido[k][i][j])):
                        nZeros += 1
                if nZeros > nRepeticao//2:
                    ImagemPósCorrecaoBoolean[i][j] = True
                else:
                    ImagemPósCorrecaoBoolean[i][j] = False
        return ImagemPósCorrecaoBoolean
    else:
        print("o número de repetições precisa ser impar e  inteiro")
    
#imagemBooleanPosCorreçãoDeRepetição = aplicarCorreçãoDeErroRepetição(3, ImageBitMap, 0.9)

                
#imgPosCorreção = matrix_boolean_to_Image(imagemBooleanPosCorreçãoDeRepetição)

#printImage(imgPosCorreção)     
    

ImageBitMap = image_to_matrix_boolean(ImagePath)


# variação da probilidade de erro
epsolons = [0.1, 0.2, 0.5, 0.7, 1]

for epsolon in epsolons:
    aplicarCanalBinárioSimétrico(ImageBitMap,epsolon)
    
#-------------------------------

#Correção repetição
for repetições in range(1,11,2):
    imagemRecebidaBoolean = aplicarCorreçãoDeErroRepetição(repetições,ImageBitMap,0.45)
    printImage(matrix_boolean_to_Image(imagemRecebidaBoolean))

print(calculaTaxaErro(ImageBitMap, imagemRecebidaBoolean))





















