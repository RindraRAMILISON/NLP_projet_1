
# coding: utf-8

# In[139]:


from collections import defaultdict, Counter
from nltk import tokenize

def Compte_Gram(lien,n):
    
    mon_fichier = open(lien, "r", encoding="utf-8")
    contenu=mon_fichier.readlines()
    token=[]
    N_1gram=[]
    Ngram=[]
    compte=defaultdict(int)
    
    compte_unigramme = defaultdict(int) 
    compte_mot=0    
    # Tokenisation du texte
    for ligne in contenu:
        token.append(tokenize.word_tokenize(ligne))
    
    #calcul du nombre de mots et de vocabulaires dans le texte 
    for ligne in token:
        longeur_ligne=len(ligne)
        compte_mot+=longeur_ligne
        i=0
        for a in ligne:
            compte[a]+=1
    vocabulaire=len(compte)
    
    #calcul des comptes N_gram
    CNgram= counts_N_gram(token,n)
    CN_1gram= counts_N_gram(token,(n-1))
    return [CNgram,CN_1gram,compte_mot,vocabulaire,n]
  
#fonction pour calucler les probabilité de N gram en prenant comme paramètre le compte  Ngram et N-1 gram
def probabilite_Ngram(count,delta):
    [CountNgram,countN_1gram,compte_mot,vocabulaire,n]=count
    probgram=defaultdict(int)
    
    for mot in CountNgram:
        n=len(mot)
        if n==1:
            denom=compte_mot
        else:
            denom=countN_1gram[mot[0:n-1]]
        if delta==0:
            probgram[mot] = (CountNgram[mot])/(denom)
        else:
            probgram[mot] = (CountNgram[mot]+delta)/(denom+(delta*vocabulaire))
    return probgram   


# Fonction pour calculer le logprob d'une séquence de mot
def Logprob(phrase,count,delta):
    import math
    CN_phrase=[]
    [CountNgram,countN_1gram,compte_mot,vocabulaire,n]=count
    token=tokenize.word_tokenize(phrase)
    longueur=len(token)
    i=0
    for mot in token:
        while n+i<=longueur:
            CN_phrase.append(tuple(token[i:i+n]))
            i+=1
    probgram=0
   
    for mot in CN_phrase:
        if n==1:
            denom=compte_mot
        else:
            denom=countN_1gram[tuple(mot[0:n-1])]
        if delta==0:
            probgram= probgram+math.log10((CountNgram[mot])/(denom))
        else:
            probgram = probgram+math.log10((CountNgram[mot]+delta)/(denom+(delta*vocabulaire)))
    return probgram   

#Focntion pour évaluer la perplexité d'une séquence de mot
def perplexité (phrase,count,delta):
    token=tokenize.word_tokenize(phrase)
    longueur=len(token)
    prob=Logprob(phrase,count,delta)
    return ((10)**(prob))**(-1/longueur)

#Fontion pour compter les Ngrams
def counts_N_gram(token,n):
    Ngram={}
    CNgram=defaultdict(int)
    for ligne in token:
        longeur_ligne=len(ligne)
        i=0
        while n+i<=longeur_ligne:
            CNgram[tuple(ligne[i:i+n])]+=1
            i+=1
    return CNgram    

#def complete_proverbe(phrase,N_modèle,delta,)

def complète_proverbe(proverbe,choix,count,delta):
    resultat=defaultdict(float)
    import operator 
    for i in choix:
        proverbe=proverbe.replace("***",i)
        res=Logprob(proverbe,count,delta)
        resultat[proverbe]=res
        proverbe=proverbe.replace(i,"***")
        print(i+ '= ' + str(res))
   
    print(max(resultat.items(), key=operator.itemgetter(1))[0])
    prov=max(resultat.items(), key=operator.itemgetter(1))[0]
    return prov
    
        


# <H1>a) Modèles de langue</H1>
#  probabilités des unigramme=
# <H5>pour N=1</H5> 

# In[2]:


countunigram=Compte_Gram("proverbes.txt",1)
probabilite_Ngram(countunigram,0)


# probabilités des bigrammes=
# <H5>pour N=2 </H5>

