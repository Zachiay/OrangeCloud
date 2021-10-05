import random
#添加人机对战的功能
global A
global B
def main():
    while True:
        Welcome()
        op=int(input("请选择游戏模式：1.人人对战 2.人机对战 3.人人在线对战"))
        if op==1:#人人对战
            A_vs_B()
        elif op == 2:#人机对战
            player_vs_Peppa()
        elif op == 3:#人人在线对战
            pass        # 玩家初始化'''
        ready()
        Turn = 1
        Start()  # 游戏初始化并开始
        while True:
            # 游戏过程_轮流出牌
            if Turn:
                A.action()
            else:
                B.action()
            Turn = 1 - Turn

            if not cardList:  # card_total == 0:
                End()
                result = int(A.total - B.total)
                if result != 0:
                    if result > 0:
                        B.showname()
                    else:
                        A.showname()
                    print("is the winner, congratulations!")
                else:
                    print("The game ends in a tie.")
                break
            else:
                continue

        if str(input('Wanan play again? (y or n)')) == 'y':
            continue
        else:
            Thank()
            break
def A_vs_B():
    global A
    global B
    A = User(input('玩家A命名：'))
    B = User(input('玩家B命名: '))  # 玩家初始化

def player_vs_Peppa():
    global A
    global B
    A = User(input('玩家命名：'))
    B = Peppa(input('对手命名: '))

#交互语句
def Welcome():
    print("---------------------Welcome to Pigtail！--------------------------")
def Start():
    print("-------------------------Game on-----------------------------------")
def End():
    print("Game over")
def Thank():
    print("Thank you!")
'''def ready():
    global cardList
    random.shuffle(cardList)   #洗牌
    for i in range(0,4):
        for x in cardList[i*13:i*13+13]:
            print("".join(x),end='\t')
        print(" ")'''
def ready():
    global cardList
    random.shuffle(cardList)   #洗牌
    for i in range(0,4):
        for x in cardList[i*7:i*7+7]:
            print("".join(x),end='\t')
        print(" ")
# PickArea 牌组
'''cardList = [('红心', 'A'), ('红心', '2'), ('红心', '3'), ('红心', '4'), ('红心', '5'), ('红心', '6'), ('红心', '7'),
            ('红心', '8'), ('红心', '9'), ('红心', '10'), ('红心', 'J'), ('红心', 'Q'), ('红心', 'K'),
            ('方块', 'A'), ('方块', '2'), ('方块', '3'), ('方块', '4'), ('方块', '5'), ('方块', '6'), ('方块', '7'),
            ('方块', '8'), ('方块', '9'), ('方块', '10'), ('方块', 'J'), ('方块', 'Q'), ('方块', 'K'),
            ('黑桃', 'A'), ('黑桃', '2'), ('黑桃', '3'), ('黑桃', '4'), ('黑桃', '5'), ('黑桃', '6'), ('黑桃', '7'),
            ('黑桃', '8'), ('黑桃', '9'), ('黑桃', '10'), ('黑桃', 'J'), ('黑桃', 'Q'), ('黑桃', 'K'),
            ('梅花', 'A'), ('梅花', '2'), ('梅花', '3'), ('梅花', '4'), ('梅花', '5'), ('梅花', '6'), ('梅花', '7'),
            ('梅花', '8'), ('梅花', '9'), ('梅花', '10'), ('梅花', 'J'), ('梅花', 'Q'), ('梅花', 'K')]'''
cardList = [('红心', 'A'), ('红心', '2'), ('红心', '3'), ('红心', '4'), ('红心', '5'), ('红心', '6'), ('红心', '7'),
            ('方块', 'A'), ('方块', '2'), ('方块', '3'), ('方块', '4'), ('方块', '5'), ('方块', '6'), ('方块', '7'),
            ('黑桃', 'A'), ('黑桃', '2'), ('黑桃', '3'), ('黑桃', '4'), ('黑桃', '5'), ('黑桃', '6'), ('黑桃', '7'),
            ('梅花', 'A'), ('梅花', '2'), ('梅花', '3'), ('梅花', '4'), ('梅花', '5'), ('梅花', '6'), ('梅花', '7')]

