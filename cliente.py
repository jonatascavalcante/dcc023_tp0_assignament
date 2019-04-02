import sys
import socket
from struct import *

MSG_TAMANHO_MAX = 7

def le_teclado(): 
	entrada = raw_input()
	if entrada: 
		return entrada

def gera_mensagem(entrada):
	dados = entrada.split(" ")
	sinal = dados[0]
	valor = dados[1]

	if sinal == "+":
		mensagem = '1'
	elif sinal == "-":
		mensagem = '0'
	valor_codificado = pack("!I", int(valor))

	return (mensagem + valor_codificado)

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 3:
    print("python cliente.py [ENDERECO] [PORTA]")
enderecoIP = sys.argv[1]
porta      = int(sys.argv[2])

# Criacao do socket
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conexao (abertura ativa)
endServidor = (enderecoIP, porta)

socket_cliente.connect(endServidor)

# Aguarda entrada do teclado
entrada_dados = le_teclado()

while True:
    mensagem = gera_mensagem(entrada_dados)
    nbytes = socket_cliente.send(mensagem)
    if nbytes != len(mensagem):
        print("Falhou ao enviar a mensagem")
        break

    resposta = socket_cliente.recv(MSG_TAMANHO_MAX)
    if not resposta:
        print("Falhou para receber uma mensagem")
        break
    print resposta
   	    
    entrada_dados = le_teclado()

# Finalizacao
socket_cliente.close()
