from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за
    обработку входящих запросов от клиентов."""

    def do_GET(self):
        """Метод для обработки входящих GET-запросов."""
        # url = ''
        # response = requests.get(url)
        # if response.status_code == 200:
        #     data = response.text
        # else:
        #     data = "<html><body><h1>Error loading page</h1></body></html>"
        try:
            with open('contacts.html', 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, "Файл contacts.html не найден на сервере.")
        except Exception as e:
            self.send_error(500, f"Внутренняя ошибка сервера: {str(e)}")

    def do_POST(self):
        """Обрабатывает POST-запрос, выводит данные в консоль и возвращает страницу."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = urllib.parse.parse_qs(post_data)

            for key, values in form_data.items():
                print(f" {key}: {values[0]}")

            with open('contacts.html', 'r', encoding='utf-8') as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            self.send_error(500, f"Ошибка обработки POST: {str(e)}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
