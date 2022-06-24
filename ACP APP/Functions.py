def Trans_to_min(x):
    D=x.day*24*60
    min = x.minute
    H = x.hour *60
    return int(D+min+H)


def Verify_in_interval(M1,M2):
    if M1[0]<=M2[0] and M1[1]>=M2[0]:
        return True
    elif M1[0]<=M2[1] and M1[1]>=M2[1]:
        return True
    else: 
        return False 


def   listAdj(M):
    listAdj=[]
    for i in range(len(M)):
        listAdj.append([])
        for j in [x for x in range(len(M)) if x != i]:
            if Verify_in_interval(M[i],M[j]) or Verify_in_interval(M[j],M[i]) :
                listAdj[i].append(j)
            else:
                pass
    return listAdj

def matriceAdj(Adj):
    Mat=[]
    for i in range( len(Adj)):
        Mat.append([])
        for j in range( len(Adj)):
            Mat[i].append(0)
            for k in range(len(Adj[i])):
                if j==Adj[i][k]:
                    Mat[i][j]=1
    return Mat

# %%
def arret(M):
    ex=[[],[]]
    for i in range (len(M)-1):
        for j in range(i+1,len(M)):
            if M[i][j]==1:
                ex[0].append(i)
                ex[1].append(j)
    return ex


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

def Minimum(C):
    min_Conducteur=0
    for i in C:
        if min_Conducteur<=i:
            min_Conducteur=i
    if len(C)> 0:
        min_Conducteur+=1
    return min_Conducteur