from http.server import BaseHTTPRequestHandler, HTTPServer
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import sys



host_name = "0.0.0.0"
port = 8080
URL = "https://www.sreality.cz/en/search/for-sale/apartments"

all_titles = []
all_images = []


class Client(QWebEnginePage):
    # Code intended for rendering the JavaScript content on the page (most of the content is from JS)
    def __init__(self, url):
        QWebEnginePage.__init__(self)
        self.html = ""
        self.loadFinished.connect(self.on_load_finished)
        self.load(QUrl(url))
        app.exec_()

    def on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print("Load Finished")

    def Callable(self,data):
        self.html = data
        app.quit()


class TestServer(BaseHTTPRequestHandler):
    def make_output(self):
        res = ""
        i = 1
        for title, img_src in zip(all_titles, all_images):
            res += f"<p>Result {i}: {title} <img src={img_src}></p> "
            i += 1

        return res


    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>Luxonis Test</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes(self.make_output(), "utf-8"))
        #self.wfile.write(bytes("<p> Hello world </p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))


def scrape(num_pages):
    for page in range(1, num_pages + 1):
        new_URL = f"{URL}?page={page}"
        client_response = Client(new_URL)

        soup = BeautifulSoup(client_response.html, "html.parser")
        flats = soup.find_all("div", class_="property ng-scope")

        for flat in flats:
            title = flat.find("span", class_="name ng-binding").text
            imgs = flat.find_all("img")

            all_titles.append(title)
            all_images.append(imgs[0]["src"])  # just take first img



if __name__ == "__main__":
    global app
    app = QApplication(sys.argv)
    scrape(2)
    print(len(all_titles), len(all_images))
    server = HTTPServer((host_name, port), TestServer)
    print("Running @ http://%s:%s" % (host_name, port))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped")
