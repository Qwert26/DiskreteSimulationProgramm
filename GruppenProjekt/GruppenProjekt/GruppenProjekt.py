import simpy;
import math;
from LCG import LCG;
#Parameters
K=3#Anzahl der Kassen bei Start
L=5#Anzahl der wartenden Kunden
Tr=0.5 #Minuten Anzahl der Minuten pro Tier an der Kasse
lamda=0.5 #/Minute Parameter der Exponentialverteilung

def generate(enviroment):
    """Generiert Kunden"""
    kundenNummer=0;
    while True:
        yield enviroment.timeout(lcg.nextTransformed(inverseCDFExponential));
        enviroment.process(customer(enviroment,counters,kundenNummer));
        print("Kunde %i erzeugt um %f"%(kundenNummer,enviroment.now));
        kundenNummer+=1;
    return;

def inverseCDFExponential(x):
    """Inverse CDF der Exponentialverteilung. Liefert Zahlen im interval [0;+infinity)"""
    return -(math.log(1-x))/lamda;

def noInSystem(resource):
    """Aktuelle Anzahl der Nutzer einer Ressourcen"""
    return len(resource.users)+len(resource.queue);

def waitingCustomers():
    """Wie viele Kunden insgesamt im System warten"""
    sum=0;
    for res in counters:
        sum+=len(res.queue);
    return sum;

def customer(enviroment,ressources,kundenNummer):
    """Modelliert einen Kunden in der Tierhandlung."""
    qLengths=[noInSystem(ressources[i]) for i in range(len(ressources))];
    for i in range(len(ressources)):
        if qLengths[i]==0 or qLengths[i]==min(qLengths):
            choice=i;
            break;
    #kuerzeste Warteschlange gewaehlt.
    print("Kunde wählte Kasse %i"%choice);
    res=ressources[choice];
    with res.request() as req:
        yield req;
        tiere=1;
        for i in range(4):
            if lcg.nextBool(0.5):
                tiere+=1;
                #Binominalverteilte Inkrementierung: Zwischen +0 und +4.
        bezahlzeit=tiere*Tr+lcg.nextTransformed(inverseCDFPareto);
        print("Kunde wird %f Minuten für das Bezahlen brauchen"%bezahlzeit);
        yield enviroment.timeout(bezahlzeit);
    #if noInSystem(res)==0 and len(ressources)>1:
        #ressources.remove(res);
    return;

def inverseCDFPareto(x):
    """inverse CDF der Paretoverteilung. Liefert Zahlen im Bereich [xmin;+infinity)."""
    xmin=1.0;
    alpha=2.0;
    return xmin/((1-x)**(1/alpha))

counters=[];
lcg=LCG();
env=simpy.Environment(8*60);#Starte die Simulation um 8 Uhr. Das sind 8*60 Minuten nach Mitternacht.
for i in range(K):
    counters.append(simpy.Resource(env));
env.process(generate(env));
env.run(until=16*60);#Lasse die Simulation bis 16 Uhr laufen. Das ist dann 16*60 Minuten nach Mitternacht.