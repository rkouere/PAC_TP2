import json
import urllib.request
import urllib.parse
import urllib.error
import base64
import helpers


# excelente explication
#http://blog.gdssecurity.com/labs/2010/9/14/automated-padding-oracle-attacks-with-padbuster.html

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


# seed 1
oracle="/padding-attack/oracle/echallier"

seed=server.query("/padding-attack/challenge/echallier/1")
cypher=seed['ciphertext']
IV=seed['IV']
#on va traiter les 32 derniers chracter
ciphertext = cypher[(len(cypher) - 32):]
IVTmp = 
# c'est le nombre que l'on va utiliser pour incrémenter le dernier bit
format = 0x00
print(cypher)
print(ciphertext)
print(IVTmp)

# for i in range(256):
#     # on va incrementer de 1 le masque à chaque itérations
#     plaintext = "{0:032x}".format(format)
#     tmp=base64.b16encode(xor(base64.b16decode(ciphertext), base64.b16decode(plaintext, casefold=True)))
#     format = format + 1
#     print("tmp = " + tmp.decode())
#     print("plaintext = " + plaintext)
#     print(server.query(oracle, {"IV": ciphertext, "ciphertext": tmp.decode()}))

# on va incrementer de 1 chaque mask
# format = format + 255

# plaintext = "{0:032x}".format(format)
# tmp=base64.b16encode(xor(base64.b16decode(ciphertext), base64.b16decode(plaintext, casefold=True)))
# format = format + 1
# print(ciphertext)
# print(tmp.decode())
# print(server.query(oracle, {"IV": ciphertext, "ciphertext": tmp.decode()}))




#print(server.query(oracle, {"IV": ciphertext, "ciphertext": tmp.decode()}))

# print(len(ciphertext))
# print(ciphertext)

# tmp=base64.b16encode(xor(base64.b16decode(ciphertext), base64.b16decode(plaintext)))

#print(server.query(oracle, {"IV": ciphertext, "ciphertext": tmp.decode()}))
