import sys
class Task: #taszk osztály
    def __init__(self, name: str, prior: int, arrival: int, length: int) -> None:
        self.name = name            #taszk betűjele
        self.prior = prior          #taszk prioritása
        self.length = length        #taszk CPU-löketideje
        self.arrival = arrival      #taszk indítási ideje
        self.remTime = length       #taszk futásának hátralévő ideje (indítási idő kezdetben)
        self.waitTime = 0           #taszk várakozásának ideje
        self.tickTime = 0           #taszk futásának eltelt ideje
    def wait(self) -> None: #taszk várakozása
        self.waitTime+=1
    def tick(self) -> None: #taszk egyszeri kezelése
        self.remTime -= 1
        self.tickTime -= 1

def sortKey(task: Task): #a végén a várakozási idők rendezéséhez (csak extra munkálkodás)
    return task.name

class FIFO: #FIFO osztály az RR ütemezőhöz
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e      
    def push(self, elem: Task) -> None: #FIFO végére szúr egy új taszkot
        self.Storage.append(elem) #fordított sorrend lesz, mert ez egy tömb
        self.empty = False
    def pop(self) -> Task: #FIFO elejéről kiveszi az ott lévő taszkot
        res = self.Storage.pop(0)
        if len(self.Storage) == 0:
            self.empty = True
        return res
    def top(self) -> Task: #visszaadja a FIFO tetején lévő elemet (nem törli)
        return self.Storage[0]
    def wait(self, time: int) -> None: #FIFO-ban lévő taszkok várakozása
        for t in self.Storage:
            if t.arrival <= time:
                t.wait()
    
    
class List: #SRTF ütemezőhöz Lista
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e
    def push(self, elem: Task) -> None:   #beszúrja a megfelelő helyre az új taszkot
        index = 0
        changed = False
        for i in range(len(self.Storage)):
            if self.Storage[i].remTime < elem.remTime:
                index = i
                changed = True
                break
        if changed:
            self.Storage.insert(index, elem)
        else:
            self.Storage.append(elem)
        self.empty = False
    def pop(self) -> Task: #Lista elejéről kiveszi az ott lévő taszkot
        res = self.Storage.pop(len(self.Storage) - 1) 
        if len(self.Storage) == 0:
            self.empty = True
        return res
    def top(self) -> Task: #Lista elején lévő elemet visszaadja (nem törli)
        return self.Storage[len(self.Storage)-1] 
    def wait(self, time: int) -> None: #Listában lévő taszkok várakozása
        for t in self.Storage:
            if t.arrival <= time:
                t.wait()
    

class RR_Scheduler: #RR ütemező az egyik szinthez
    def __init__(self, prior: int, time: int) -> None:
        self.prior = prior
        self.time = time
        self.FIFO = FIFO()
    def addTask(self, task: Task) -> None: #taszk felvétele az RR_Scheduler FIFO-jába
        self.FIFO.push(task)
    def popTask(self) -> Task: #taszk kiválasztása a FIFO elejéről
        return self.FIFO.pop()
    
class SRTF_Scheduler: #SRTF ütemező a másik szinthez
    def __init__(self, prior: int) -> None:
        self.prior = prior
        self.List = List()
    def addTask(self, task: Task) -> None: #taszk felvétele az SRTF_Scheduler (rendezett) listájába
        self.List.push(task)
    def popTask(self) -> Task: #taszk kiválasztása a lista elejéről
        return self.List.pop()
        
class Scheduler: #többszintű ütemező osztály
    def __init__(self) -> None:
        self.RR_Scheduler = RR_Scheduler(1, 2)  #az ütemező 1-es prioritású szintje
        self.SRTF_Scheduler = SRTF_Scheduler(0) #az ütemező 0-s prioritású szintje
        self.finishedTasks = []                 #a már elvégzett taszkok
        self.activeTask = None                  #az éppen végzett taszk
        self.text = ""                          #a taszkok futásának szövege (1. output)
        self.temp = [] #átmeneti mappa a még meg nem érkezett taszkoknak
        
    def addTask(self, task: Task) -> None: #taszk felvétele a megfelelő szintre
        if task.prior == 1:
            self.RR_Scheduler.addTask(task)
        else:
            self.SRTF_Scheduler.addTask(task) 
    def getInput(self) -> None: #az adatok befogadása
        lines = []
        while True:
            try:
                lines.append(input())
            except:
                break
        for line in lines:
            try:
               inp = line.split(',')
               t = Task(inp[0], int(inp[1]), int(inp[2]), int(inp[3]))
               self.temp.append(t)
            except:
                pass
        
    def work(self): #a szimuláció
        time = 0
        while (len(self.temp) != 0) or ((not self.RR_Scheduler.FIFO.empty) or (not self.SRTF_Scheduler.List.empty)) or (self.activeTask is not None): #itt egy iteráció = egy taszk kiválasztása
            #######################################
            # a már megérkezett taszkok felvétele #
            #######################################
            i = 0
            while i < len(self.temp):
                task = self.temp[i]
                if task.arrival <= time:
                    self.addTask(task)
                    self.finishedTasks.append(task)
                    self.temp.pop(i)
                else:
                    i+=1
            
            ###################################
            # choose task -> prior 1, aztán 0 #
            ###################################
            
            if self.activeTask is not None:
                if self.activeTask.prior == 0:
                    if not self.RR_Scheduler.FIFO.empty:
                        self.addTask(self.activeTask)
                        self.activeTask = self.RR_Scheduler.popTask()
                    elif (not self.SRTF_Scheduler.List.empty) and (self.SRTF_Scheduler.List.top().remTime < self.activeTask.remTime):
                        self.addTask(self.activeTask)
                        self.activeTask = self.SRTF_Scheduler.popTask()
            else:
                if not self.RR_Scheduler.FIFO.empty:
                    self.activeTask = self.RR_Scheduler.popTask()
                    self.activeTask.tickTime = self.RR_Scheduler.time
                elif not self.SRTF_Scheduler.List.empty:
                    self.activeTask = self.SRTF_Scheduler.popTask()

            # taszk tickelése
            if self.activeTask is not None:
                self.activeTask.tick()
                if len(self.text) == 0 or (self.text[len(self.text)-1] != self.activeTask.name):
                    self.text += self.activeTask.name

            #minden másik taszk várakozik
            self.SRTF_Scheduler.List.wait(time)
            self.RR_Scheduler.FIFO.wait(time)
            

            #ha lejárt a taszk futási ideje
            if (self.activeTask is not None) and self.activeTask.remTime == 0:
                #self.finishedTasks.append(self.activeTask)
                self.activeTask = None

            #ha lejár az RR szinten lévő taszk időszelete
            if (self.activeTask is not None) and self.activeTask.prior == 1 and self.activeTask.tickTime == 0: #ha lejár az időszelet, mindenképp kerüljön vissza
                self.addTask(self.activeTask)
                self.activeTask = None
                
            time += 1
            
        print(self.text)
        print(",".join(f"{t.name}:{t.waitTime}" for t in self.finishedTasks))


if __name__ == "__main__":
     scheduler = Scheduler()
     scheduler.getInput()
     scheduler.work()
    
    
    
    
    
    
