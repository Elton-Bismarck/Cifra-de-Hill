#Parte da importação das bilbiotecas usadas, da declaração da chave e da
#declaração das Funções que transformarão o texto em número para a execução das operações e retorna em texto novamente

import numpy as np
import sympy as sp

#Número de caracteres = 113
chave = np.array([[1, 3, 0],
                  [2, 5, 1],
                  [2, 1, 3]])
#Verificação se MDC(det(chave),Número de caracteres)
det = sp.Matrix(chave).det()

#Converte letra em número
def Conversaoemnumero(letra):
  caracteres = "abcdefghijklmnopqrstuvwxyzáàâãéêíóõôúçABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÕÔÚÜÇ–-_.,:;?!()[]{}=+/\@#%&*| 0123456789"
    
  return (1 + caracteres.find((letra)))

#Converte número em letra
def Conversaoemcaractere(numero):
    caracteres = "abcdefghijklmnopqrstuvwxyzáàâãéêíóõôúçABCDEFGHIJKLMNOPQRSTUVWXYZÁÀÂÃÉÊÍÓÕÔÚÜÇ–-_.,:;?!()[]{}=+/\@#%&*| 0123456789"

    return (caracteres[numero - 1])

#Função que retorna o tamanho do texto
def tamanhotexto(texto):
  return int(len(texto))

#Transforma a mensagem numa matriz
def recebertexto(texto):            
  comf = int(len(texto))            #Tamanho do texto
  comp = int(comf/3) + 1            #Número de linhas da matriz
  b = (3, comp)                     #Determina a ordem da matriz texto com base na matriz chave, para que Ncolunas da chave = Nlinhas do texto
  textocrip = np.zeros(b)           #Cria a matriz recipiente para o texto de ordem b
  l = -1
  for i in range(3):
    for j in range(comp):
      l = l + 1    
      if l<comf:                    #Parte que não permite que se extrapole a quantidade de caracteres da frase texto
        textocrip[i,j] = Conversaoemnumero(texto[l])

  return textocrip

#Transforma a matriz numérica em texto novamente
def transftexto(codigo,compcod):    #Código e tamanho do texto
  altura = codigo.shape[0]          #Número de linhas
  largura = codigo.shape[1]         #Número de colunas
  dop = ""                          #Cria uma string recipiente para o texto  
  l = -1
  for i in range(altura):
    for j in range(largura):
      l = l + 1    
      if l<compcod:
        if l<compcod - 1:
          dop = dop[:l] + Conversaoemcaractere(int(codigo[i,j])) + dop[l+1:]     #Divide o string, adiciona um caractere e junta-o novamente
        else:
          dop = dop[:l] + Conversaoemcaractere(int(codigo[i,j])) + dop[l:]       #Caso para o último caractere do texto
      
  return dop 

#Código da criptografia
def criptografa(matexto,matchave,M):            #M = Tamanho do texto 
  #Parte que cifra
  matC = np.matmul(matchave,matexto)            #Matriz da multiplicação da matriz chave com a matriz texto
  alt = matC.shape[0]                           #Calcula o tamanho da matriz formada
  larg = matC.shape[1]
  u = -1
  a = -1
  for g in range(alt):
    for r in range(larg):
      u = u + 1
      if u<=M:
        matC[g,r] = (matC[g,r])%(113)           #Realiza a operação Mod(Número de caracteres do código)
  #Parte que criptografa
  U = np.copy(matchave)                         #Decomposição LU
  n = len(U)   
  L = np.eye(n)
  for j in range(n-1):
    for i in range(j+1,n):
      L[i,j] = U[i,j]/U[j,j]
      for k in range(j+1,n):
        U[i,k] = U[i,k] - L[i,j]*U[j,k]
        U[i,j] = 0

  z = np.linalg.inv(L)                          #Inversa de L
  Cript = np.matmul(z,matC)                     #Multiplicação do texto por L
  for e in range(alt):
    for s in range(larg):
      a += 1
      if a<=M:
        Cript[e,s] = (int(Cript[e,s]))%(113)    #Operação Mod(113)

  return Cript

#Código da descriptografia
def descriptografar(matcript,chave,MT):
  #Determinando U**(-1)
  alt = matcript.shape[0]
  larg = matcript.shape[1]
  f = -1
  q = -1
  imm = pow(2, 111, 113)                       #Calculo do Inverso multiplicativo modular
  
  U = np.copy(chave)
  n = len(U)   
  L = np.eye(n)
  for j in range(n-1):
    for i in range(j+1,n):
      L[i,j] = U[i,j]/U[j,j]
      for k in range(j+1,n):
        U[i,k] = U[i,k] - L[i,j]*U[j,k]
        U[i,j] = 0
  
  adjU = sp.Matrix(U).adjugate()               #Calculo da adjunta da matriz U 

  U1 = adjU*imm
  for e in range(3):
    for s in range(3):
      f += 1
      if f<=MT:
        U1[e,s] = (U1[e,s])%(113)
  
  Mdesc = np.matmul(U1,matcript)
  for y in range(alt):
    for x in range(larg):
      q += 1
      if f<=MT:
        Mdesc[y,x] = (Mdesc[y,x])%(113)
        
  return Mdesc

def principal(chave):
  texto = input('Escreva sua mensagem e pressione enter \n')
  pergunta = input('Deseja criptografar ou descriptografar? \n')
  tmn = tamanhotexto(texto)
  mtexto = recebertexto(texto)
  if pergunta == "criptografar":
    cripto = criptografa(mtexto, chave,tmn)
    print("Texto criptografado:","\n", transftexto(cripto,tmn))
    kayn = input('Deseja descriptografar? \n')
    if kayn == "sim":
      print("Seu texto descriptografado:","\n",transftexto(descriptografar(cripto,chave,tmn),tmn))
    elif kayn == "não":
      print("Obrigado pelo uso")  
  elif pergunta == "descriptografar":
    print("Seu texto descriptografado:","\n",transftexto(descriptografar(recebertexto(texto),chave,tmn),tmn))
     
principal(chave)
input("Obrigado por usar")