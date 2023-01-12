from http.server import BaseHTTPRequestHandler, HTTPServer


hostName = "localhost"
serverPort = 80


class MyServer(BaseHTTPRequestHandler):
    """Temp"""

    def do_GET(self):
        """Get"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org"
                               "</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: </p>"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
