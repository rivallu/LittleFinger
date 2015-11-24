#!/usr/bin/env python
#-*-coding:UTF-8-*-

import os,subprocess,sys,re,json

domain=sys.argv[1]
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
print dico