# SetArea 放置区
card=["flo",1]      #新出的牌
Up_card = "flower"  #顶部花色
SAtotal = 0         #放置区卡牌数
SA_Heart = []  #红心
SA_Spade = []  #黑桃
SA_Cube = []  #梅花
SA_Diamond = [] #方块 #放置区卡牌标记

def addSA(x):  #传入当前的卡片
    global SAtotal
    SAtotal+=1
    if x[0]=="黑桃":
        SA_Spade.append(x)
    elif x[0]=="红心":
        SA_Heart.append(x)
    elif x[0]=="方块":
        SA_Diamond.append(x)
    elif x[0]=="梅花":
        SA_Cube.append(x)

def clrSA():
    global SAtotal
    global Up_card
    SAtotal=0
    Up_card="flower"
    SA_Diamond.clear()
    SA_Spade.clear()
    SA_Cube.clear()
    SA_Heart.clear()
    print("---------------------------放置区已清空-------------------------------------------------------------")

# 游戏玩家类
class User:
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.flower = "card花色"
        self.number = 0
        self.diamond = []
        self.cube = []
        self.heart = []
        self.spade = []
    def action(self):
        print("-----------------------------------------------------------该回合由",self.name,"出牌--------------")
        global card
        global Up_card
        #print("当前放置区顶部卡牌花色为",Up_card)
        if self.total == 0:
            #print("您当前没有手牌，已为您选择摸牌操作")
            self.draw()
        else:
            self.ShowPoker()
            print("您当前手牌共",self.total,"张，请选择执行操作:", end=' ')
            #print("您当前手牌如上，请选择执行操作",end=' ')
            if int(input("1.摸牌\t2.出牌\n")) == 1:
                self.draw()
            else:
                self.OutPoker()
        addSA(card)
        if card[0]==Up_card :
            self.Allin()
            clrSA()
        else:
            Up_card=self.flower
       # print("                                                                           该回合后顶部卡牌花色为",Up_card)
    def draw(self):
        global card
        card = cardList.pop()
        print(self.name, "摸了一张牌：\t\t                            ","".join(card))
        self.flower=card[0]
    def OutPoker(self):
        global card
        op = int(input("请选择您要出的手牌花色：1.黑桃 2.红心 3.梅花 4.方块"))
        if op == 1:
            self.flower = "黑桃"
        elif op == 2:
            self.flower = "红心"
        elif op == 3:
            self.flower = "梅花"
        elif op == 4:
            self.flower = "方块"
        self.number = input("请选择您要出的手牌数字：")
        card = (self.flower, self.number)
        self.delcard(card)
        print(self.name, "出了一张牌：：                                     ","".join(card))
    def delcard(self,x):
        global card
        self.total -= 1
        if x[0] == "黑桃":
            self.spade.remove(x)
        elif x[0] == "红心":
            self.heart.remove(x)
        elif x[0] == "方块":
            self.diamond.remove(x)
        elif x[0] == "梅花":
            self.cube.remove(x)
    def ShowPoker(self):
        if self.diamond:
            for x in self.diamond:
                print("".join(x), end='\t')
            print(" ")
        if self.cube:
            for x in self.cube:
                print("".join(x), end='\t')
            print(" ")
        if self.heart:
            for x in self.heart:
                print("".join(x), end='\t')
            print(" ")
        if self.spade:
            for x in self.spade:
                print("".join(x), end='\t')
            print(" ")
    def Allin(self):
        self.total+=SAtotal
        self.diamond.extend(SA_Diamond)
        self.cube.extend(SA_Cube)
        self.heart.extend(SA_Heart)
        self.spade.extend(SA_Spade)
    def showname(self):
        print(self.name,end=' ')

