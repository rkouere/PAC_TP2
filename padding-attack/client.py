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

def getBloc(cypher, nbrBlock):
    if nbrBlock*32 >= len(cypher):
        return -1
    else:
        return cypher[nbrBlock * 32:(nbrBlock + 1) * 32]


# get a seed with 01 as the last byte
def getSeed(i):
    while 1:
        try:
            seed = server.query("/padding-attack/last-byte/echallier/"+str(i), {"value": "01"})
            if seed['status'] == 'OK':
                print("seed working = " + str(i))
                return i
                break
        except:
            print("seed dead")
            i = i + 1

def bytes_to_hex(bytes_to_encode):
    return base64.b16encode(bytes_to_encode)

def string_hex_to_bytes(string_to_encode):
    return base64.b16decode(string_to_encode.encode())

URL="http://pac.bouillaguet.info/TP2"
server = Server(URL)

oracle="/padding-attack/oracle/echallier"

seedNum = 3

seed=server.query("/padding-attack/challenge/echallier/" + str(seedNum))


cypher=seed['ciphertext']
IV=seed['IV']
#le IV que l'on va manipuler
C = getBloc(cypher, 11)
C_original = getBloc(cypher, 11)

#le ciphertext que l'on va envoyer
cipherTextHack = getBloc(cypher, 12)
#le valeur intermediaire que l'on cherche a trouver
index_du_cypher = "01"
IntValue = []
CLimiter = 32
#IntValue.insert(0, 0x)
print(C)
print("--------")
# on va xorer la fin de C avec 01 puis avec 02 afin que sa valeur soit valide avec un padding de 2
#on va avoir un compteur pour changer les bon octets de l'IV
# comptIV = 1
# for y in range(comptIV):
#     format = y+1
#     plaintext = "{0:032x}".format(format)
#     C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))

#     #On xor C avec le 02
#     format = format + 1
#     plaintext = "{0:032x}".format(format)
#     C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))




#On xor C avec le 01
print(C)

# on change la valeur des bytes à 1 et on va les incrementer
#C = C.decode()
C = C[0:CLimiter-2] + "00" + C[CLimiter:CLimiter+2]
print(C)

# on va essayer de trouver la valeur intermediaire dont on a besoin pour avoir la valeur que l'on veut
format = 0x79
for i in range(0x79, 256):
    # on va incrementer de 1 le masque à chaque itérations
    plaintext = "{0:032x}".format(format)
    IV_tmp=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))
    format = (i + 1)
    print("plaintext = " + plaintext)
    result = server.query(oracle, {"IV": IV_tmp.decode(), "ciphertext": cipherTextHack})
    if(result['status'] == 'OK'):
        # on a besoin de tout transofmer en bytes pour pouvoir utiliser la fonction xor
        # on a besoin du C
        tmp1 = base64.b16decode(IV_tmp[CLimiter-2:CLimiter])
        # on a besoin de l'index pour connaitre la valeur que l'on "hackait"
        tmp2 = base64.b16decode(index_du_cypher.encode())
        # la valeur intermediaire
        tmp3 = base64.b16encode(xor(tmp1, tmp2)).decode()
        IntValue.insert(-int(index_du_cypher), base64.b16encode(xor(base64.b16decode(C_original[CLimiter-2:CLimiter]), base64.b16decode(tmp3))).decode())
        break





iterator = int(index_du_cypher)
C=getBloc(cypher, 11)
# on va faire le xor qu'il faut pour recuperer 
tmp1 = string_hex_to_bytes(C[CLimiter-2:CLimiter])
tmp2 = string_hex_to_bytes(IntValue[-int(index_du_cypher)])

print(bytes_to_hex(xor(tmp1, tmp2)))
index_du_cypher = str(int(index_du_cypher) + 1)
C = C[0:CLimiter-2] + "00" + C[CLimiter:CLimiter+2]










# tmp1 = base64.b16decode(C[30:32])
# tmp2 = base64.b16decode(IntValue[-iterator])
# value_of_plainText = base64.b16encode(xor(tmp1, tmp2))
# print(base64.b16decode(value_of_plainText))
# print("---------")
# tmp2 = base64.b16encode(xor(base64.b16decode(value_of_plainText), tmp1))
# print(tmp2)
# print("----------")
# iterator = 1
# # on va xorer la fin de C avec la valeur que l'on connait de la fin du ciphertext puis avec 02 afin que sa valeur soit valide avec un padding de 2
# # on a vire C donc il faut le recuperer
# valuePadding = iterator + 1
# format = IntValue[-iterator]
# plaintext = "{0:032x}".format(format)
# C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))

# #On xor C avec le 02
# format = valuePadding
# plaintext = "{0:032x}".format(format)
# C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))


# ORIGINAL marche avec 1
# on va xorer la fin de C avec la valeur que l'on connait de la fin du ciphertext puis avec 02 afin que sa valeur soit valide avec un padding de 2
# iterator = 1
# valuePadding = iterator + 1
# format = IntValue[-iterator]
# plaintext = "{0:032x}".format(format)
# C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))

# #On xor C avec le 02
# format = valuePadding
# plaintext = "{0:032x}".format(format)
# C=base64.b16encode(xor(base64.b16decode(C), base64.b16decode(plaintext, casefold=True)))