# In[3]:


countbigram=Compte_Gram("proverbes.txt",2)
probabilite_Ngram(countbigram,0)


# probabilités des trigrammes=
# <H5>pour N=3 </H5>

# In[4]:


counttrigram=Compte_Gram("proverbes.txt",3)
probabilite_Ngram(counttrigram,0)


# <H1>b) Lissage Laplace</H1>
#  probabilités des unigrammes avec lissage=
# <H5>pour N=1 et delta=1</H5>

# In[5]:


probabilite_Ngram(countunigram,1)


# probabilités des bigrammes avec lissage=
# <H5>pour N=2 et delta=1</H5>

# In[6]:


probabilite_Ngram(countbigram,1)


# probabilités des trigrammes avec lissage=
# <H5>pour N=3 et delta=1</H5>

# In[7]:


probabilite_Ngram(counttrigram,1)


# <H1>d) Estimation</H1>
# <H5>Fonctions pour	estimer	le	logarithme	de	la	probabilité	(logprob) d'une séquence de mots:</H5>
# Pour illustrer notre exemple, prenons le cas d'une phrase dans le texte en utilisant le modèle bigramme avec un delta=2
# 

# In[8]:


Logprob("acquiers bonne renommée, et dors grasse matinée",countbigram,2)


# <H5>fonctions pour	estimer la	perplexité	d’une	séquence	de	mots	à	l’aide	d’un	modèle:</H5>
# Pour illustrer notre exemple, prenons le même cas ci-dessous pour les trois modèles
# 

# In[159]:


print(perplexité ("acquiers bonne renommée, et dors grasse matinée",countunigram,1))
print(perplexité ("acquiers bonne renommée, et dors grasse matinée",countunigram,0.01))


# In[161]:


print(perplexité ("acquiers bonne renommée, et dors grasse matinée",countbigram,1))
print(perplexité ("acquiers bonne renommée, et dors grasse matinée",countbigram,0.01))


# In[158]:


print(perplexité ("acquiers bonne renommée, et dors grasse matinée",counttrigram,1))
print(perplexité ("acquiers bonne renommée, et dors grasse matinée",counttrigram,0.01))


# <H5>Deuxième exemple:</h5>
# il n’y a point de rose de cent jours

# In[152]:


Delta_1=perplexité ("il n’y a point de rose de cent jours",countunigram,1)
Delta_=perplexité ("il n’y a point de rose de cent jours",countunigram,0.5)
print(Delta_1)
print(Delta_)


# In[153]:


Delta_1=perplexité ("il n’y a point de rose de cent jours",countbigram,1)
Delta_=perplexité ("il n’y a point de rose de cent jours",countbigram,0.5)
print(Delta_1)
print(Delta_)


# In[154]:


Delta_1=perplexité ("il n’y a point de rose de cent jours",counttrigram,1)
Delta_=perplexité ("il n’y a point de rose de cent jours",counttrigram,0.5)
print(Delta_1)
print(Delta_)


# <H5>Troisième exemple:</h5>
# après la pluie, le beau temps

# In[162]:


Delta_1=perplexité ("après la pluie, le beau temps",countunigram,1)
Delta_=perplexité ("après la pluie, le beau temps",countunigram,0.5)
print(Delta_1)
print(Delta_)


# In[163]:


Delta_1=perplexité ("après la pluie, le beau temps",countbigram,1)
Delta_=perplexité ("après la pluie, le beau temps",countbigram,0.5)
print(Delta_1)
print(Delta_)


# In[164]:


Delta_1=perplexité ("après la pluie, le beau temps",counttrigram,1)
Delta_=perplexité ("après la pluie, le beau temps",counttrigram,0.5)
print(Delta_1)
print(Delta_)


# <H1>e) Compléter	les	proverbes</H1><br>
# 

# <h5>Variation de delta sur Modèle unigram</h5>

# In[140]:


