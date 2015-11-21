
from popgen import composition

i = 0
while i < 1:
    c = composition.Composer()
    c.compose()
    a = "output/%d.wav" % i
    print "Trying #%d" % i
    print a
    c.save(a)
    i += 1
