# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:26:22 2020

@author: victo
"""

import numpy as np
import random as rd

def TerminalUtility(s,joueurs):
    
    #Gagnant sur les lignes
    for i in s:
        for n in range(14):
            if(i[n]==i[1+n]==i[2+n]==i[3+n]==i[4+n]==i[5+n]!="."):
                return [True,99999] if(i[n]==joueurs[0]) else [True,-99999]
                  
    #Gagnant sur les colonnes :
    for j in range(19):   
        x=s[:,j]
        for n in range(14):
            if(x[n]==x[1+n]==x[2+n]==x[3+n]==x[4+n]==x[5+n]!="."):
                return [True,99999] if(x[n]==joueurs[0]) else [True,-99999]
    
    #Gagnant sur les diagonales: On récupéres tout les diagonale de longueure supérieure ou égale à 6
    # et on les parcours en regardant si il y a un gagnant

    #Mattrice retournée de s afin d'avoir les diagonal inverse
    s2=np.array([np.flip(s[i]) for i in range(len(s))])
    
    for k in range(-len(s)+1,len(s[0,:])):
        d1=s.diagonal(k)
        d2=np.flip(s2.diagonal(k)) 
        if(len(d1)>=6):
            for n in range(len(d1)-5): 
                if(d1[n]==d1[1+n]==d1[2+n]==d1[3+n]==d1[4+n]==d1[5+n]!='.'):
                    return [True,99999] if(d1[n]==joueurs[0]) else [True,-99999]
            for n in range(len(d2)-5): 
                if(d2[n]==d2[1+n]==d2[2+n]==d2[3+n]==d2[4+n]==d2[5+n]!='.'):
                    return [True,99999] if(d2[n]==joueurs[0]) else [True,-99999]
        

    #Le tableau est remplit
    if("." not in s):
        return [True,300]
   
    return [False]
            
    



def heuristique(s,joueurs):
    #Rq : j=[moi,adversaire]
    
    #Permet de retourner le nombre de possibilité de gagner et pour chaque possibilité
    #combien de pions reste t'il à placer
    def LCDGagnant(LCD,index,joueurs):
        
        #On commence par restreindre la recherhe aux 5 pions de part et d'autre du point concerné
            
        tab1=LCD[index:] if(len(LCD)-1-index<6) else LCD[index:index+6]
        tab2=tab2=LCD[:index] if(index<6) else LCD[index-5:index]  
                 
        tab = np.concatenate([tab2,tab1])
            
        #Ensuite on compte le nb de possibilité de gagner 
        nbPossibilite,nbPionsTot=0,0
               
        for k in range(len(tab)-6):
            if(joueurs[1] not in tab[k:6+k]):
                nbPossibilite+=1
                nbPionsTot+=np.sum(tab[k:6+k]==joueurs[0])

        return [nbPossibilite,nbPionsTot]
    
    
    def EvalAction(a,joueurs):
            
        #On évalue une action par le fait qu'à l'instant t0 elle peut potentiellement nous faire plus ou moins gagner
        fitness=0
        
        #On regarde si il est possible de gagner sur cette ligne
        fitness1=0
        info=LCDGagnant(s[a[0]],a[1],joueurs)
        if(info[0]>0):
            fitness1+=info[0]**2+info[1]**3
    
            
        #On regarde si il est possible de gagner sur cette colonne
        fitness2=0
        info=LCDGagnant(s[:,a[1]],a[0],joueurs)
        if(info[0]>0):
            fitness2+=info[0]**2+info[1]**3
    
    
        #On s'occupe pour finir des diagonales :
        
        #On récupére les deux diagonales concernées:
        fitness3=0
        
        d1=[]
        i,j=a
        while(0<=i and 0<=j):
            i,j=i-1,j-1 
        x1=i,j
        while(i<len(s) and j<len(s[0,:])):
            d1.append(s[i,j])
            i,j=i+1,j+1
                
        d2=[]
        i,j=a
        while(i<len(s) and 0<=j):
            i,j=i+1,j-1
        x2=i,j
        while(0<=i and j<len(s[0,:])):
            d2.append(s[i,j])
            i,j=i-1,j+1
            
        #Pour chaque diagonales on regarde si elle est gagnante:
        
        fitness31=0
        info=LCDGagnant(d1,a[0]-x1[0],joueurs)
        if(info[0]>0):
            fitness31+=info[0]**2+info[1]**3
    
            
        fitness32=0
        info=LCDGagnant(d2,x2[0]-a[0],joueurs)
        if(info[0]>0): 
            fitness32+=info[0]**2+info[1]**3
                
        fitness3=fitness31+fitness32 
            
        
        fitness=fitness1+fitness2+fitness3

        return fitness
            
    score=0
    coefAttaque=10
    coefDefense=1
    
    for a in action(s):
        #On evalue le score de la grille pour le programme (domicile):
        score+=coefAttaque*EvalAction(a,joueurs)
        #On evalue le score de la grille pour l'adversaire
        score-=coefDefense*EvalAction(a,[joueurs[1],joueurs[0]])
        
    #Ici on favorise l'attaque plutot que la défense
    
    return score
        

def action(s):
    #On parcours du bas pour gagner du temps au debut
    actions=[]
    for k in range(19):
        tab=s[:,k]
        if tab[-1]=='.':
            actions.append([len(tab)-1,k])
        elif(tab[0]=='.'):
            i=-1
            while(i-1>=-19 and tab[i-1]!='.' ):
                i-=1
            actions.append([len(tab)+i-1,k])
    return actions 
       


def Result(s,a,j):
    res=np.copy(s)
    res[a[0],a[1]]=j
    return res


#On regarde 1 coup dans le futur

def Max_Value(s,A,B,joueurs):
    global profondeure
    profondeure+=1
    
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return term[1]
    elif(profondeure>1):
        return heuristique(s,joueurs)
    else:
        #Beta
        v=-9999999999
        for a in action(s):
            v=max(v,Min_Value(Result(s,a,joueurs[0]),A,B,joueurs))
            profondeure-=1  
            if v>=B:
                return v
            A=max(A,v)
                    
        return v

def Min_Value(s,A,B,joueurs):
    global profondeure
    profondeure+=1
    
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return term[1]

    elif(profondeure>1):
        return heuristique(s,joueurs)
    else:
        #Alpha
        v=9999999999
        for a in action(s):
            v=min(v,Max_Value(Result(s,a,joueurs[1]),A,B,joueurs))
            profondeure-=1
            if v<=A:
                return v
            B=min(B,v)
        return v
            


def MinMax(s,joueurs):
    act=[None]
    value=-9999999999
    for a in action(s):
        
        global profondeure
        profondeure=0
        res=Min_Value(Result(s,a,joueurs[0]),-9999999999,9999999999,joueurs)
        if(res>value):
            value=res
            act=[a]
        elif(res==value):
            act.append(a)
    #Si on a le choix entre plusieurs coups de même score on choisi aléatoirement
    #afin d'avoir un jeux plus varier ce qui peut destabiliser l'adversaire
    i=rd.randint(0,len(act)-1)
    return act[i]


def SaisieSecur(s):
    c=input("colonne n° : ")

    while ((c.isdigit()==True and 0<=int(c)<19 and '.' in s[:,int(c)] )==False ):
        c=input("colonne n° : ")
        
    i,j=0,int(c)
    for x in range(19):
        if(s[x,j]!="."):
            i=x-1
            break  
        if(x==18 and s[x,j]=="."):            
            i=x
            break 
            
    return [i,j]

def affichage(plateau):
    print("\n")
    for i in plateau:
        print('|',end='')
        for j in i:
            print(j+' | ',end='')
        print('\n')
    print("\n")

def SaisieAleatoire(s):
    c=rd.randint(0,18)

   
    i,j=0,c
    for x in range(19):
        if(s[x,j]!="."):
            i=x-1
            break  
        if(x==18 and s[x,j]=="."):            
            i=x
            break 
            
    return [i,j]

def MorpionGame():
    #Mise en forme du jeu
    Grid=np.array([     
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.']])

    affichage(Grid)
    j=2
    
    term=TerminalUtility(Grid,["O","X"])
    while term[0]==False:
        
        if(j==2):
            print("C'est votre tour, rentrez le numéro d'une colonne : ")
            saisie=MinMax(Grid,["O","X"])
            Grid[saisie[0],saisie[1]]="O"
            affichage(Grid)
            j=1
         
        elif(j==1):
            print("Au tour du programme :")
            action=MinMax(Grid,["X","O"])
            Grid[action[0],action[1]]="X"
            affichage(Grid) 
            j=2
        
        term=TerminalUtility(Grid,["X","O"])
    print("La partie est finie !")
    


    
    
    res=TerminalUtility(Grid,["X","O"])[1]
    if(res==99999):
        print("Vous avez perdu..")
    elif(res==-99999):
        print("Vous avez gagné !")
    else:
        print("Egalité!")
            
        
if __name__=="__main__":
    MorpionGame()