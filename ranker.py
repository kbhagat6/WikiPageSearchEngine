import cPickle as pickle 
import networkx as nx
import matplotlib.pyplot as plt
from numpy import zeros,matrix, random, sum,arange, ones, dot,shape,allclose
from scipy import linalg as LA
from array import array
import math



def rankpages(Dgraph):

	filelist=nx.nodes(Dgraph)
	fnlength=len(filelist)
	S = matrix(zeros((fnlength, fnlength)))

	edict=dict([fn,j] for j, fn in enumerate(filelist))


	for n,nbrsdict in Dgraph.adjacency_iter():
		for nbr,eattr in nbrsdict.items():
			S[edict[n],edict[nbr]]=eattr['weight']

	d=0.85
	E=ones(S.shape)/fnlength
	for i in range(fnlength):
		S[i,:]=S[i,:]/sum(S[i,:])

	G=S*d+E*(1-d)  #Stochastic Matrix
	ploteigenvals(G);
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
		for t in range(10):
			rlist.append(R.item(t))
		if(i>0):
			if(allclose(rlist,tmplist)):
				conviter=i;
				break;
		tmplist=rlist;
	ev=[dot(prob,G**j) for j in range(1,conviter)]
	#print(ev[18][5])`
	return ev

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
	evmat=rankpages(Dgraph)
	plotfig(evmat,flength)
