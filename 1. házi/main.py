class Task: #taszk osztály
    def __init__(self, name: str, prior: int, arrival: int, length: int) -> None:
        self.name = name            #taszk betűjele
        self.prior = prior          #taszk prioritása
        self.arrival = arrival      #taszk indítási ideje
        self.length = length        #taszk CPU-löketideje
        self.remTime = length       #taszk futásának hátralévő ideje
        self.wait = 0
        self.tickTime = 0           #taszk futásának eltelt ideje
    def wait(self) -> None:
        self.wait+=1
    def tick(self) -> None:
        self.length -= 1
    
    
    #test?
    def __str__(self) -> str:
        return f"{self.name},{self.prior},{self.length},{self.remTime}"

class FIFO: #FIFO osztály az RR ütemezőhöz
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e
        
    def push(self, elem: Task) -> None: #FIFO végére szúr egy új taszkot
        self.Storage.append(elem) #fordított sorrend lesz, mert ez egy tömb
        self.empty = False

    def pop(self) -> Task: #FIFO elejéről kiveszi az ott lévő taszkot
        res = self.Storage.pop(0) if len(self.Storage) != 0 else None
        if len(self.Storage) == 0:
            self.empty = True
        return res
    
class List: #SRTF ütemezőhöz Lista
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e

    def insert(self, elem: Task) -> None:   #beszúrja a megfelelő helyre az új taszkot
        index = 0
        for i in range(len(self.Storage)):
            if self.Storage[i].remTime < elem.remTime:
                index = i
                break
        self.Storage.insert(index, elem)
        self.empty = False
            
    def pop(self) -> Task: #Lista elejéről kiveszi az ott lévő taszkot
        res = self.Storage.pop(len(self.Storage) - 1) if len(self.Storage) != 0 else None
        if len(self.Storage) == 0:
            self.empty = True
        return res

class RR_Scheduler: #RR ütemező az egyik szinthez
    def __init__(self, prior: int, time: int) -> None:
        self.prior = prior
        self.time = time
        self.FIFO = FIFO()
        
    def addTask(self, task: Task) -> None: #taszk felvétele az RR_Scheduler FIFO-jába
        self.FIFO.push(task)
    def popTask(self) -> Task: #taszk kiválasztása a FIFO elejéről
        return self.FIFO.pop()
    def tick(self): #TODO: ha ...
        pass
    # def getTask() -> Task: #visszaad egy taszkot a FIFO ele
    #     pass
    

class SRTF_Scheduler: #SRTF ütemező a másik szinthez
    def __init__(self, prior: int) -> None:
        self.prior = prior
        self.List = List()
    def addTask(self, task: Task) -> None: #taszk felvétele az SRTF_Scheduler (rendezett) listájába
        self.List.insert(task)
    def popTask(self) -> Task: #taszk kiválasztása a lista elejéről
        return self.List.pop()
    def tick(self): #TODO: ha ...
        pass

class Scheduler: #többszintű ütemező osztály
    def __init__(self) -> None:
        self.RR_Scheduler = RR_Scheduler(1, 2)
        self.SRTF_Scheduler = SRTF_Scheduler(0)
        self.activeTask = None
        self.taskHistory : Task = [] #TODO: ez valid deklaráció Task type-ra?
    def addTask(self, task: Task) -> None: #taszk felvétele a megfelelő szintre
        if task.prior == 0:
            self.RR_Scheduler.addTask(task)
        else:
            self.SRTF_Scheduler.addTask(task)   
    def getInput(self) -> None:
        while True:
            inp = input().strip()
            if not inp:
                break
            inp = inp.split(',')

            t = Task(inp[0], int(inp[1]), int(inp[2]), int(inp[3]))
            self.addTask(t)
            self.taskHistory.append(t)

    def start(self) -> None: #a beadott taszkok után az elindítással kezdődik meg a szimuláció
        
        while not SRTF_Scheduler.List.empty and not RR_Scheduler.FIFO.empty: #amíg van taszk valamelyik szinten
            #choose task
            ##self.activeTask = self.chooseTask()
            if self.activeTask is None: #ha nincs aktív taszkunk
                #choose new task
                    #from 1 or 0
                pass
            if self.activeTask.prior != 1 and not self.SRTF_Scheduler.List.empty: #ha van magas prioritású taszk a Listában
                self.RR_Scheduler.FIFO.push(self.activeTask) #visszakerül a FIFO végére
                self.activeTask = self.SRTF_Scheduler.List.pop()
            else:
                #if nem járt le az időszelet a mostaniról
                if self.activeTask.tickTime < 2:
                    self.activeTask = self.RR_Scheduler.FIFO.pop()
            self.activeTask.tick()
            #print a betűjelet

            pass
        for task in self.taskHistory:
            print(f"{task.name}:{task.wait},", end="")
        print()
        pass
    def chooseTask(self) -> Task: #kiválasztja a soron következő taszkot és azt kiveszi a tárolójából
        pass

    def tick(self) -> None: #egy CPU tick -> az aktuális taszk hátralévő ideje csökken
        #get best task
        #tick task
        task = self.chooseTask()
        if task is None:
            return
        
        #TODO: kell magic
        task.tick()

        #amely taszkok nem futnak, azok várakozási ideje nő
        for t in self.RR_Scheduler.FIFO.Storage:
            t.wait()
        for t in self.SRTF_Scheduler.List.Storage:
            t.wait()
        
    

if __name__ == "__main__":
    scheduler = Scheduler()
    #scheduler.addTask(Task('A', 1,2,3))
    scheduler.getInput()
    scheduler.start()
    
    
    
    
    
