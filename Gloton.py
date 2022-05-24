# %%
n=8
Adj=dict()
Adj=[[1,2,3,6],[0,4,5],[0,6],[0,6],[1,5,7],[1,4,7],[0,2,3,7],[4,5,6]]
def Gloton(Adj):
    n=len(Adj)
    NC=dict()
    C=[0 for k in range(n)]
    for i in range(n):
        NC[i]=[]
    def  rajouter(k,NC):
        if ((k in NC)==True):
            return NC
        else:
            NC.append(k)
            return NC
    i=0
    while i<=n-1:
        exist=True
        k=0
        while (exist==True):
            exist=k in NC[i]
            if (exist==True):
                k+=1
        C[i]=k    
        for j in range(len(Adj[i])):
            voisin=Adj[i][j]
            NC[voisin]=rajouter(k,NC[voisin])
        i+=1
    return C


# %%
# C=Gloton(Adj)
# print(C)
# def freq(C):
#     fc=[]
#     i=0

#     while (i in C):
#         k=0
#         for j in C:
#             if j==i:
#                 k+=1
#         fc.append(k)
#         i+=1
#     return fc
# def nequitable(fc):
#     for i in fc:
#         if not i+1>=max(fc):
#             return True
#     return False
# def maxid(C,fc):
#     M=[]
#     maxid=[]
#     for i in range(len(fc)):
#         if fc[i]==max(fc):
#             M=i
#             break
#     for i in range(len(C)):
#         if C[i]==M:
#             maxid.append(i)
#     return maxid
# def minid(C,fc):
#     M=[]
#     minid=[]
#     for i in range(len(fc)):
#         if fc[i]==min(fc):
#             M=i
#             break
#     for i in range(len(C)):
#         if C[i]==M:
#             minid.append(i)
#     return minid


# fc=freq(C)
# while(nequitable(fc)):
#     maxlist=maxid(C,fc)
#     minlist=minid(C,fc)
#     for i in maxlist:
#         for j in minlist:
#             if not ( i in Adj[j] and j in Adj[i]):
#                 C[i]=C[j]
#                 break;
#     if fc==freq(C):
#         C[maxlist[0]]=max(C)+1
#     fc=freq(C)
#     break
# print(C)
            





# %%
Adj
C=Gloton(Adj)
def fjk(Adj,C):
listco = []

def co_adj(Adj,C):

    global listco
    for i in range(len(Adj)):
        list=[]
        for j in range (len(Adj[i])):
            x=Adj[i][j]
            list.append(C[x])
        listco.append(list)
    return(listco)
print( "le vecteur des couleurs ajacentes est",co_adj(Adj,C))
couleur=[]
def Couleur(C):
    global couleur
    couleur=[]
    for i in range(len(set(C))):
        couleur.append(i)
    return (couleur)
print("les couleurs utilisées sont",Couleur(C))

# %%
freq=[]
cmax=-1
cmin=-1
def Frequance ():
    global couleur
    global C
    global freq
    global cmax
    global cmin
    freq=[]
    for i in range(len(couleur)):
        x=0
        for j in range(len(C)):
            if C[j]==couleur[i]:
                x+=1
        freq.append(x)
    cmax=freq.index(max(freq))
    cmin=freq.index(min(freq))
    return (freq)
Frequance ()


print("l'ocurance initiale de chaque couleur est",freq)

# %%
nequitable=True
def Equitabilite(freq):
    global nequitable
    c = int(max(freq)) - int(min(freq))
    print(c)
    if c > 1:
        nequitable = False
    else:
        nequitable=True
    return (nequitable)
Equitabilite(freq)
print(nequitable)
if nequitable==False:
    print("Equitable")
else:
    print("n'est pas  equitable")

# %%
vecclr=[]
def sommets_couleur(C,couleur):
    global vecclr
    for i in range(len(couleur)):
        vec=[]

        for j in range(len(C)):
            if couleur[i]==C[j]:

                vec.append(j)
        vecclr.append(vec)
    return (vecclr)

# %%
sommets_couleur(C, couleur)
test=False
while(nequitable==False and test==False):
    x=cmax
    for i in range(len(vecclr[x])):
        if cmin not in listco[(vecclr[x][i])]:
            y=int(vecclr[x][i])
            C[y]=cmin
            test=True
            Couleur(C)
            co_adj(Adj, C)
            Frequance()
            print(freq)
            Equitabilite(freq)
            sommets_couleur(C, couleur)

            break
        else:
            test=False
    if test==False:

        z=int(vecclr[x][1])
        C[z] =len(set(C))
        Couleur(C)
        print(couleur)
        co_adj(Adj, C)
        Frequance()
        Equitabilite(freq)
        sommets_couleur(C, couleur)

# %%
print("le vecteur de coloration obtenue avec l'algorithme de jdk est",C,"le nombrede couleurs utilisees est",len(set(C)),"elles sont les suivantes",set(C))


