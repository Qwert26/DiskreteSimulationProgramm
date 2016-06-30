import simpy;
import math;
from LCG import LCG;
import Analytics;
#Parameters
K=3#Anzahl der Kassen bei Start
L=5#Anzahl der wartenden Kunden
Tr=0.5 #Minuten, Anzahl der Minuten pro Tier an der Kasse
lamda=0.5 #/Minute, Parameter der Exponentialverteilung

def generate(enviroment):
    """Generiert Kunden"""
    kundenNummer=0;
    while True:
        yield enviroment.timeout(lcg.nextTransformed(inverseCDFExponential));
        enviroment.process(customer(enviroment,counters,kundenNummer));
        print("Kunde %i erzeugt um %i:%i:%i"%(kundenNummer,enviroment.now/60,enviroment.now%60,(enviroment.now%1)*60)); #Druckt die genaue Uhrzeit aus, wann ein neuer Kunde die Tierhandlung betritt.
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
    return len(counters.queue);

def customer(enviroment,ressource,kundenNummer):
    """Modelliert einen Kunden in der Tierhandlung."""
    with ressource.request() as req:
        Analytics.addWaitsAtPoint(enviroment.now,waitingCustomers());
        inSystem=enviroment.now;
        yield req;
        Analytics.addWaittimePerCustomer(kundenNummer,enviroment.now-inSystem);
        tiere=1;
        for i in range(4):
            if lcg.nextBool(0.5):
                tiere+=1;
                #Binominalverteilte Inkrementierung: Zwischen +0 und +4.
        bezahlzeit=tiere*Tr+lcg.nextTransformed(inverseCDFPareto);
        print("Kunde %i wird %f Minuten für das Bezahlen brauchen"%(kundenNummer,bezahlzeit));
        yield enviroment.timeout(bezahlzeit);
    if waitingCustomers()<ressource.capacity:
        print("Kasse geschlossen");
        ressource.capacity-=1;
    Analytics.addTotaltimePerCustomer(kundenNummer,enviroment.now-inSystem);
    return;

def inverseCDFPareto(x):
    """inverse CDF der Paretoverteilung. Liefert Zahlen im Bereich [xmin;+infinity)."""
    xmin=1.0;
    alpha=2.0;
    return xmin/((1-x)**(1/alpha))

def counterOpener(enviroment):
    while True:
        while L<=waitingCustomers():
            yield;
        yield env.timeout(lcg.nextTransformed(inverseCounterTime));
        print("Kasse geöffnet.");
        counters.capacity+=1;
    return;

def inverseCounterTime(x):
    return math.sqrt(math.sqrt(24*x+1)-1);

lcg=LCG();
env=simpy.Environment(8*60);#Starte die Simulation um 8 Uhr. Das sind 8*60 Minuten nach Mitternacht.
counters=simpy.Resource(env,K);
env.process(generate(env));
env.process(counterOpener(env));
env.run(until=16*60);#Lasse die Simulation bis 16 Uhr laufen. Das ist dann 16*60 Minuten nach Mitternacht.
Analytics.createWaitAtPointGraph();
Analytics.createWaittimePerCustomerGraph();
Analytics.createTotaltimePerCustomerGraph();