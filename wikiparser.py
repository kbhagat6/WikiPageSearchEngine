import wikipedia
import sys
import networkx as nx
import matplotlib.pyplot as plt
import cPickle as pickle
import random

Dgraph=nx.DiGraph()


		
def parseandbuild(countrylist):
	edges=[]
	nodedict={}
	pagedict={}
	print("parsing wikipedia and building tree........")
	Dgraph.add_nodes_from(countrylist)
	for c in countrylist:
		count=0;
		nodedict[c]=[]
		try:
		
			country=wikipedia.page(c);
			#clinks=country.links
			#print(c)
		except 	wikipedia.exceptions.DisambiguationError as e:
				errarr=e.options
				cword=[i for i in errarr if ("country" in i) or ("Country" in i)]
				#print(cword)
        
		except  ValueError:
				print("valerror")
				continue
	
	        pagedict[c]=country.content
		clinks=country.links
		for j in countrylist:
			if(j==c):
				continue
			cnt=clinks.count(j)
			if(cnt>0):
				nodedict[c].append(j)
				edges.append([c,j,{'weight':cnt}])
				count=count+1							
	
		Dgraph.add_edges_from(edges)
	with open('pages.pk1','wb') as f:
		pickle.dump(pagedict,f)
		
def plotfig():		
	print("Rendering tree")

	plt.figure(figsize=(10,10))
	pos=nx.spring_layout(Dgraph)
	plt.title("Weighted Directed Graph of wiki-ranked countries")
	nx.draw(Dgraph,pos,node_size=0,alpha=0.3,edge_color='r')
	plt.savefig("Directed_Graph.png")
	with open('Dgraph.pk1','wb') as f:
		pickle.dump(Dgraph,f)

	plt.show()


def main():
	itemlist=[]
	try:
		with open("countrylist.txt",'r') as f:
			for line in f:
				for nword in line.split(","):
		        		itemlist.append(nword.lstrip());	
	except OSError:
		print("file not found")

	lenlist=len(itemlist);
	print "number of wikipages that can be ranked: ",lenlist
	print("\n")
	value=input("Ideally, pick a subset of items to be ranked: ")
	while(value>lenlist or value<=0 or value!=value):
		value=input("Enter again: ")

	countrylist=random.sample(itemlist,value)	
	parseandbuild(countrylist)
	plotfig()

if __name__=="__main__":
	main()
