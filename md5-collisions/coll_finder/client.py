import json
import urllib.request
import urllib.parse
import urllib.error
import base64

class ServerError(Exception):
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = None

class Server:
    def __init__(self, base_url):
        self.base = base_url

    def query(self, url, parameters=None ):
         """Charge l'url demandée. Si aucun paramètre n'est spécifié, une requête
            HTTP GET est envoyée. Si des paramètres sont présents, ils sont encodés
            en JSON, et une requête POST est envoyée.

            La méthode préconisée pour envoyer des paramètres consiste à les stocker
            dans un dictionnaire. Ceci permet de nommer les champs. Par exemple :

            # sans paramètres
            >>> server = Server("http://pac.bouillaguet.info/TP1/")
            >>> response = server.query('client-demo')
            >>> print(response)
            Je n'ai pas reçu de paramètres

            #    avec paramètres
            >>> parameters = {'login': 'toto', 'id': 1337}
            >>> response = server.query('client-demo', parameters)
            >>> print(response)
            Dans les paramètres j'ai trouvé :
            *) ``login'' : ``toto''
            *) ``id'' : ``1337''
            <BLANKLINE>
         """
         url = self.base + url
         try:
            request = urllib.request.Request(url)
            data = None
            if parameters is not None:
                data = json.dumps(parameters).encode()
                request.add_header('Content-type', 'application/json')
            with urllib.request.urlopen(request, data) as connexion:
                result = connexion.read().decode()
                if connexion.info()['Content-Type'] == "application/json":
                    result = json.loads(result)
            return result
         except urllib.error.HTTPError as e:
             raise ServerError(e.code, e.read().decode()) from None
def xor(a, b):
           c = bytearray()
           for x,y in zip(a,b):
               c.append(x ^ y)
           return c

URL="http://pac.bouillaguet.info/TP2"
server = Server(URL)

f = open("ex1_1.txt", "rb")
m0 = base64.b16encode(f.read())

f = open("ex1_2.txt", "rb")
m1 = base64.b16encode(f.read())


print(server.query("/md5-collisions/checker/echallier", {0: "656368616c6c696572206c6c6c6d6e617a6a68666c64666c7164736a6673716a666b6a646b7366686e6b736a68666473716a666a666471736b666a6b736f640aa5aa8e2a93cbb3fe7dff33f72885884cbc6459c5a22819081a723f2eb5b594869eacf7e5d86ded7c6b0e5e02aed36c21f6cbeac94a78750f852ddd5a4cef82bbb6dd226565a0eab09d7ed08ba656ed97d797467b7c1d92e82db320583b6068a7cf932018a745be557703485b53202097255ba588e0764e29dac32f947d6f386c2050414320504f574141414141414141414141", 1: "656368616c6c696572206c6c6c6d6e617a6a68666c64666c7164736a6673716a666b6a646b7366686e6b736a68666473716a666a666471736b666a6b736f640aa5aa8e2a93cbb3fe7dff33f72885884cbc645945a22819081a723f2eb5b594869eacf7e5d86ded7c6b0e5e02ae536d21f6cbeac94a78750f852dddda4cef82bbb6dd226565a0eab09d7ed08ba656ed97d79746fb7c1d92e82db320583b6068a7cf932018a745be557703485b53a01f97255ba588e0764e29dac32f147d6f386c2050414320504f574141414141414141414141"}))
