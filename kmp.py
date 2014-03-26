# encoding=UTF-8

# Copyright © 2007, 2014 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''text algorithms: pattern matching'''

def P(text):
	'''Build prefix-suffix table for the text.

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
	'''Build strong prefix-suffix table for the text.

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
