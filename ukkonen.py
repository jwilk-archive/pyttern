'''Text algorithms: Suffix trees -- the Ukkonen algorithm.'''

INF = 1.0e3000

class SuffixNode(object):
	
	def __init__(self, i_from, i_to, text):
		self.children = {}
		self.suffix_link = None
		self.i_from = i_from
		self.i_to = i_to
		self.text = text

	@property
	def edge(self):
		return self.i_from, max(self.i_from, self.i_to - 1)

	@property
	def label(self):
		if self.i_to == INF:
			text = self.text[self.i_from:]
		else:
			text = self.text[self.i_from : self.i_to]
		return repr(text)
	
	def add(self, child):
		self[self.text[child.i_from]] = child

	def __getitem__(self, id):
		return self.children[id]

	def __setitem__(self, id, child):
		self.children[id] = child

	def __str__(self, indent = 0):
		return '%s%s\n%s' % (indent * '  ', self.label, ''.join(s.__str__(indent + 1) for s in self.children.itervalues()))

def Ukkonen(text):

	'''Suffix tree for the text.
	
	>>> print Ukkonen('ananas')
	''
	  'a'
	    's'
	    'na'
	      's'
	      'nas'
	  's'
	  'na'
	    's'
	    'nas'
	<BLANKLINE>
	'''

	def update(node, i, j):
		old_node = None
		while True:
			end_point, new_node = test_and_split(node, i, j - 1, text[j])
			if end_point:
				break;
			new_node.add(SuffixNode(j, INF, text))
			if old_node is not None:
				old_node.suffix_link = new_node
			old_node = new_node
			node, i = canonize(node.suffix_link, i, j - 1)
		if old_node is not None:
			old_node.suffix_link = node
		return node, i

	def test_and_split(node, i, j, ch):
		if i <= j:
			node1 = node[text[i]]
			i1, j1 = node1.edge
			i_split = i1 + j - i + 1
			if ch == text[i_split]:
				return True, node
			else:
				new_node = SuffixNode(i1, i_split, text)
				node.add(new_node)
				node1.i_from = i_split
				new_node.add(node1)
				return False, new_node
		else:
			return (ch in node.children), node

	def canonize(node, i, j):
		if i > j:
			return node, i
		node1 = node[text[i]]
		i1, j1 = node1.edge
		while j1 - i1 <= j - i:
			i += j1 - i1 + 1
			node = node1
			if i <= j:
				node1 = node[text[i]]
				i1, j1 = node1.edge
		return node, i

	text_len = len(text)
	bot = SuffixNode(None, None, text)
	root = SuffixNode(0, 0, text)
	for char in text:
		bot[char] = root
	root.suffix_link = bot
	node = root
	i = 0
	for j in xrange(text_len):
		node, i = update(node, i, j)
		node, i = canonize(node, i, j)
	return root

if __name__ == '__main__':
	import doctest
	doctest.testmod()

# vim:ts=4 sw=4
