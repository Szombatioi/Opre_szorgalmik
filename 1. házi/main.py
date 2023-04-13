class Task: #taszk osztály
    def __init__(self, name: str, prior: int, arrival: int, length: int) -> None:
        self.name = name            #taszk betűjele
        self.prior = prior          #taszk prioritása
        self.arrival = arrival      #taszk indítási ideje
        self.length = length        #taszk CPU-löketideje
        self.remTime = length       #taszk futásának hátralévő ideje TODO: lehet nem kell?
        self.waitTime = 0
        self.tickTime = 0           #taszk futásának eltelt ideje
    def wait(self) -> None:
        self.waitTime+=1
    def tick(self) -> None:
        self.remTime -= 1
        self.tickTime -= 1
    
    
    #test?
    def __str__(self) -> str:
        return f"{self.name},{self.prior},{self.arrival},{self.remTime}"

class FIFO: #FIFO osztály az RR ütemezőhöz
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e
        
    def push(self, elem: Task) -> None: #FIFO végére szúr egy új taszkot
        self.Storage.append(elem) #fordított sorrend lesz, mert ez egy tömb
        elem.wait()
        self.empty = False

    def pop(self) -> Task: #FIFO elejéről kiveszi az ott lévő taszkot
        res = self.Storage.pop(0) if len(self.Storage) != 0 else None
        if len(self.Storage) == 0:
            self.empty = True
        return res
    def wait(self):
        for t in self.Storage:
            t.wait()
    def top(self) -> Task:
        return self.Storage[0]
    
class List: #SRTF ütemezőhöz Lista
    def __init__(self) -> None:
        self.Storage = [] #egyszerű implementáció, ezért csak egy tömb
        self.empty = True #üres-e

    def push(self, elem: Task) -> None:   #beszúrja a megfelelő helyre az új taszkot
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
    def wait(self):
        for t in self.Storage:
            t.wait()
    def top(self) -> Task:
        return self.Storage[len(self.Storage)-1]

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
        self.List.push(task)
    def popTask(self) -> Task: #taszk kiválasztása a lista elejéről
        return self.List.pop()
    def tick(self): #TODO: ha ...
        pass
        
class Scheduler:
    def __init__(self) -> None:
        self.RR_Scheduler = RR_Scheduler(1, 2)
        self.SRTF_Scheduler = SRTF_Scheduler(0)
        self.finishedTasks = []
        self.activeTask = None
        self.text = ""
        self.temp = [] #átmeneti mappa a még meg nem érkezett taszkoknak
        
    def addTask(self, task: Task) -> None: #taszk felvétele a megfelelő szintre
        if task.prior == 1:
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
            #self.addTask(t)
            self.temp.append(t)
            print("Added: ",t)
            
    def work(self):
        time = 0
        for i in range(len(self.temp)):
        
            print("Is it? ",self.temp[i].arrival)
            if self.temp[i].arrival <= time:
                self.addTask(self.temp[i])
                self.temp.pop(i)
                i+=1
        while (not self.RR_Scheduler.FIFO.empty) and (not self.SRTF_Scheduler.List.empty): #itt egy iteráció = egy taszk kiválasztása

            """for task in self.temp:
                print("Is it? ",task.arrival)
                if task.arrival <= time:
                    self.addTask(task)
                    self.temp.remove(task)
                    print("removed")"""
            
            ###################################
            # choose task -> prior 1, aztán 0 #
            ###################################
            
            if self.activeTask is not None:
                if self.activeTask.prior == 0: #SRTF-ből van a taszk
                    if not self.RR_Scheduler.FIFO.empty and self.RR_Scheduler.FIFO.top().arrival <= time:
                        self.SRTF_Scheduler.List.push(self.activeTask)
                        self.activeTask = self.RR_Scheduler.FIFO.pop()
                    elif self.SRTF_Scheduler.List.top().arrival <= time and self.SRTF_Scheduler.List.top().remTime < self.activeTask.remTime:
                        self.SRTF_Scheduler.List.push(self.activeTask)
                        self.activeTask = self.SRTF_Scheduler.List.pop()
                else: #self.activeTask.prior==1
                    if self.RR_Scheduler.FIFO.top().remTime < self.activeTask.remTime:
                        self.RR_Scheduler.FIFO.push(self.activeTask)
                        self.activeTask = self.RR_Scheduler.FIFO.pop()
            else:
                if not self.RR_Scheduler.FIFO.empty and self.RR_Scheduler.FIFO.top().arrival <= time:
                    self.activeTask = self.RR_Scheduler.FIFO.pop()
                elif self.SRTF_Scheduler.List.top().arrival <= time:
                    self.activeTask = self.SRTF_Scheduler.List.pop()
            print("Task: ",self.activeTask)
            self.activeTask.tick()
            if len(self.text) == 0 or (self.text[len(self.text)-1] != self.activeTask.name):
                self.text += self.activeTask.name

            #minden másik task várakozik
            self.RR_Scheduler.FIFO.wait()
            self.SRTF_Scheduler.List.wait()

            if self.activeTask.remTime == 0:
                print(f"---Task_{self.activeTask.name} is finished")
                self.finishedTasks.append(self.activeTask)
                self.activeTask = None
                continue

            if self.activeTask.prior == 0 and self.activeTask.tickTime == 0: #ha lejár az időszelet, mindenképp kerüljön vissza
                print("---Time is over")
                self.RR_Scheduler.FIFO.push(self.activeTask)
                self.activeTask = None
            
            time += 1
            
            
        print("out1:", self.text, "\nout2:")
        for t in self.finishedTasks:
            print(f"{t.name}:{t.waitTime}", end=",")
        print()


if __name__ == "__main__":
     scheduler = Scheduler()
     scheduler.getInput()
     print("Start:")
     scheduler.work()
    
    
    
    
    
    