class Peppa(User):
    '''自动出牌算法：选择手牌中其他花色数量最多的出
    如果剩下与底牌同花色则摸牌'''
    def __init__(self,name):
        super().__init__(name)
        self.cntdiamond=0
        self.cntcube=0
        self.cntspade=0
        self.cntheart=0
    def action(self):
        print("---------------------------------------------------------该回合由",self.name,"出牌--------------")
        global card
        global Up_card
        #print("当前放置区顶部卡牌花色为",Up_card)
        if self.total == 0:
            #print("您当前没有手牌，已为您选择摸牌操作")
            self.draw()
        else:
            if self.onlydraw():
                self.draw()
            else:
                self.OutPoker()
        addSA(card)
        if card[0]==Up_card :
            self.Allin()
            clrSA()
        else:
            Up_card=self.flower
        #print("                                                                             该回合后顶部卡牌花色为",Up_card)
    def OutPoker(self):
            global card

            if Up_card == "红心":
                if self.cntdiamond >= self.cntcube and self.cntdiamond >= self.cntspade:
                    card=self.diamond.pop()
                    self.flower="方块"
                    self.cntdiamond-=1
                elif self.cntspade >= self.cntdiamond and self.cntspade> self.cntcube:
                    card = self.spade.pop()
                    self.flower="黑桃"
                    self.cntspade-=1
                else:
                    card = self.cube.pop()
                    self.flower="梅花"
                    self.cntcube-=1
            elif Up_card == "黑桃":
                if self.cntdiamond >= self.cntcube and self.cntdiamond >= self.cntheart:
                    card=self.diamond.pop()
                    self.flower="方块"
                    self.cntdiamond -= 1
                elif self.cntheart >= self.cntdiamond and self.cntheart> self.cntcube:
                    card = self.heart.pop()
                    self.flower="红心"
                    self.cntheart-=1
                else:
                    card = self.cube.pop()
                    self.flower="梅花"
                    self.cntcube -= 1
            elif Up_card == "梅花":
                if self.cntspade >= self.cntdiamond and self.cntspade >= self.cntheart:
                    card=self.spade.pop()
                    self.flower="黑桃"
                    self.cntspade -= 1
                elif self.cntheart >= self.cntspade and self.cntheart> self.cntdiamond:
                    card = self.heart.pop()
                    self.flower="红心"
                    self.cntheart-=1
                else:
                    card = self.diamond.pop()
                    self.flower="方块"
                    self.cntdiamond -= 1
            elif Up_card == "方块":
                if self.cntspade >= self.cntcube and self.cntspade >= self.cntheart:
                    card=self.spade.pop()
                    self.flower="黑桃"
                    self.cntspade -= 1
                elif self.cntheart >= self.cntspade and self.cntheart> self.cntcube:
                    card = self.heart.pop()
                    self.flower="红心"
                    self.cntheart-=1
                else:
                    card = self.cube.pop()
                    self.flower="梅花"
                    self.cntcube -= 1
            else:
                if self.cntspade >= self.cntdiamond and self.cntspade >= self.cntheart and self.cntspade >= self.cntcube:
                    card=self.spade.pop()
                    self.flower="黑桃"
                    self.cntspade -= 1
                elif self.cntheart >= self.cntspade and self.cntheart> self.cntdiamond and self.cntheart >=self.cntcube:
                    card = self.heart.pop()
                    self.flower="红心"
                    self.cntheart-=1
                elif self.cntdiamond >= self.cntspade and self.cntdiamond >= self.cntheart and  self.cntdiamond >=self.cntcube:
                    card = self.diamond.pop()
                    self.flower="方块"
                    self.cntdiamond -= 1
                else:
                    card = self.cube.pop()
                    self.flower="梅花"
                    self.cntcube -= 1
            self.total -= 1
            print(self.name, "出了一张牌：                                  ", "".join(card))
    def onlydraw(self):
        if Up_card=="红心" and self.cntdiamond+self.cntcube+self.cntspade==0:
            return 1
        if Up_card=="黑桃" and self.cntdiamond+self.cntcube+self.cntheart==0:
            return 1
        if Up_card=="梅花" and self.cntdiamond+self.cntheart+self.cntspade==0:
            return 1
        if Up_card=="方块" and self.cntheart+self.cntcube+self.cntspade==0:
            return 1
        else: return 0
    def Allin(self):
            self.total += SAtotal
            self.diamond.extend(SA_Diamond)
            self.cntdiamond+=len(SA_Diamond)
            self.cube.extend(SA_Cube)
            self.cntcube+=len(SA_Cube)
            self.heart.extend(SA_Heart)
            self.cntheart+=len(SA_Heart)
            self.spade.extend(SA_Spade)
            self.cntspade+=len(SA_Spade)
    def delcard(self, x):
        pass

main()
