import sys
import socket
from struct import *

MSG_TAMANHO_MAX = 5
MODULO_MAX 	    = 1000000
QTD_DIGITOS     = 6

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 2:
	print("python servidor.py [PORTA]")

porta = int(sys.argv[1])

# Criacao do socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Abertura passiva
endereco = ("", porta)
socket_servidor.bind(endereco)

contador = 0

while True:
	socket_cliente, cliente = socket_servidor.accept()

	# Comunicacao entre o servidor e o cliente
	while True:
		mensagem = socket_cliente.recv(MSG_TAMANHO_MAX)

		# Falha ao receber a mensagem
		if not mensagem:
			break;

		# TODO: Separar os bytes da mensagem do cliente
		sinal = 
		valor = 

		unpack("!I", valor)

		# Interpreta o valor do cliente e realiza a operacao correspondente
		if sinal == 0
			contador -= valor
		elif sinal == 1
			contador += valor
		contador = contador % MODULO_MAX

		# Monta o valor da resposta como string de seis caracteres
		resposta  = ''
		qtd_zeros = QTD_DIGITOS - len(contador)

		while qtd_zeros > 0:
			resposta += '0'
			qtd_zeros -= 1

		resposta += str(contador)

		nbytes = socket_cliente.send(resposta)
		if nbytes != len(msg):
			break

	# Finalizacao
	socket_cliente.close()

socket_servidor.close()
