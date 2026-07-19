from itertools import combinations

def p_any(lst, vrb = False):

    if vrb:
        print("Recibido:", lst)

    sm = sum(lst)

    if vrb:
        for i in range(0, len(lst)):
            print(lst[i], " + ", sep="", end="")
        print("")

    sk = 1
    for x in range(len(lst), 1, -1):
        tuplet = list(combinations(lst, x))
        sk *= -1
        for y in tuplet:
            mlt = 1
            if vrb:
                print("\t+", sk, end="")
            for z in range(0, len(y)):
                mlt *= y[z]
                if vrb:
                    print(" * ", y[z], sep="", end="")
            sm += sk * mlt
            if vrb:
                print("")

    return sm

drupal = [.9757, .9754, .9746, .9658, .9286, .9271, .9237, .6823, .4359, .1694, 0.0678, 0.0612, 0.0557, 0.0397, 0.0363, 0.0275, 0.019, 0.0142]
wordpress = [.0033, .0025, .0016, .0016, .0016, .0014, .0012, .0009, .0008, .0005, .0004]
wagtail = [.0011, .0009]
print("\n", p_any(wordpress, True))
