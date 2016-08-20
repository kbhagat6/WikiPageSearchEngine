import cPickle as pickle 
import networkx as nx
import matplotlib.pyplot as plt
from numpy import zeros,matrix, random, sum,arange, ones, dot,shape,allclose
from scipy import linalg as LA
from array import array
import re
import math



def processmatrix(Dgraph):

	filelist=nx.nodes(Dgraph)
	fnlength=len(filelist)
	S = matrix(zeros((fnlength, fnlength)))

	edict=dict([fn,j] for j, fn in enumerate(filelist))
	

	for n,nbrsdict in Dgraph.adjacency_iter():
		for nbr,eattr in nbrsdict.items():
			S[edict[n],edict[nbr]]=eattr['weight']
	#print(S)
	d=0.85 #damping factor
	E=ones(S.shape)/fnlength
	S=d*S+E*(1-d)   #stochastic matrix
	G=matrix(zeros(S.shape))
	for i in xrange(fnlength):
		if(sum(S[i,:]!=0)):
			G[i,:]=S[i,:]/sum(S[i,:])
        
	ploteigenvals(G); #we can check the eivenvalues of G as it coverges
	prob=random.random(fnlength)
	smprob=sum(prob)
	prob=(prob/smprob)   #random surfer model constraint
	R=prob
	conviter=0
	tmplist=[]
	for i in range(50):	#find iteration of convergence
		R=dot(R,G)
		rlist=[]
		#s=[map(float,line.strip()) for line in R]
		for t in range(R.shape[1]):
			rlist.append(R.item(t))
		if(i>0):
			if(allclose(rlist,tmplist)):
				conviter=i;
				break;
		conviter=i
		tmplist=rlist;
	print(conviter)	
	ev=[dot(prob,G**j) for j in range(1,conviter)]
	#print(ev[18][5])
	#print(ev)
	return (edict,R,ev)


def searchquery(filename,word,edict,R):
	
	with open('pages.pk1', 'rb') as f:
   		pagedict=pickle.load(f)
	worddict={}
	worddict[word]={}
	pr={}
	wlist=word.split()
	for fn in filename:
		ct=len(re.findall(r"(?=("+'|'.join(wlist)+r"))",pagedict[fn]))
		#print(fn)
		if(ct>0):
			worddict[word][fn]=ct
			pr[fn]=R[0,edict[fn]]
	print(worddict)
        print(sorted(pr.keys(),key=pr.__getitem__,reverse=True))	

		
def ploteigenvals(G):
	print(LA.eig(G))

def plotfig(ev,fnlength):
	plt.figure()
	for i in xrange(fnlength):
		plt.plot([j[0,i] for j in ev], label=filelist[i],lw=2)


	plt.draw()	
	yticks=arange(0,0.001,0.35)
	plt.yticks=(yticks)
	plt.title('rank vs. iter step')
	plt.xlabel('iteration step')
	plt.ylabel('rank')
	plt.legend()
	plt.grid(True)
	plt.savefig("rank.png")
	plt.show()


if __name__=="__main__":

	with open('Dgraph.pk1', 'rb') as f:
   		Dgraph=pickle.load(f)
	filelist=nx.nodes(Dgraph)
	flength=len(filelist)
	(edict,R,evmat)=processmatrix(Dgraph)
	plotfig(evmat,flength)

	word=raw_input("Enter a search paramter: ")
	chkregx=re.compile("^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$")
        while not re.search(chkregx,word):
        	word=raw_input("Enter again: ")
	searchquery(filelist,word,edict,R)
