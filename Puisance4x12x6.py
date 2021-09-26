# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 08:21:38 2020

@author: victo
"""

import numpy as np
import random as rd
import time

#On définit la profondeure max et initial :
profondeure=-1
profondeureMax=3

CRED = '\33[41m'
CBLUE   = '\33[44m'
CYEL   = '\33[36m'
CEND = '\033[0m'

#renvoie la diagonale gauche et droite exentré de k 
def diag(s,k):
    d1,d2=[],[]
    i,j= (0,k) if(k>0) else (-k,0)
    while(i and j >0):
        i,j=i-1,j-1 
    while(i<len(s) and j<len(s[0])):
        d1.append(s[i,j])
        d2.append(s[i,len(s[0])-j-1])
        i,j=i+1,j+1
    return d1,d2


#Ici pour le puissance 4 on peut définirt Terminale et Utility dans une même fonction :
def TerminalUtility(s,joueurs):
    #On retourner un resultat de type [terminal,score]
    
    #Gagnant sur les lignes
    for i in s:
        for n in range(9):
            if(i[n]==i[1+n]==i[2+n]==i[3+n]!="."):
                return [True,99999] if(i[n]==joueurs[0]) else [True,-99999]
                  
    #Gagnant sur les colonnes :
    for j in range(12):   
        x=s[:,j]
        for n in range(3):
            if(x[n]==x[1+n]==x[2+n]==x[3+n]!="."):
                return [True,99999] if(x[n]==joueurs[0]) else [True,-99999]
    
    
    #Gagnant sur les diagonales :
    
    #Pour chaque diagonale exentrée de k :
    for k in range(-2,9):
        d1,d2=diag(s,k)
        #On regarde si il y a un gagnant sur une de ces deux diagonales :
        for n in range(len(d1)-3): 
            if(d1[n]==d1[1+n]==d1[2+n]==d1[3+n]!='.'):
                return [True,99999] if(d1[n]==joueurs[0]) else [True,-99999]
            
            if(d2[n]==d2[1+n]==d2[2+n]==d2[3+n]!='.'):
                return [True,99999] if(d2[n]==joueurs[0]) else [True,-99999]

            
            

    #Plus de jetons:
    nbP=np.sum(s=='.')
    if(nbP==30):
        return [True,50]
   
    return [False]
            
    


def heuristique(s,joueurs):
    
    #Permet de retourner si il est possible de gagner dans tab 
    #pour le joueur Local et Adversaire et si oui on associe également
    #le nombre de pions déja placé
    def checkLCD(tab,jL,jA):
        resLocal=[True,0]
        resAdversaire=[True,0]
        
        for k in tab:
            if(k==jA):
                resLocal[0]=False
                resAdversaire[1]+=1
                if(resAdversaire[0]==False):
                    break
            elif(k==jL):
                
                resAdversaire[0]=False
                resLocal[1]+=1
                if(resLocal[0]==False):
                    break
            
            
                
        return resLocal,resAdversaire
    
    #Permet de donner un score à une Ligne Colonne ou Diagonale :
    def EvalLCD(LCD,index,joueurs):

        #On commence par restreindre la recherhe aux 3 pions de part et d'autre 
        #du point concerné :
        tab1=LCD[index:] if(len(LCD)-1-index<4) else LCD[index:index+4]
        tab2=tab2=LCD[:index] if(index<4) else LCD[index-3:index]     
        tab = np.concatenate([tab2,tab1])
        
        #On va calculer un score en tant qu'adversaire et joueure Local
        fitnessLocal,fitnessAdversaire=0,0
         
        #Pour chaque "sous tableau" de taille 4 de la LCD :
        for k in range(len(tab)-3):
            #On regarde si il est possible de gagner et les nombre de pions
            check=checkLCD(tab[k:4+k],joueurs[0],joueurs[1])
            
            #Si on peut gagner en tant que joueur Local on augmente le score Local
            #On augmente le score de façon polynomial en fonction du nombre de pions
            if(check[0][0]):
                fitnessLocal+=3**check[0][1]
            #Si on peut gagner en tant que joueur adverse on augmente le score Adverse 
            if(check[1][0]):
                fitnessAdversaire+=3**check[1][1]
            
                
        return fitnessLocal,fitnessAdversaire
    
    def EvalAction(a,joueurs):
            
        #On evalue une action part sont potentiel sur les lignes colonnes et diagos

        #Evaluation de la ligne
        info=EvalLCD(s[a[0]],a[1],joueurs)
        fitness1Local,fitness1Aversaire=info
        
        #Evaluation de la colonne
        info=EvalLCD(s[:,a[1]],a[0],joueurs)
        fitness2Local,fitness2Aversaire=info


        #On s'occupe des diagonales :
        #On récupére les deux diagonales concernées:
        d1=[]
        i,j=a
        while(i>=0 and j >=0 ):
            d1.append(s[i,j])
            i,j=i-1,j-1 
            
        d1.reverse()
        i1=len(d1)-1
        i,j=a[0]+1,a[1]+1
        
        while(i<len(s) and j<len(s[0])):
            d1.append(s[i,j])
            i,j=i+1,j+1
              
        d2=[]
        i,j=a
        while(i<len(s) and j>=0):
            d2.append(s[i,j])
            i,j=i+1,j-1
            
        d2.reverse()
        i2=len(d2)-1
        i,j=a[0]-1,a[1]+1
        
        while(0<=i and j<len(s[0])):
            d2.append(s[i,j])
            i,j=i-1,j+1
            
        #Evaluation des deux diagonales :
       
        fitness31Local,fitness31Adversaire=0,0     
        if(len(d1)>3):
            info=EvalLCD(d1,i1,joueurs)
            fitness31Local,fitness31Adversaire=info
        
        fitness32Local,fitness32Adversaire=0,0
        if(len(d2)>3):
            info=EvalLCD(d2,i2,joueurs)
            fitness32Local,fitness32Adversaire=info
                
        fitness3Local=fitness31Local+fitness32Local 
        fitness3Aversaire=fitness31Adversaire+fitness32Adversaire
        
        fitnessLocal=fitness1Local+fitness2Local+fitness3Local
        fitnessAdversaire=fitness1Aversaire+fitness2Aversaire+fitness3Aversaire
        
        return fitnessLocal,fitnessAdversaire

    #Ici on favorise l'attaque plutot que la défense
    score=0
    coefAttaque=1.7
    coefDefense=1
    
    #Pour chaque action on va ajouter sons score Local et soustraire son score adversaire
    for a in action(s):
        fitnessS=EvalAction(a,joueurs)
        score+=coefAttaque*fitnessS[0]  
        score-=coefDefense*fitnessS[1]

    return round(score,1)
        


def action(s):
    #On parcours les colonnes à partir du bas pour gagner du temps au debut
    actions=[]
    for k in range(12):
        tab=s[:,k]
        if tab[-1]=='.':
            actions.append([len(tab)-1,k])
        elif(tab[0]=='.'):
            i=-1
            while(i-1>=-6 and tab[i-1]!='.' ):
                i-=1
            actions.append([len(tab)+i-1,k])
    return actions 
       


def Result(s,a,j):
    #On fait une copie du tableau et on place le bon pion au bonne endroit
    res=np.copy(s)
    res[a[0],a[1]]=j
    return res




def Max_Value(s,A,B,joueurs):
    #A chaque descente en profondeure on met à jour la variable
    global profondeure
    profondeure+=1
    

    #On vérifie si on est dans un etat terminal
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return [term[1],profondeure]
    #On vérifie si on a dépacé la profondeure max
    elif(profondeure>profondeureMax):
        return [heuristique(s,joueurs),profondeure]
    #Sinon on appel récursivement avec la coupure Beta
    else:
        #Pour chaque action on retournera sa valeure ainsi que la profondeure 
        #d'ou viens cette valeure
        v=[-9999999,profondeure]
        for a in action(s):
            mnV=Min_Value(Result(s,a,joueurs[0]),A,B,joueurs)
            v=[max(v[0],mnV[0]),mnV[1]]
            profondeure-=1  
            if v[0]>=B:return v
            A=max(A,v[0])
                    
        return v


def Min_Value(s,A,B,joueurs):
    #Même raisonnement avec qu'avec Max Value
    global profondeure
    profondeure+=1
    
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return [term[1],profondeure]
    elif(profondeure>profondeureMax):
        return [heuristique(s,joueurs),profondeure]
    else:
        v=[9999999,profondeure]
        for a in action(s):
            mxV=Max_Value(Result(s,a,joueurs[1]),A,B,joueurs)
            v=[min(v[0],mxV[0]),mxV[1]]
            profondeure-=1
            if v[0]<=A:return v
            B=min(B,v[0])
        return v
            


def MinMax(s,joueurs):
    global profondeure
    act=[None]
    value=-9999999
    
    #On va prendre l'action avec la valeure maximale
    #Cependant si on a plusieurs actions avec la même valeure on prend celle
    #qui se situe le moins profondemment dans l'arbre
    for a in action(s):
        
        profondeure=0
        coup=Min_Value(Result(s,a,joueurs[0]),-9999999,9999999,joueurs)
        res=coup[0]
        profondeureCoup=coup[1]
        if(res>value):
            value=res
            act=[[a,profondeureCoup]]
        elif(res==value):
            act.append([a,profondeureCoup])
    return min(act,key=lambda x:x[1])[0]




def affichage(plateau):
    #On met en forme la grille :
    print("\n| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |11 |12 | ")
    print("\n------------------------------------------------- ")
    for i in plateau:
        print('| ',end='')
        for j in i:
            if(j=='X'):
                print(CRED+j+CEND+' | ',end='') 
            elif(j=='.'):
                print(j+' | ',end='')
            else:
                print(CBLUE+j+CEND+' | ',end='')
        print('\n')
    print("\n")

def SaisieSecur(s):
    #On gére la saisie afin de ne pas avoir d'erreures :
    c=input("colonne n° : ")

    while ((c.isdigit()==True and 0<=int(c)-1<12 and '.' in s[:,int(c)-1] )==False ):
        c=input("colonne n° : ")
        
    i,j=0,int(c)-1
    for x in range(6):
        if(s[x,j]!="."):
            i=x-1
            break  
        if(x==5 and s[x,j]=="."):            
            i=x
            break 
            
    return [i,j]

def SaisieAleatoire(s):
    #On tire des coups aléatoirement pour voir comment l'IA réagit :
    c=rd.randint(0,11)

    i,j=0,c
    for x in range(6):
        if(s[x,j]!="."):
            i=x-1
            break  
        if(x==5 and s[x,j]=="."):            
            i=x
            break 
            
    return [i,j]


def MorpionGame():
    #Mise en forme du jeu
    listeT=[]
    
    CombatIa=input("Quel mode voulez-vous :\n 1:Classique\n 2:Combat d'IA \n\n →")
    pionJ=input("Le programme joue avec des X \nAvec quoi voulez vous jouer ? ")
    j=input("Qui commence ?\n 1: La Machine\n 2: Vous \n\n →  ")
    j=1 if(j!="1" and j!="2") else int(j)
    
    Grid=np.array([     
                    ['.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.'],
                    ['.','.','.','.','.','.','.','.','.','.','.','.']])
    affichage(Grid)
        
    
    term=TerminalUtility(Grid,["X",pionJ])
    while term[0]==False:
        
        if(j==2):
            if(CombatIa!="2"):
                print("C'est votre tour, rentrez le numéro d'une colonne : ")
                t1=time.time()
                saisie=SaisieSecur(Grid)
                dt=time.time()-t1
                print("Vous avez réflechis "+CYEL+str(round(dt,1))+CEND+" sc et jouez en "+CYEL+str(saisie[1]+1)+CEND)
            else:
                print("Votre IA alliée reflechie..")
                t1=time.time()
                saisie=MinMax(Grid,[pionJ,"X"])
                dt=time.time()-t1
                print("Votre IA a réflechie "+CYEL+str(round(dt,1))+CEND+" sc et joue en "+CYEL+str(saisie[1]+1)+CEND)
            Grid[saisie[0],saisie[1]]=pionJ
            affichage(Grid)
            j=1
         
        elif(j==1):
            print("Le programme reflechi... :")
            t1=time.time()
            action=MinMax(Grid,["X",pionJ])
            dt=time.time()-t1
            listeT.append(dt)
            print("L'IA adverse a réflechie "+CYEL+str(round(dt,1))+CEND+" sc et joue en "+CYEL+str(action[1]+1)+CEND)
            Grid[action[0],action[1]]="X"
            affichage(Grid) 
            j=2
        
        term=TerminalUtility(Grid,["X",pionJ])
    print("La partie est finie !")
    Tmoy=round(np.array(listeT).mean(),4)
    print("L'IA a prie en moyenne ",Tmoy,"sc à répondre")


    
    
    res=TerminalUtility(Grid,["X",pionJ])[1]
    if(res==99999):
        print("Vous avez perdu..")
    elif(res==-99999):
        print("Vous avez gagné !")
    else:
        print("Egalité!")
            
        
if __name__=="__main__":
    MorpionGame()