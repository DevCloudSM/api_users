#a faire jeudi
from flask import Flask, request, Response
from werkzeug.middleware.proxy_fix import ProxyFix
import requests

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/service1/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_service1(path):
    url = 'http://localhost:5000/' + path
    response = requests.request(method=request.method, url=url, headers=request.headers, data=request.get_data())
    return Response(response.content, status=response.status_code, headers=dict(response.headers))

if __name__ == '__main__':
    app.run(port=5000)