mon_fichier = open("test2.txt", "r", encoding="utf-8")
contenu=mon_fichier.readlines()
choixtable=[]
delta=[0.01,0.1,0.5,0.9]
#proverbe=["a beau mentir qui *** de loin","a beau *** qui vient de loin","l’occasion fait le ***","aide-toi, le ciel t’***","année de gelée, *** de blé","après la pluie, le *** temps","aux échecs, les *** sont les plus près des rois","ce que *** veut, dieu le veut", "bien mal acquis ne *** jamais","bon ouvrier ne querelle pas ses ***","ce n’est pas tous les jours ***","pour le fou, c’est tous les jours ***","dire et faire, *** deux","mieux vaut *** que jamais","d’un sac *** ne peut tirer deux moutures","à qui dieu aide, *** ne peut nuire","il n’y a *** de rose de cent jours","il faut le *** pour le croire","on ne *** pas le poisson qui est encore dans la mer","la langue d’un *** vaut mieux que celle d’un menteur"]
a=0
for line in contenu:
    x=line.split('"')
    proverbe=str(x[1])
    print(proverbe)
    choixtable.append([x[3],x[5],x[7],x[9]])
    choix=(choixtable[a])
    print(choix)
    a+=1
    for i in delta:
        print('pour delta = '+ str(i))
        complète_proverbe(proverbe,choix ,counttrigram,i)
        print('\n') 
    


# <h5>Variation de delta sur Modèle bigram</h5>

# In[141]:


mon_fichier = open("test2.txt", "r", encoding="utf-8")
contenu=mon_fichier.readlines()
choixtable=[]
delta=[0.01,0.1,0.5,0.9]
#proverbe=["a beau mentir qui *** de loin","a beau *** qui vient de loin","l’occasion fait le ***","aide-toi, le ciel t’***","année de gelée, *** de blé","après la pluie, le *** temps","aux échecs, les *** sont les plus près des rois","ce que *** veut, dieu le veut", "bien mal acquis ne *** jamais","bon ouvrier ne querelle pas ses ***","ce n’est pas tous les jours ***","pour le fou, c’est tous les jours ***","dire et faire, *** deux","mieux vaut *** que jamais","d’un sac *** ne peut tirer deux moutures","à qui dieu aide, *** ne peut nuire","il n’y a *** de rose de cent jours","il faut le *** pour le croire","on ne *** pas le poisson qui est encore dans la mer","la langue d’un *** vaut mieux que celle d’un menteur"]
a=0
for line in contenu:
    x=line.split('"')
    proverbe=str(x[1])
    print(proverbe)
    choixtable.append([x[3],x[5],x[7],x[9]])
    choix=(choixtable[a])
    print(choix)
    a+=1
    for i in delta:
        print('pour delta = '+ str(i))
        complète_proverbe(proverbe,choix ,countbigram,i)
        print('\n') 


# <h5>Variation de delta sur Modèle trigram</h5>

# In[142]:


mon_fichier = open("test2.txt", "r", encoding="utf-8")
contenu=mon_fichier.readlines()
choixtable=[]
delta=[0.01,0.1,0.5,0.9]
#proverbe=["a beau mentir qui *** de loin","a beau *** qui vient de loin","l’occasion fait le ***","aide-toi, le ciel t’***","année de gelée, *** de blé","après la pluie, le *** temps","aux échecs, les *** sont les plus près des rois","ce que *** veut, dieu le veut", "bien mal acquis ne *** jamais","bon ouvrier ne querelle pas ses ***","ce n’est pas tous les jours ***","pour le fou, c’est tous les jours ***","dire et faire, *** deux","mieux vaut *** que jamais","d’un sac *** ne peut tirer deux moutures","à qui dieu aide, *** ne peut nuire","il n’y a *** de rose de cent jours","il faut le *** pour le croire","on ne *** pas le poisson qui est encore dans la mer","la langue d’un *** vaut mieux que celle d’un menteur"]
a=0
for line in contenu:
    x=line.split('"')
    proverbe=str(x[1])
    print(proverbe)
    choixtable.append([x[3],x[5],x[7],x[9]])
    choix=(choixtable[a])
    print(choix)
    a+=1
    for i in delta:
        print('pour delta = '+ str(i))
        complète_proverbe(proverbe,choix ,counttrigram,i)
        print('\n') 

