waitsAtPoint={};
waittimePerCustomer={};
totaltimePerCustomer={};
def addWaitsAtPoint(zeitpunkt:float,wartendeKunden:int):
    waitsAtPoint[zeitpunkt]=wartendeKunden;
    return;

def addWaittimePerCustomer(kundenNummer:int,wartezeit:float):
    waittimePerCustomer[kundenNummer]=wartezeit;
    return;

def addTotaltimePerCustomer(kundenNummer:int,verweilzeit:float):
    totaltimePerCustomer[kundenNummer]=verweilzeit;
    return;
