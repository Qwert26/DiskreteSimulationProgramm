import simpy;
import simpy.resources.base;
import math;
class ManagedRessources(object):
    def __init__(self,env:simpy.Environment,startCount:int):
        self.counters=[];
        self.waitsFor={};
        self.env=env;
        for i in range(startCount):
            self.counters.append(simpy.Resource(env,1));
            self.waitsFor[self.counters[i]]=list();
        return;

    def getIn(self,kundenNummer:int):
        minor=2**31;
        for res in self.waitsFor:
            minor=min(minor,len(self.waitsFor[res]));
        #kleinste Warteschlange gefunden
        for res in self.waitsFor:
            if len(self.waitsFor[res])==0 or len(self.waitsFor[res])<=minor:
                self.waitsFor[res].append(kundenNummer);
                return;
                #Angestellt.
        raise RuntimeError("There had to be a list which has the shortest length!");

    def increaseCounters(self):
        """Erhöht die Anzahl der Kassen um 1"""
        res=simpy.Resource(self.env,1)
        self.counters.append(res);
        waitingCustomers=[];
        for prev in self.waitsFor:
            waitingCustomers.extend(self.waitsFor[prev]);
            self.waitsFor[prev].clear();
        self.waitsFor[res]=list();
        for kundennummer in waitingCustomers:
            self.getIn(kundennummer);
        return;

    def tryCloseCounter(self,resource:simpy.Resource):
        if len(self.waitsFor)>1:
            if len(self.waitsFor[resource])==0:
                self.waitsFor.pop(resource,object());
                print("Kasse geschlossen");
        return;

    def getCounter(self,kundenNummer):
        """Versucht sich an die Kasse zu stellen, an dessen Warteschlange er gerade steht."""
        for res in self.waitsFor:
            if kundenNummer in self.waitsFor[res]:
                if self.waitsFor[res][0]==kundenNummer and len(res.users)==0:
                    self.waitsFor[res].pop(0);
                    return res;
                else :
                    return None;
        return None;
