import simpy;
import math;
class ManagedRessources(object):
    def __init__(self,env:simpy.Environment,startCount:int):
        self.waitsFor={};
        self.env=env;
        for i in range(startCount):
            self.waitsFor[simpy.Resource(env,1)]=list();
        return;

    def getIn(self):
        """Erzeugt ein neues Event für den Kunden und gibt es zurück."""
        minor=2**31;
        for res in self.waitsFor:
            minor=min(minor,len(self.waitsFor[res]));
        #kleinste Warteschlange gefunden
        for res in self.waitsFor:
            if len(self.waitsFor[res])==0 or len(self.waitsFor[res])<=minor:
                event=simpy.Event(self.env);
                self.waitsFor[res].append(event);
                if res.count==0 and len(self.waitsFor[res])==1:
                    event.succeed();
                return event;
                #Angestellt.
        raise RuntimeError("There had to be a list which has the shortest length!");

    def increaseCounters(self):
        """Erhöht die Anzahl der Kassen um 1 und verteilt die internen Events neu."""
        res=simpy.Resource(self.env,1)
        waitingCustomers=[];
        for prev in self.waitsFor:
            waitingCustomers.extend(self.waitsFor[prev]);
            self.waitsFor[prev].clear();
        self.waitsFor[res]=list();
        for kundennummer in waitingCustomers:
            minor=2**31;
            for res in self.waitsFor:
                minor=min(minor,len(self.waitsFor[res]));
            #kleinste Warteschlange gefunden
            for res in self.waitsFor:
                if len(self.waitsFor[res])==0 or len(self.waitsFor[res])<=minor:
                    self.waitsFor[res].append(kundennummer);
                    if res.count==0 and len(self.waitsFor[res])==1:
                        kundennummer.succeed();
                    break;
        return;

    def nextActionForCounter(self,resource:simpy.Resource):
        """Entscheidet zwischen nächste Bedienung und schließen der Kasse"""
        if len(self.waitsFor[resource])>0:
            self.waitsFor[resource][0].succeed();
        else:
            if len(self.waitsFor)>1:
                self.waitsFor.pop(resource);
                print("Kasse geschlossen");
        return;

    def getCounter(self,customerEvent:simpy.Event):
        """Kunde versucht sich an die Kasse zu stellen, an dessen Warteschlange er gerade steht. Das übergebene Event dient als Identität."""
        for res in self.waitsFor:
            if customerEvent in self.waitsFor[res]:
                self.waitsFor[res].remove(customerEvent);
                return res;
        raise RuntimeError("");

class MyRessource(simpy.Resource):
    @simpy.Resource.capacity.setter
    def capacity(self,value):
        if value==self._capacity:
            #print("No change");
            return;
        else:
            if self._capacity<value:
                self._capacity=value;
                #print("Triggering now available events");
                #capacity was increased.
                while self.put_queue and self.count()<self._capacity:
                    request=self.put_queue(0);
                    self.put_queue.remove(request);
                    self._do_put(request);
            else:
                #capacity might be decreased.
                if self._capacity>len(self.put_queue):
                    #print("Reducing capacity to bigger value")
                    self._capacity=max(len(self.put_queue),value);
                else:
                    #print("No change");
                    return;