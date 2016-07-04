import matplotlib.pyplot as plot;
def main():
    plot.plot([0,1,4,9]);
    plot.xlabel("x");
    plot.ylabel("y");
    plot.show();
    return;
if __name__ == "__main__":
    main();
"""with ressource.request() as req:
        Analytics.addWaitsAtPoint(enviroment.now,waitingCustomers());
        Analytics.addAverageQueueLengthAtPoint(enviroment.now,waitingCustomers()/ressource.capacity);
        yield req;
        Analytics.addWaittimePerCustomer(kundenNummer,enviroment.now-inSystem);
        Analytics.addAverageQueueLengthAtPoint(enviroment.now,waitingCustomers()/ressource.capacity);
        tiere=1;
        for i in range(4):
            if lcg.nextBool(0.5):
                tiere+=1;
                #Binominalverteilte Inkrementierung: Zwischen +0 und +4.
        bezahlzeit=tiere*Tr+lcg.nextTransformed(inverseCDFPareto);
        print("Kunde %i wird %f Minuten für das Bezahlen brauchen"%(kundenNummer,bezahlzeit));
        yield enviroment.timeout(bezahlzeit);
    Analytics.addTotaltimePerCustomer(kundenNummer,enviroment.now-inSystem);
    ressource.capacity=ressource.capacity-1;"""