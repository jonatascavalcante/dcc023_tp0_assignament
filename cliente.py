import sys
import socket
import errno
from struct import *

MSG_TAMANHO_MAX = 6
CLIENT_TIME_OUT = 15

def gera_mensagem(entrada):
    dados = entrada.split(" ")
    sinal_entrada = dados[0]
    valor = dados[1]
    sinal_saida = 0

    if(sinal_entrada == "+"):
        sinal_saida = 1
    elif(sinal_entrada == "-"):
        sinal_saida = 0

    return pack("!BI", int(sinal_saida), int(valor))

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 3:
    print("python cliente.py [ENDERECO] [PORTA]")
enderecoIP = sys.argv[1]
porta      = int(sys.argv[2])

# Criacao do socket
time_out = pack('ll', CLIENT_TIME_OUT, 0)
socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, time_out)

# Conexao (abertura ativa)
endServidor = (enderecoIP, porta)

socket_cliente.connect(endServidor)

for entrada in sys.stdin:
    mensagem = gera_mensagem(entrada)
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
   	    
# Finalizacao
socket_cliente.close()
