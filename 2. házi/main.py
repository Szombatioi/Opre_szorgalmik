class Page:
    def __init__(self, name: str) -> None:
        self.name = name
        self.value: int = None
        self.maxFreeze = 3
        self.freeze = 3
        self.frozen = False
        
        
    def __str__(self) -> str:
        return f"{self.name} - {self.value}"

class Fifo:
    def __init__(self) -> None:
        self.storage = []
    def Push(self, p: Page) -> None:
        self.storage.insert(0,p)
    def PushFront(self, p: Page) -> None:
        self.storage.append(p)
    def Pop(self) -> Page:
        return self.storage.pop(len(self.storage)-1)
    def Contains(self, value: int) -> bool:
        for x in self.storage:
            if x.value == value:
                return True
        return False
    def HasNoFree(self) -> bool:
        for x in self.storage:
            if x.freeze > 0:
                return False
        return True
    # def Give(self) -> Page: #átadja a lapot, ilyenkor visszakerül a fagyasztás értéke
    #     p = self.storage.pop(len(self.storage)-1)
    #     p.freeze = p.maxFreeze
    #     return p

if __name__ == "__main__":
    line = input().split(',') #1,2,3,-1,5,-1
    pFaults = 0
    
    p1 = Page("A")
    p2 = Page("B")
    p3 = Page("C")
    
    fifo = Fifo()
    
    fifo.Push(p1)
    fifo.Push(p2)
    fifo.Push(p3)
    
    for ref in line: #minden hivatkozásra
        ref = abs(int(ref))
        if fifo.Contains(ref):
            print("-", end="")
        else:
            if fifo.HasNoFree():
                print("*", end="")
            else:
                page = fifo.Pop()
                if page.frozen and page.freeze > 0: #ha a FIFO elején még fagyasztva van a keret
                    page.freeze -= 1
                    fifo.Push(page)
                else: #TODO: a frozen tul-t állítsuk át néha (de hogy?)
                    page.freeze = 3 #visszaállítás
                    page.value = ref
                    fifo.Push(page)
                    pFaults += 1
                    print(page.name, end="")
    print(f"\n{pFaults}")
    
