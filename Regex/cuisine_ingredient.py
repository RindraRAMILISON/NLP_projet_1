
# coding: utf-8

# In[80]:


def get_ingredient(phrase):
    import re
    global quantité
    global ingredient
    
    res =re.search(r'(((?P<qa1>((\d+(.\d+)?) )((c. à .*?)|(cuillère.? à \w.*?)|(tasse.?)|(..)|(.)|)) ((d[’\'])|de )?(?P<ia1>\w.*))|((?P<q0>\d.*? ((\w.*?\))?)) ((d[’\'])|de )?(?P<i0>\w.*)(, ))|((?P<q1>\d.*? ((\w.*?\))?)) ((d[’\'])|de )?(?P<i1>\w.*))|(((?P<q2>\d.*?) )((d[’\'])|de )(?P<i2>\w.*))|(((?P<q3>\d+(.\d+)?) )(?P<i3>\w.*), )|(((?P<q5>\d+(.\d+)?) )(?P<i5>\w.*)))',phrase)
    
    if res:
        if (res.group('qa1')):
            quantité=res.group('qa1')
            ingrédient=res.group('ia1')
            
        if (res.group('q0')):
            quantité=res.group('q0')
            ingrédient=res.group('i0')
            
        if (res.group('q1')):
            quantité=res.group('q1')
            ingrédient=res.group('i1')
            
        if (res.group('q2')):
            quantité=res.group('q2')
            ingrédient=res.group('i2')
            print(quantité)
            print(ingrédient)
        if (res.group('q3')):
            quantité=res.group('q3')
            ingrédient=res.group('i3')
           
        if (res.group('q5')):
            quantité=res.group('q5')
            ingrédient=res.group('i5')
        
       
    else:
        quantité="NA"
        ingrédient="NA"
     
    return [quantité,ingrédient]
    
import re

mon_fichier = open("ingredients.txt", "r",encoding="utf-8")
test=open("ingredients_solutions.txt", "r",encoding="utf-8")

fichier1=mon_fichier.readlines()
fichier2=test.readlines()
i=0
evaluation=0
evaluation1=0
for line in fichier1:
    [Q,I]=get_ingredient(line)
    solution=re.search(r'(QUANTITE:(?P<solq>.*)   INGREDIENT:(?P<soling>.*))', fichier2[i])
    
    if solution :
        solq=solution.group('solq')
        soling=solution.group('soling')

    if (solq==Q and ((soling+' '==I) or (soling==I))) :
        evaluation+=1
    
    else:
        print(line)
        evaluation1+=1
        print('not found '+str(evaluation1))
        print('QUANTITÉ = '+Q+' = '+ solq)
        print('INGREDIENT = '+ I+' = '+soling)
    i+=1
evaluation_regex=evaluation

print(evaluation1)

print(str(evaluation_regex)+'/'+str(i))


