import matplotlib.pyplot as plot;
import csv;
waitsAtPoint=[];
waittimePerCustomer=[];
totaltimePerCustomer=[];
averageQueueLengthAtPoint=[];
runStats=[];

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
    plot.xlabel("Uhrzeit");
    plot.ylabel("wartende Kunden");
    plot.xlim(8,16);
    plot.savefig("Wartegraph.svg");
    plot.show();
    plot.clf();
    return;

def exportWaitsAtPoint(filename:str):
    with open(filename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL);
        writer.writerow(['Uhrzeit','wartende Kunden']);
        for datapoint in waitsAtPoint:
            writer.writerow(datapoint);
    return;

def meanWaits():
    sum=0.0;
    for data in waitsAtPoint:
        sum+=data[1];
    return sum/len(waitsAtPoint);

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
    plot.savefig("Wartezeiten.svg");
    plot.show();
    plot.clf();
    return;

def exportWaittimePerCustomer(filename:str):
    with open(filename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL);
        writer.writerow(['Kundennummer','Wartezeit']);
        for datapoint in waittimePerCustomer:
            writer.writerow(datapoint);
    return;

def meanWaittimePerCustomer():
    sum=0.0;
    for time in waittimePerCustomer:
        sum+=time[1];
    return sum/len(waittimePerCustomer);

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
    plot.savefig("Verweilzeiten.svg");
    plot.show();
    plot.clf();
    return;

def exportTotaltimePerCustomer(filename:str):
    with open(filename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL);
        writer.writerow(['Kundennummer','Verweilzeit']);
        for datapoint in totaltimePerCustomer:
            writer.writerow(datapoint);
    return;

def meanTotaltimePerCustomer():
    sum=0.0;
    for time in totaltimePerCustomer:
        sum+=time[1];
    return sum/len(totaltimePerCustomer);

def exportMeans(filename:str):
    with open(filename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL);
        writer.writerow(['mittlere Anzahl wartender Kunden',meanWaits()]);
        writer.writerow(['mittlere Wartezeit',meanWaittimePerCustomer()]);
        writer.writerow(['mittlere Verweildauer',meanTotaltimePerCustomer()]);
        writer.writerow(['mittlere Warteschlangenlänge',meanAverageQueueLength()]);
    return;

def addAverageQueueLengthAtPoint(zeitpunkt:float,durchschnitt:float):
    averageQueueLengthAtPoint.append((zeitpunkt,durchschnitt));
    return;

def meanAverageQueueLength():
    sum=0.0;
    for data in averageQueueLengthAtPoint:
        sum+=data[1];
    return sum/len(averageQueueLengthAtPoint);

def reset():
    averageQueueLengthAtPoint.clear();
    waitsAtPoint.clear();
    waittimePerCustomer.clear();
    totaltimePerCustomer.clear();
    return;

def storeRun(lamda:float,run:int,kunden:int):
    runStats.append((lamda,run,kunden,meanWaittimePerCustomer(),meanAverageQueueLength()));
    return;

def exportRuns(filename:str):
    with open(filename,'w',newline='') as csvfile:
        writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL);
        writer.writerow(['lambda-Wert','runID','Kunden','mittlere Wartezeit','mittlere Warteschlangenlänge']);
        for run in runStats:
            writer.writerow(run);
    return;