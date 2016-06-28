import simpy
import math
from LCG import LCG
#Parameters
K=3
L=5
Tr=0.5 #Minuten
lamda=0.5 #/Minute
def generate(enviroment):
    """Generiert Kunden"""
    while True:
        enviroment.timeout();
def inverseCDFExpo(x):
    return -(math.log(1-x))/lamda;
def noInSystem(resource):
    return len(resource.users)+len(resource.queue);
def customer(enviroment,ressources):
    return;
counters=[];
lcg=LCG();
env=simpy.Environment(8*60);
for i in range(K):
    counters.append(simpy.Resource(env));
noInSystem(counters[0]);