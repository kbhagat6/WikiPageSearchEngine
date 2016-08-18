#Custom-Built Search Engine Using Page Rank Algorithm


## Installation(Linux, OSX, Windows)
```sh
Create the repo folder and use git clone.
pip install wikipedia
pip install scipy
pip install networkx
```
#Running the code

Ensure internet connection and run the wikiparser.py. 
The wikiparser.py parses and searches wikipedia for all the words in the text file(use case: country). For each search it grabs the content and all the links to other wikipedia pages(which happen to be linking to other pages). It then builds a directed graph(assumption was that pages don't necessarily have to link back to each other) and stores it. 

The rank.py parses the directed graph with a dictionary of all of the nodes and links. It then builds the stochastic matrix(markov chain) by applying the random surfer model constraint, adding a random perturbation matrix to satisfy <a href=https://en.wikipedia.org/wiki/Perron%E2%80%93Frobenius_theorem#Positive_matrices>Perron-Frobenius Theorem</a>, and then finds the iteration of algorithm convergence. The perturbing matrix takes into accnt that page can be accessed by some other means so it allows the math to satisfy the eigenvalue properties specified in the theorem.  In a broader sense, the eigenvalues of the stochastic matrix could be for things like spam detection b/c it's often one of things spammers change based on linkage patterns to deliberately adjust rank.
Lastly, the code then displays a graph of all pages ranks and how it converged after each iteration, then you can search for a word in any of the "trained" wiki pages, then returns a sorted list based on ranking I applied previously.

```python
request = _wiki_request(query_params)
html = request['query']['pages'][pageid]['revisions'][0]['*']
lis = BeautifulSoup(html,"html.parser").find_all('li')
filtered_lis = [li for li in lis if not 'tocsection' in ''.join(li.get('class', []))]
may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]
raise DisambiguationError(getattr(self, 'title', page['title']), may_refer_to)
```
 The 3rd line on the code above, or (line 389 on wikipedia.py) should match your html parser if you receive warnings to explicitly declare your parser.
