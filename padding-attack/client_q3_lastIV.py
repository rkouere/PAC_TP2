import json
import urllib.request
import urllib.parse
import urllib.error
import base64
import helpers


# excelente explication
#http://blog.gdssecurity.com/labs/2010/9/14/automated-padding-oracle-attacks-with-padbuster.html
# text fin
# ['36', '63', '63', '66', '31', '64', '61', '65', '36', '35', '32', '38', '31', '32', '34', '01']


DEBUG = 1
index_du_cypher = 0x01
format_index = 1
IntValue = []
#le valeur intermediaire que l'on cherche a trouver
CLimiterOriginal = 32
CLimiter = CLimiterOriginal


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

def nbr_to_hexa(nbr):
    return "{0:002x}".format(nbr)

def bytes_to_hex(bytes_to_encode):
    return base64.b16encode(bytes_to_encode).decode()

def string_hex_to_bytes(string_to_encode):
    return base64.b16decode(string_to_encode.encode(), casefold=True)

# permet de connaitre la valeur originel du block C à l'index "index/256"
def find_value_plaintext(index):
    global IntValue
    format = index * 0x00
    for i in range(0x00, 257):
        # on va incrementer de 1 le masque à chaque itérations
        plaintext = "{0:032x}".format(format)
        IV_tmp=base64.b16encode(xor(base64.b16decode(C, casefold=True), base64.b16decode(plaintext, casefold=True)))
        format = index * (i + 1)
        result = server.query(oracle, {"IV": IV_tmp.decode(), "ciphertext": cipherTextHack})
        if(DEBUG):
            print(IV_tmp)
            print(plaintext)
        if(result['status'] == 'OK'):
            # on a besoin de tout transofmer en bytes pour pouvoir utiliser la fonction xor
            # on a besoin du C
            tmp1 = base64.b16decode(IV_tmp[CLimiter-2:CLimiter], casefold=True)
            # on a besoin de l'index pour connaitre la valeur que l'on "hackait"
            tmp2 = base64.b16decode(nbr_to_hexa(index_du_cypher), casefold=True)
            # la valeur intermediaire
            tmp3 = base64.b16encode(xor(tmp1, tmp2)).decode()
            if(DEBUG):
                print("tmp3")
                print(tmp3)
                print(IV_tmp[CLimiter-2:CLimiter])
                print("index_dy_cypher")
                print(index_du_cypher)
                
            IntValue.insert(-int(index_du_cypher), base64.b16encode(xor(base64.b16decode(C_original[CLimiter-2:CLimiter], casefold=True), base64.b16decode(tmp3, casefold=True))).decode())
            if(DEBUG):
                print("IntValue")
                print(IntValue[-int(index_du_cypher)])
            return index * 256
            break



def init_block_cracked_oracle():
    global index_du_cypher
    global format_index
    global CLimiter
    C = C_original
    CLimiter = CLimiterOriginal
    for i in range(index_du_cypher):
        tmp1 = string_hex_to_bytes(C[CLimiter-2:CLimiter])
        tmp2 = string_hex_to_bytes(IntValue[-int(i+1)])
        tmp3 = bytes_to_hex(xor(tmp1, tmp2))
        val_C_to_replace = bytes_to_hex(xor(string_hex_to_bytes(nbr_to_hexa(index_du_cypher + 1)), string_hex_to_bytes(tmp3)))
        C = C[0:CLimiter-2] + val_C_to_replace + C[CLimiter:]
        CLimiter = CLimiter - 2
    index_du_cypher = index_du_cypher + 1
    return C[0:CLimiter-2] + "00" + C[CLimiter:]




# DEFINITION DES VARIABLES
URL="http://pac.bouillaguet.info/TP2"
server = Server(URL)
oracle="/padding-attack/oracle/echallier"
seedNum = 135

#53616C757420656368616C6C69657227
#C3
#A9757373692021204E276F75626C696520706173206465202264C3A9636F64657222206365636920656E20756E69636F64652065740A6427656E6C65766572206C652070616464696E672E0A2D2D2D2D2D2D2D2D2D2D0A54686520503443207333727633720A0A736565643A203133350A70736575646F2D72616E646F6D206A756E6B3A20666F6F0A6D61633A203230643266653664393866343466613163366366653338616439323530343332

plain_final ="53616C757420656368616C6C69657227C3A9757373692021204E276F75626C696520706173206465202264C3A9636F64657222206365636920656E20756E69636F64652065740A6427656E6C65766572206C652070616464696E672E0A2D2D2D2D2D2D2D2D2D2D0A54686520503443207333727633720A0A736565643A203133350A70736575646F2D72616E646F6D206A756E6B3A20666F6F0A6D61633A203230643266653664393866343466613163366366653338616439323530343332"


C = plain_final[0:32] + "00" + plain_final[34:]
format = 0

# for i in range(256):
#     val_tmp = "{0:02x}".format(format)
#     format = (i + 1)
#     C = plain_final[0:32] + str(val_tmp) + plain_final[34:38]
#     print(C)
#     try:
#         plaintext = base64.b16decode(C).decode()
        
#         print(server.query("/padding-attack/validation/echallier/"+str(seedNum), {'plaintext': plaintext}))
#         print(C)
#     except:
#         print("bad char")


#plaintext = base64.b16decode(IV_tmp).decode()
plaintext = 'Salut echallier,\n\nBravo, tu as réussi ! N\'oublie pas de "décoder" ceci en unicode et\nd\'enlever le padding.\n----------\nThe P4C s3rv3r\n\nseed: 135\npseudo-random junk: foo\nmac: 20d2fe6d98f44fa1c6cfe38ad9250432'
print(plaintext)
print(server.query("/padding-attack/validation/echallier/"+str(seedNum), {'plaintext': plaintext}))
