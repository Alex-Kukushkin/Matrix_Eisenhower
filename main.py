import socket
import controllers as CR


def run():
    """ Запуск соединения """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()
    print('Сервер запущен')

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(4096)

        if request:
            response = cr.generate_response(request.decode('utf-8'))

            client_socket.sendall(response)
            client_socket.close()


if __name__ == '__main__':
    cr = CR.ControllersResponses()
    run()
