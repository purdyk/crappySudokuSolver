__author__ = 'purdyk'

from lxml import html
import urllib2

# http://kjell.haxx.se/sudoku/?action=Create%20a%20field&seed=94193662-v3-17-L5
# http://kjell.haxx.se/sudoku/?action=Create%20a%20field&seed=196733367-v3-17-L5

fh = urllib2.urlopen('http://kjell.haxx.se/sudoku/?action=Create%20a%20field&seed=94193662-v3-17-L5')
raw = fh.read()
fh.close()
tree = html.fromstring(raw)

out = ['0'] * 81

for i in range(2, 83):
    val = tree.xpath("//*[@id=\"id{}\"]".format(i))[0].value

    i2 = i - 2

    square = i2 / 9
    squareoff = i2 % 9

    baserow = (square / 3) * 3
    basecol = (square % 3) * 3

    offrow = (squareoff / 3)
    offcol = (squareoff % 3)

    spot = ((baserow + offrow) * 9) + basecol + offcol

    if len(val) > 0:
        out[spot] = val

print "".join(out)

#000000103000000000000950000000020050057000009000006000006000090400200080003060000
