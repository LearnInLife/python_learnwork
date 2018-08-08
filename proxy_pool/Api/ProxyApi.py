# -*- coding:utf-8 -*-


from flask import Flask, jsonify, request
from werkzeug.wrappers import Response
from Util.GetConfig import GetConfig
from Manager.ProxyManager import ProxyManager

app = Flask(__name__)


class JsonResponse(Response):

    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, dict)):
            response = jsonify(response)
        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse

api_list = {
    'get': u'get an usable proxy',
    'get_all': u'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8080': u'delete an unable proxy',
    'get_status': u'proxy statistics'
}


@app.route('/')
def index():
    return api_list


@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return proxy if proxy else 'no proxy!'


@app.route('/get_all/')
def get_all():
    proxies = ProxyManager().getAll()
    return proxies


@app.route('/delete/', methods=['GET'])
def delete():
    proxy = request.args.get('proxy')
    ProxyManager().delete(proxy)
    return 'success'


@app.route('/get_status/')
def get_status():
    status = ProxyManager().getNumber()
    return status


def run():
    config = GetConfig()
    app.run(host=config.host_ip, port=config.host_port)


if __name__ == '__main__':
    run()
