import simpy;
import math;
from LCG import LCG;
from ManagedRessources import ManagedRessources as MR;
import Analytics;
#Parameters
K=3#Anzahl der Kassen bei Start
L=5#Anzahl der wartenden Kunden
Tr=0.5 #Minuten, Anzahl der Minuten pro Tier an der Kasse
lamda=0.5 #/Minute, Parameter der Exponentialverteilung
period=0.01;#Periodendauer in Minuten mit der gewartet wird zwischen Bedingungsanfragen: Je niedriger desto genauer aber auch mehr Overhead für die Simulation.

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

def waitingCustomers():
    """Wie viele Kunden insgesamt im System warten"""
    sum=0;
    for res in counters.waitsFor:
        sum+=len(counters.waitsFor[res]);
    return sum;

def customer(enviroment,ressource,kundenNummer):
    """Modelliert einen Kunden in der Tierhandlung."""
    Analytics.addWaitsAtPoint(enviroment.now,waitingCustomers());
    inSystem=enviroment.now;
    ressource.getIn(kundenNummer);
    while True:
        counter=ressource.getCounter(kundenNummer);
        if counter is None:
            yield env.timeout(period);#Warte eine Periode.
        else:
            if isinstance(counter,simpy.Resource):
                with counter.request() as req:
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
                Analytics.addTotaltimePerCustomer(kundenNummer,enviroment.now-inSystem);
                ressource.tryCloseCounter(counter);
                return;
    return;

def inverseCDFPareto(x):
    """inverse CDF der Paretoverteilung. Liefert Zahlen im Bereich [xmin;+infinity)."""
    xmin=1.0;
    alpha=2.0;
    return xmin/((1-x)**(1/alpha))

def counterOpener(enviroment):
    while True:
        while L<=waitingCustomers():
            yield env.timeout(period);#Warte eine Periode.
        yield env.timeout(lcg.nextTransformed(inverseCounterTime));
        print("Kasse geöffnet.");
        counters.increaseCounters();
    return;

def inverseCounterTime(x):
    return math.sqrt(math.sqrt(24*x+1)-1);

lcg=LCG();
env=simpy.Environment(8*60);#Starte die Simulation um 8 Uhr. Das sind 8*60 Minuten nach Mitternacht.
counters=MR(env,K);
env.process(generate(env));
env.process(counterOpener(env));
env.run(until=16*60);#Lasse die Simulation bis 16 Uhr laufen. Das ist dann 16*60 Minuten nach Mitternacht.
#Erzeuge, zeige und speichere Graphen.
Analytics.createWaitAtPointGraph();
Analytics.createWaittimePerCustomerGraph();
Analytics.createTotaltimePerCustomerGraph();
#Zeige Mittelwerte an.
print("mittlere Anzahl wartender Kunden: %f"%Analytics.meanWaits());
print("mittlere Wartezeit: %f"%Analytics.meanWaittimePerCustomer());
print("mittlere Verweilzeit: %f"%Analytics.meanTotaltimePerCustomer());
#Exportiere Daten in das CSV-Format.
Analytics.exportWaitsAtPoint("wartende_Kunden.csv");
Analytics.exportTotaltimePerCustomer("Verweilzeiten.csv");
Analytics.exportWaittimePerCustomer("Wartezeiten.csv");
Analytics.exportMeans("Mittelwerte.csv");