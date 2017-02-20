#!/usr/bin/python


import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind(('localhost', 1239))

mySocket.listen(5)

suma = 0;
i = 0;

def answer (numero,msg,error):
    if not error:
        htmlAnswer = "<html><body>"
        htmlAnswer += "<p><h5>" + msg + "</h5></p>"
        htmlAnswer += "</body></html>"
        print (msg)
    else:
        htmlAnswer = "<html><body>"
        htmlAnswer += "<p><h5>" + msg + ' ' + str(numero) + '\n' +"</h5></p>"
        htmlAnswer += "<p><h3>"'Dame un numero.'+ "</h3></p>"
        htmlAnswer += "</body></html>"
        print (chr(27) + "[0;31m" + msg + ' ' + numero + chr(27) + "[0m\n")

    return htmlAnswer

def sumar (suma,numero,i):
	if i == 0 or i == 1:
		if i == 0:
			msg = 'Primer numero recibido: ' + str(numero)
			msg += '. Dame otro numero.'
			suma = suma + numero
		if i == 1:
			msg = 'Segundo numero recibido: ' + str(numero)
			msg += '. La suma de ' + str(numero) + ' + '
			msg += str(suma) + ' es '
			suma = suma + numero
			msg += str(suma)
		i = i + 1
	elif i >= 2:
		suma = 0
		i = 0
		msg = 'Primer numero recibido: ' + str(numero)
		msg += '. Dame otro numero.'
		suma = suma + numero
		i = i + 1

	return suma, i, msg

try:
    while True:
        error = False
        print ('Waiting for connections..')
        (recvSocket, address) = mySocket.accept()

        ### Recibido
        print ('Request received:\n')
        peticion = recvSocket.recv(2048).decode("utf-8","strict") #la petición, con encode bytes pasados a utf-8
        print (peticion)

        try:
            numero = int(peticion.split()[1][1:]) #split() separa por saltos de linea y espacios
        except ValueError:
            error = True
            numero = peticion.split()[1][1:]
            if numero == '':
            	msg = 'No he recibido un numero, en verdad no he recibido nada.'
            else:
            	msg = 'No he recibido un numero. He recibido:'
            htmlError1 = answer(numero, msg, error)
            recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" + htmlError1 +
                                "\r\n", 'utf-8'))
            recvSocket.close()
            continue

        if not error:
            [suma, i, msg] = sumar(suma,numero,i)

        ### Respuesta si todo va bien
        print ('Answering back...')
        htmlAnswer = answer(numero, msg, error)
        recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" + htmlAnswer +
                        "\r\n", 'utf-8'))
        recvSocket.close()

        #print ('SUMA:',suma, '\nI:', i) #Traza indexaciones

except KeyboardInterrupt:
    print ("\n¡CLOSING BINDED SOCKET!")
    mySocket.close()
