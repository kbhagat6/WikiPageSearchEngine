import wikipedia
import sys
import networkx as nx
import matplotlib.pyplot as plt
import cPickle as pickle
import random

Dgraph=nx.DiGraph()


		
def parseandbuild(wikilist):
	edges=[]
	nodedict={}
	pagedict={}
	print("parsing wikipedia and building tree........")
	Dgraph.add_nodes_from(wikilist)
	for c in wikilist:
		count=0;
		nodedict[c]=[]
		try:
		
			obj=wikipedia.page(c);
			#clinks=country.links
			#print(c)
		except 	wikipedia.exceptions.DisambiguationError as e:
				errarr=e.options
				cword=[i for i in errarr if ("country" in i) or ("Country" in i)]
				#print(cword)
        
		except  ValueError:
				print("valerror")
				continue
	
	        pagedict[c]=obj.content
		clinks=obj.links
		for j in wikilist:
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
	plt.title("Weighted Directed Graph of wiki-ranked pages")
	nx.draw(Dgraph,pos,node_size=0,alpha=0.3,edge_color='b')
	plt.savefig("Directed_Graph.png")
	with open('Dgraph.pk1','wb') as f:
		pickle.dump(Dgraph,f)

	plt.show()


def main():
	itemlist=[]
	if len(sys.argv) < 2:
		sys.stderr.write("Invalid command line, exactly one argument required")
		return 0;
	filename=sys.argv[1];
	try:
		with open(filename,'r') as f:
			for line in f:
				for nword in line.split(","):
		        		itemlist.append(nword.lstrip());	
	except (IOError,OSError) as e:
		print("file not found")
		return 0

	lenlist=len(itemlist);
	print "number of wikipages that can be ranked: ",lenlist
	print("\n")
	value=input("Ideally, pick a subset of items to be ranked: ")
	while(value>lenlist or value<=0 or value!=value):
		value=input("Enter again: ")

	itemlist=random.sample(itemlist,value)	
	parseandbuild(itemlist)
	plotfig()

if __name__=="__main__":
	main()
