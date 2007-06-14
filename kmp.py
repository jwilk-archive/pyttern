'''Text algorithms: Pattern matching.'''

def P(text):
	'''Prefix-suffix table for the text.

	>>> P('ananasy')
	[-1, 0, 0, 1, 2, 3, 0, 0]
	'''
	t = -1
	p = [t]
	for i, x in enumerate(text):
		while t >= 0 and x != text[t]:
			t = p[t]
		t += 1
		p.append(t)
	return p

def Ps(text):
	'''Strong prefix-suffix table for the text.

	>>> Ps('ananasy')
	[-1, 0, -1, 0, -1, 3, 0, 0]
	'''
	t = -1
	p = [t]
	text_len = len(text)
	for i, x in enumerate(text):
		while t >= 0 and x != text[t]:
			t = p[t]
		t += 1
		if i + 1 == text_len or text[t] != text[i + 1]:
			p.append(t)
		else:
			p.append(p[t])
	return p

def KMP(needle, haystack, f):
	'''Search for the needle in the haystack.
	Compute the prefix-suffix table with <f>.

	>>> KMP('ana', 'ananasy', P)
	0 0 1 0 1 0 0
	>>> KMP('ana', 'ananasy', Ps)
	0 0 1 0 1 0 0
	'''
	p = f(needle)
	n_len = len(needle)
	i = 0
	for sym in haystack:
		while i >= 0 and needle[i] != sym:
			i = p[i]
		i += 1
		if i == n_len:
			print 1,
			i = p[n_len]
		else:
			print 0,
	print

if __name__ == '__main__':
	import doctest
	doctest.testmod()

# vim:ts=4 sw=4
