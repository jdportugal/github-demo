import re
import requests
import bs4
import random
from copy import deepcopy

lista=[]

def procura(msg,rep):
    teste=[]
    contador=0
    for line in msg.find_all('a'):
        lr=str((line.get('href')))
        regex=re.compile(r"https://pt")
        testar=regex.search(lr)
        if testar!=None:
            teste.append(lr)
            contador+=1
    if contador==0:
        return 1
    i=0
    while i!=contador:
        num=i
        #print(num)
        stri=teste[num]
        if stri in lista:
            return 1
        if rep>10:
            rep=0
            return 1
        #print(teste[num])
        try:
            msg2=requests.get(stri)
            rep+=1
            lista.append(teste[num])
            noStarchSoup2 = bs4.BeautifulSoup(msg2.text,"html.parser")
            #print("----------"+str(rep))
            procura(noStarchSoup2,rep)
        except requests.exceptions.RequestException as e:    # This is the correct syntax
            print ("error")
        i+=1;
    

def main():
    res = requests.get('https://pt.wikipedia.org/wiki/Wikipédia:Página_principal')
    Soup = bs4.BeautifulSoup(res.text,"html.parser")
    procura(Soup,0)
    for i in range(len(lista)):
        print(str(lista[i]))

main()
