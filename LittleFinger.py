#!/usr/bin/env python
#-*-coding:UTF-8-*-

from scapy.all import *
import os,subprocess,sys,re,json, argparse

#####################################################################################
# Fonction qui gère les arguments du script                                         #
#####################################################################################
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", help="Choose the victim domain. Example: -v google.fr")
    return parser.parse_args()


#####################################################################################
# Fonction qui permet de chercher dans une page donnée tout les email               #
# @param url : l'URL a parcourir                                                    #
# @return phoneNumList : la liste de tout les email trouvé                          #
#####################################################################################
def findEmail(url):
    emailList=[]
    # req=urllib2.Request(sys.argv[1])
    fd=urllib2.urlopen(url)
    while 1:
        data=fd.read(1024)
        email=re.search('[a-z0-9._\-]+\@[a-z.\-]*',data)
        if email:
            emailList.append(email.group(0))
        if not len(data):
            break
    for email in emailList:
        if emailList.count(email)>1:
            emailList.remove(email)
    emailList.sort()
    return emailList

#####################################################################################
# Fonction qui permet de chercher dans une page donnée tout les numéro de téléphone #
# @param url : l'URL a parcourir                                                    #
# @return phoneNumList : la liste de tout les numéro trouvé                         #
#####################################################################################
def findPhoneNumber(url):
    phoneNumList=[]
    # req=urllib2.Request(sys.argv[1])
    fd=urllib2.urlopen(url)
    while 1:
        data=fd.read(1024)
        phoneNum=re.search('(0|\+33)[1-9]([-.\ ]?[0-9]{2}){4}',data)
        if phoneNum:
            phoneNumList.append(phoneNum.group(0))
        if not len(data):
            break
    for phone in phoneNumList:
        if phoneNumList.count(phone)>1:
            phoneNumList.remove(phone)
    phoneNumList.sort()
    return phoneNumList



args=parse_args()
domain=args.domain

dico={}
print "Début de la prise d'empreinte sur",domain
whois=subprocess.check_output(['whois',domain])

#Recherche toute les adresses IP
ip=re.findall(r'(([0-9]{1,3}\.){3}[0-9]{1,3})',whois)

#Recherche tout les nom de domaine
name=re.findall(r"(([a-z0-9]*\.)+([a-z0-9\-])+\.([a-z]){2})",whois)

#Recherche toute les adresses e-mail
email=re.findall(r"(([a-z0-9])*\@([a-z0-9\-])*\.([a-z]){2})",whois)
del ip[0] #supprime la première ip publique soit la notre
for i in range (0,len(ip)):
    ip[i]=ip[i][0]
for i in range (0,len(name)):
    name[i]=name[i][0]
# supprime les sites web du whois
for i in name:
    if(re.search(r"(w{3}\..*)",i)):
        name.remove(i)

for i in range (0,len(email)):
    email[i]=email[i][0]
email.sort()

#####################################################################################
# Fonction qui effectue un transfert de zone                                        #
# @param domain : domain a testé                                                    #
# @return dico : le dictionaire avec toute les IP et leurs nom                      #
#####################################################################################
def zoneTransfert (domain):
    transfert=subprocess.check_output(['host','-l',domain, ip[0]])
    name=re.findall(r"(([a-z0-9]*\.)+([a-z0-9\-])+\.([a-z]){2})",transfert)
    for i in range (0,len(name)):
        name[i]=name[i][0]
    ip=re.findall(r'(([0-9]{1,3}\.){3}[0-9]{1,3})',transfert)
    for i in range (0,len(ip)):
        ip[i]=ip[i][0]
    for i in range (0,len(ip)):
        dico[name[i]]=ip[i]

    dicotmp=dico.copy()
    for key in dico:
        if re.search(r"192\.168\..*",dico[key]):
            del dicotmp[key]
            dico[key]=''
        if re.search(r"172\.16\..*",dico[key]):
            del dicotmp[key]
            dico[key]=''
    dico=dicotmp
    return dico

#Fonction qui regarde si une IP est up
def checkIsUp(listIP):
    ipList=[]
    for ip in listIP:
        resu=os.system("ping -c 1 -W 1 " + listIP[ip]+" >/dev/null")
    	if resu == 0:
            ipList.append(ipTest)
    return ipList
