import sys
import socket
from struct import *

MSG_TAMANHO_MAX = 5
MAX_CLIENTES    = 10
MODULO_MAX 	    = 1000000
QTD_DIGITOS     = 6
TIME_OUT 	    = 15

def decodifica_mensagem(mensagem, contador):
	sinal = mensagem[0]
	valor = mensagem[1:]

	valor = unpack("!I", valor)
	valor = valor[0]

	# Interpreta o valor do cliente e realiza a operacao correspondente
	if sinal == '0':
		contador -= valor
	elif sinal == '1':
		contador += valor

	contador = contador % MODULO_MAX

	return contador

# Monta o valor da resposta como string de seis caracteres
def monta_resposta(contador):
	resposta  = ''
	qtd_zeros = QTD_DIGITOS - len(str(contador))

	while qtd_zeros > 0:
		resposta += '0'
		qtd_zeros -= 1

	resposta += str(contador)

	return resposta

# Fim das definicoes das funcoes

# Leitura da porta a ser atribuida ao servidor
if len(sys.argv) < 2:
	print("python servidor.py [PORTA]")

porta = int(sys.argv[1])

# Criacao do socket
# Criacao do socket
time_out = pack('ll', TIME_OUT, 0)
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, time_out)

# Abertura passiva
endereco = ("", porta)
socket_servidor.bind(endereco)
socket_servidor.listen(MAX_CLIENTES)

contador = 0

while True:
	socket_cliente, cliente = socket_servidor.accept()

	# Comunicacao entre o servidor e o cliente
	while True:
		mensagem = socket_cliente.recv(MSG_TAMANHO_MAX)

		# Falha ao receber a mensagem
		if not mensagem:
			break

		contador = decodifica_mensagem(mensagem, contador)
		resposta = monta_resposta(contador)

		nbytes = socket_cliente.send(resposta)
		if nbytes != len(resposta):
			break

	# Finalizacao
	socket_cliente.close()

socket_servidor.close()
