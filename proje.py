import requests
import urllib.parse
from requests.api import request
import time
#Epoch time, date time'a dönüşür -- datetime.fromtimestamp()

urlCustomers="https://northwind.netcore.io/query/customers.json"
rCustomers= requests.get(urlCustomers)
if not rCustomers.status_code==200:
    raise Exception("API Bağlantı Sorunu. Status code:{}. Text: {}".format(
        rCustomers.status_code, rCustomers.text
    ))

#print(rCustomers.text)

jsonCustomers=rCustomers.json()
#print(rCustomers.json())


urlOrders="https://northwind.netcore.io/query/orders.json"
rOrders= requests.get(urlOrders)
if not rOrders.status_code == 200:
    raise Exception("API Bağlantı Sorunu. Status code: {}. Text: {}".format(
        rOrders.status_code, rOrders.text
    )) 
#print(rOrders.text)

jsonOrders=rOrders.json()
#print(rOrders.json())


def metinKontrol(metin):
    if len(metin)>15:
        return f"{str(metin[0:15])}..." 
    else:
        return f"{metin}" + " "*(15-(len(metin)))

def musteriListele():
    print("Müşteri Listesi")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")
    print("|ID     |CompanyName            |ContactName            |Address               |Country               |City |")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+") 
    for i in jsonCustomers['results']:  
        print(f"{i['id']}\t {metinKontrol(i['companyName'])}\t {metinKontrol(i['contactName'])}\t {metinKontrol(i['address'])}\t {metinKontrol(i['country'])}\t{metinKontrol(i['city'])}") 
     
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")


def musteriAra(musteriId):
    for i in jsonCustomers["results"]:
        if i['id']==musteriId:
            print(f"{musteriId} ID'li müşteri bulundu. Detay Listesi ")
            print("==========================") 
            print(f"Id           :{i['id']} ")   
            print(f"Firma Adı    :{i['companyName']} ")   
            print(f"Müşteri Adı  :{i['contactName']} ")   
            print(f"İş Disiplini :{i['contactTitle']} ")   
            print(f"Adres        :{i['address']} ")   
            print(f"Şehir        :{i['city']} ")   
            print(f"Posta Kodu   :{i['postalCode']} ")   
            print(f"Ülke         :{i['country']} ")   
            print(f"Telefon      :{i['phone']} ")   
            print(f"Fax          :{i['fax']} ")   
            break
    else:
        print(f"{musteriId} ID'li müşteri bulunamadı.")



def siparisListele():
    print("Sipariş Listesi")
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+-----------------------+") 
    print("|ID     |CustomerId      |OrderDate                     |ShipAddress            |ShipCity             |ShipCountry |") 
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+-----------------------+") 
    for i in jsonOrders["results"]:  
        epochSaniye= int(i['orderDate'][6:15])
        gunumuzZamani=time.ctime(epochSaniye)
        print(f"{i['id']}\t {i['customerId']}\t\t {gunumuzZamani}\t {metinKontrol(i['shipAddress'])}\t {metinKontrol(i['shipCity'])}\t {metinKontrol(i['shipCountry'])}") 
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+") 

def siparisAra(siparisId):
    for i in jsonOrders["results"]:
        if i['id']==siparisId:
            epochSaniye= int(i['orderDate'][6:15])
            gunumuzZamani=time.ctime(epochSaniye)
            print(f"{siparisId} ID'li sipariş bulundu. Detay Listesi")
            print("==========================")
            print(f"Sipariş Id       :{i['id']} ")   
            print(f"Müşteri Id       :{i['customerId']} ")     
            print(f"Sipariş Tarihi   :{gunumuzZamani} ")   
            print(f"Adres            :{i['shipAddress']} ")   
            print(f"Şehir            :{i['shipCity']} ")    
            print(f"Ülke             :{i['shipCountry']} ")   
            
            nereye = i["shipCity"]
            cevap = input(f"Kargo Rotasını {nereye.upper()} Şehri İçin Görmek İster misiniz? [e/E] :") 
            if cevap.lower()=="e":
                while True:
                    print(f"Varış Noktası {nereye} için Rota Hesaplanacak")
                    nereden=input("Nereden Çıkacak:")
                    print("==========================")
                    url="https://www.mapquestapi.com/directions/v2/route?"+urllib.parse.urlencode({"key":"hVtarhygWABG2kM1BWV7y1VLw7YzHqXV" ,"from":nereden, "to":nereye})
                    jsonData=requests.get(url).json()
                    #print(jsonData)
                    print(f"Kargo rotası {nereden}  den/dan {nereye} e/a/ye/ya ")
                    print(f"Toplam Süre:"+(jsonData["route"]['formattedTime']))
                    print(f"Kilometre:  "+str((jsonData["route"]['distance'])*1.61))
                    print(f"Kullanılan Yakıt (litre) : "+str((jsonData["route"]['fuelUsed'])*3.78))
                    print("==========================")
                    for item in jsonData["route"]["legs"][0]["maneuvers"]:
                        print((item["narrative"])+ "(" +str("{:.2f}".format((item['distance'])*1.61)+"km)"))
                    print("=============================================\n")
                    break
            break
    else:
        print(f"{siparisId} ID'li sipariş bulunamadı.")


  
while True:
    for i in range(5):
        print()
    secim=int(input("""
        Seçiminiz:
        [1] → MÜŞTERİ LİSTELE
        [2] → MÜŞTERİ ARA <MÜŞTERİ ID'E GÖRE>
        [3] → SİPARİŞ LİSTELE
        [4] → SİPARİŞ ARA <SİPARİŞ ID'E GÖRE>
        [5] → ÇIK
        """))
    
    if secim==1:
        musteriListele()
    elif secim==2:
        musteriAra('DRACD')
    elif secim==3:
        siparisListele()
    elif secim==4:
        siparisAra(10258)
    elif secim==5:
        break

    else:
        print("Hatalı Seçim")
    