
from popgen import composition

i = 0
while i < 100:
    try:
        c = composition.Composition()
        c.compose()
        a = "output/%d.wav" % i
        print "Trying #%d"%i
        print a
        c.play(a)
        i += 1
    except:
        print "Error on #%d"%i
