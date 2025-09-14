import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    """Специальный класс, который отвечает за
    обработку входящих запросов от клиентов."""

    def do_GET(self) -> None:
        """Метод для обработки входящих GET-запросов."""
        url = "https://raw.githubusercontent.com/Andrievskis/Lesson_21_2/feature/basics_of_layout/contacts.html"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                content = response.text

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))

            else:
                error_html = "<html><body><h1>Ошибка загрузки страницы</h1></body></html>"
                self.send_response(response.status_code)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(error_html.encode("utf-8"))

        except requests.exceptions.RequestException as e:
            error_html = f"<html><body><h1>Внутренняя ошибка сервера: {str(e)}</h1></body></html>"
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(error_html.encode("utf-8"))

    def do_POST(self) -> None:
        """Обрабатывает POST-запрос, выводит данные в консоль и возвращает страницу."""
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode("utf-8")
            form_data = urllib.parse.parse_qs(post_data)

            for key, values in form_data.items():
                print(f" {key}: {values[0]}")

            url = "https://raw.githubusercontent.com/Andrievskis/Lesson_21_2/feature/basics_of_layout/contacts.html"
            response = requests.get(url)

            if response.status_code == 200:
                content = response.text
            else:
                content = "<html><body><h1>Ошибка загрузки страницы</h1></body></html>"

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        except requests.exceptions.RequestException as e:
            error_html = f"<html><body><h1>Ошибка загрузки страницы: {str(e)}</h1></body></html>"
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(error_html.encode("utf-8"))

        except Exception as e:
            error_html = f"<html><body><h1>Ошибка обработки POST: {str(e)}</h1></body></html>"
            self.send_response(500)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(error_html.encode("utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
