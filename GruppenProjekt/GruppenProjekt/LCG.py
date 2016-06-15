import math
class LCG(object):
    """Implementierung des LCGs"""
    def __init__(self,mult=1103515245,add=12345,mod=2**31,seed=62200291):
        """Initialisiert den LCG mit den gegebenen Multiplikator, Addierer, Modulo und Seed-Wert. Alle haben default-Werte."""
        self.mult=mult;
        self.add=add;
        self.mod=mod;
        self.seed=seed;
        self.nextNextGaussian=0.0;
        self.hasNextNextGaussian=False;
    def nextSeed(self):
        """Erzeugt den nächsten Seed und gibt ihn zurück."""
        self.seed=(self.mult*self.seed+self.add)%self.mod;
        return self.seed;
    def nextFloat(self):
        """Erzeugt den nächsten float-Wert im Bereich [0;1) und gibt ihn zurück. Benötigt Python 3 fürs korrekte Arbeiten!"""
        return self.nextSeed()/self.mod;
    def nextTransformed(self,inverseCDF):
        """Erzeugt intern den nächsten float-Wert und übergibt diesen der inversen CDF."""
        return inverseCDF(self.nextFloat());
    def nextGaussian(self):
        """Erzeugt standardnormal-verteilte Zufallszahlen nach der Marsaglia Polar Methode. Selber Algorithmus wie auch in java.util.Random.nextGaussian()."""
        if (self.hasNextNextGaussian):
            self.hasNextNextGaussian=False;
            return self.nextNextGaussian;
        else:
            while True:
                u=self.nextFloat()*2-1;
                v=self.nextFloat()*2-1;
                #u und v sind gleichverteilt in [-1;1)
                s=u*u+v*v;
                if(s<1):
                    #s ist im Einheitskreis
                    self.hasNextNextGaussian=True;
                    factor=math.sqrt(-2*math.log(s)/s);
                    self.nextNextGaussian=u*factor;
                    return v*factor;
                else:
                    #s ist nicht im Einheitskreis: Erneuter Versuch.
                    continue;
    def nextBool(self,chance=0.5):
        """Erzeugt den nächsten Warheitswert der mit der gegebenen chance den Wert 'True' hat."""
        return chance>self.nextFloat();