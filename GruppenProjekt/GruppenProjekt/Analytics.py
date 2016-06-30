import matplotlib.pyplot as plot
waitsAtPoint=[];
waittimePerCustomer=[];
totaltimePerCustomer=[];

def addWaitsAtPoint(zeitpunkt:float,wartendeKunden:int):
    waitsAtPoint.append((zeitpunkt,wartendeKunden));
    return;

def createWaitAtPointGraph():
    zeitpunkte=[];
    wartende=[];
    for datapoint in waitsAtPoint:
        zeitpunkte.append(datapoint[0]/60);
        wartende.append(datapoint[1]);
    plot.plot(zeitpunkte,wartende);
    plot.xlabel("Stunden");
    plot.ylabel("wartende Kunden");
    plot.xlim(8,16);
    plot.savefig("Wartegraph.png");
    plot.show();
    plot.clf();
    return;

def addWaittimePerCustomer(kundenNummer:int,wartezeit:float):
    waittimePerCustomer.append((kundenNummer,wartezeit));
    return;

def createWaittimePerCustomerGraph():
    waittimePerCustomer.sort(key=lambda id:id[0]);
    data=[];
    for time in waittimePerCustomer:
        data.append(time[1]);
    plot.plot(data);
    plot.xlabel("Kundennummer");
    plot.ylabel("Wartezeit [min]");
    plot.savefig("Wartezeiten.png");
    plot.show();
    plot.clf();
    return;

def addTotaltimePerCustomer(kundenNummer:int,verweilzeit:float):
    totaltimePerCustomer.append((kundenNummer,verweilzeit));
    return;

def createTotaltimePerCustomerGraph():
    totaltimePerCustomer.sort(key=lambda id:id[0]);
    data=[];
    for time in totaltimePerCustomer:
        data.append(time[1]);
    plot.plot(data);
    plot.xlabel("Kundennummer");
    plot.ylabel("Verweilzeit [min]");
    plot.savefig("Verweilzeiten.png");
    plot.show();
    plot.clf();
    return;