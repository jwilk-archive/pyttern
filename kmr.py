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

'''text algorithms: suffix tables and suffix trees'''

def KMR(text):
    '''Build suffix table for the text.
    Time complexity: O(n log n), where n = |text|.

    >>> text = 'ananasy'
    >>> for n in KMR(text):
    ...     print n, text[n:]
    ...
    0 ananasy
    2 anasy
    4 asy
    1 nanasy
    3 nasy
    5 sy
    6 y
    '''
    text_len = len(text)
    if text_len <= 1:
        return [0] * text_len
    tail = [None] * text_len
    y = list(text) + tail
    delta = 1
    while delta < text_len:
        y = [(y[i], y[i + delta]) for i in xrange(text_len)]
        ys = sorted(y)
        yd = {}
        a = None
        n = 0
        for i in xrange(text_len):
            if ys[i] != a:
                a = ys[i]
                yd[a] = n
                n += 1
        y = [yd[n] for n in y] + tail
        delta *= 2
    suf = tail
    for i, j in enumerate(y[:text_len]):
        suf[j] = i
    return suf

def LCP(text, suf=None):
    '''Computer LCP for the text, given the suffix table.
    Time complexity: O(n) (+ suffix table computation), where n = |text|.

    >>> text = 'ananasy'
    >>> suf = KMR(text)
    >>> for i, j, d in zip(suf, suf[1:], LCP(text, suf)):
    ...     print text[i:], text[j:], d
    ...
    ananasy anasy 3
    anasy asy 1
    asy nanasy 0
    nanasy nasy 2
    nasy sy 0
    sy y 0
    '''
    if suf is None:
        suf = KMR(text)
    text_len = len(text)
    if text_len < 2:
        return []
    rank = [None] * text_len
    result = [None] * text_len
    for i, j in enumerate(suf):
        rank[j] = i
    j = 0
    for i in xrange(text_len):
        if rank[i] == 0:
            j = 0
        else:
            i1 = suf[rank[i] - 1]
            while i + j < text_len and i1 + j < text_len and text[i + j] == text[i1 + j]:
                j += 1
        result[rank[i]] = j
        j -= j > 0
    return result[1:]

def KS(text):
    '''Build suffix table for the text.
    Time complexity: O(n), where n = |text|.

    >>> text = 'ananasy'
    >>> for n in KS(text):
    ...     print n, text[n:]
    ...
    0 ananasy
    2 anasy
    4 asy
    1 nanasy
    3 nasy
    5 sy
    6 y
    '''

    def encode(text):
        alphabet = set()
        for i in xrange(1, text_len, 3):
            alphabet.add(tuple(text[i : i + 3]))
            alphabet.add(tuple(text[i + 1 : i + 4]))
        alphabet = sorted(alphabet)
        encoding = dict((value, code) for code, value in enumerate(alphabet))
        etext = []
        for i in xrange(1, text_len, 3):
            etext += encoding[tuple(text[i : i + 3])],
        etext += -1,
        for i in xrange(2, text_len, 3):
            etext += encoding[tuple(text[i : i + 3])],
        return etext

    def decoding(i):
        mid = (text_len + 1) // 3
        if i < mid:
            return i * 3 + 1
        elif i == mid:
            return text_len
        else:
            return (i - mid - 1) * 3 + 2

    def decode(suffix_table):

        def quick_cmp(i, j):
            while True:
                t_i, v_i = rsuf[i]
                t_j, v_j = rsuf[j]
                if t_i == t_j:
                    return cmp(v_i, v_j)
                if i >= text_len:
                    return -1
                if j >= text_len:
                    return +1
                result = cmp(text[i], text[j])
                if result != 0:
                    return result
                i += 1
                j += 1

        def merge(list1, list2):
            list = list1 + list2
            list.sort(cmp=quick_cmp)
            return list

        suf23 = [decoding(i) for i in suffix_table]
        suf1 = [i for _, _, i in sorted((text[i - 1], pos, i - 1) for pos, i in enumerate(suf23) if i % 3 == 1)]
        rsuf = {}
        for pos, i in enumerate(suf23):
            rsuf[i] = 23, pos
        for pos, i in enumerate(suf1):
            rsuf[i] = 1, pos
        suf = merge(suf1, suf23)
        if suf[0] == text_len:
            del suf[0]
        return suf

    text_len = len(text)
    if text_len <= 3:
        result = [i for _, i in sorted((text[i:], i) for i in xrange(text_len))]
        return result
    return decode(KS(encode(text)))

class SuffixNode(object):

    '''node of a suffix tree'''

    def __init__(self, parent, i_from, i_to, text=None):
        self.i_from = i_from
        self.i_to = i_to
        if parent is not None:
            self.depth = parent.depth + i_to - i_from
            self.text = parent.text
            parent.add(self)
        else:
            self.depth = 0
            self.text = text
        self.children = {}

    def add(self, child):
        key = self.text[child.i_from]
        self.children[key] = child

    def to_suffix_table(self, result=None):
        ret = False
        if result == None:
            result = []
            ret = True
        if len(self.children) == 0:
            result += len(self.text) - self.depth,
        else:
            for label in sorted(self.children.iterkeys()):
                self.children[label].to_suffix_table(result)
        if ret:
            return result

    @property
    def label(self):
        return repr(self.text[self.i_from : self.i_to])

    def __str__(self, indent=0):
        return '%s%s\n%s' % (indent * '  ', self.label, ''.join(s.__str__(indent + 1) for s in self.children.itervalues()))

def suffix_tree(text, suf=None, lcp=None):
    '''Build suffix tree for the text, given the suffix table and the LCP table.

    >>> print suffix_tree('ananas')
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
    text_len = len(text)
    if text_len == 0:
        return None
    if suf is None:
        suf = KMR(text)
    if lcp is None:
        lcp = LCP(text, suf)
    root = SuffixNode(None, 0, 0, text)
    child = SuffixNode(root, suf[0], text_len)
    stack = [root, child]
    for i, lcp in zip(suf[1:], lcp):
        current = None
        while stack[-1].depth > lcp:
            current = stack.pop()
        parent = stack[-1]
        if parent.depth == lcp:
            leaf = SuffixNode(parent, i + lcp, text_len)
            stack += leaf,
        else:
            i_from = current.i_from
            i_to = current.i_to
            i_split = i_from + lcp
            if i_split == i_to:
                leaf = SuffixNode(current, i + lcp, text_len)
            else:
                current.i_to = i_split
                current.depth -= i_to - i_split
                children = current.children
                current.children = {}
                extent = SuffixNode(current, i_split, i_to)
                extent.children = children
                leaf = SuffixNode(current, i + lcp, text_len)
            stack += current, leaf,
    return root

if __name__ == '__main__':
    import doctest
    doctest.testmod()

# vim:ts=4 sw=4 et
