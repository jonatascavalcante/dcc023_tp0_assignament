import sys
import socket
from struct import *

MSG_TAMANHO_MAX = 6
TIME_OUT 	    = 15

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
time_out = pack('ll', TIME_OUT, 0)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, time_out)

# Conexao (abertura ativa)
endServidor = (enderecoIP, porta)

socket_cliente.connect(endServidor)

# Aguarda entrada do teclado
entrada_dados = le_teclado()

while True:
    mensagem = gera_mensagem(entrada_dados)
    nbytes = socket_cliente.send(mensagem)
    if nbytes != len(mensagem):
        break
    try:
    	resposta = socket_cliente.recv(MSG_TAMANHO_MAX)
    except socket.error, error:
    	erro_socket = error.args[0]
    	if erro_socket == errno.EAGAIN or erro_socket == errno.EWOULDBLOCK:
    		break
    		
    if not resposta:
        break
    print resposta
   	    
    entrada_dados = le_teclado()

# Finalizacao
socket_cliente.close()
