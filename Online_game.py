
# coding:utf8
import requests, json,time

# 设置操作间隔为3s
def sleeptime (hour, min, sec):
    return hour * 3600 + min * 60 + sec
second = sleeptime(0, 0, 3)

global A,r_last
r_last={"data":None}

# 接口访问变量
global Student_id
global Password
global My_token
global Header
global uuid

# 登录
def Register ():        #登录
    global My_token
    global Header
    Student_id = input("请输入用户账号：")
    Password = input("请输入密码：")  # 输入用户信息
    data = {
        'student_id': Student_id,
        'password': Password
    }
    url = 'http://172.17.173.97:8080/api/user/login'
    response = requests.post(url=url, data=data)  # 发送登录请求
    r = response.json()  # 将返回转化成dict类型
    status=r['status']
    if status==200:    # 判断登录状态
        print("登录成功")
    else:
        print("登录失败，请稍后重试")
    My_token=r['data']['token']
    Header = {
        'Authorization': My_token
    }   # 将返回的token放入其他接口的header中
# 创建对局
def build_game():
    global uuid
    global A
    A = online_pig(1,'host')
    url='http://172.17.173.97:9000/api/game'
    op=int(input("您是否要公开对局？1.是\t2.否"))
    if op==1:
        data={
            "private": False  # 可供查询
        }
    else:
        data = {
            "private": True  # 仅能通过uuid加入
        }
    response = requests.post(url=url, data=data, headers=Header)  # 发送登录请求
    r = response.json()  # 将返回转化成dict类型
    # print(r)
    if r['code']==200:    # 判断登录状态
        print("创建对局成功")
    else:
        print("创建失败，请稍后重试")
    uuid=r['data']['uuid']
    print("创建对局uuid=",uuid)
# 加入对局
def join_game():
    global uuid
    global A
    A = online_pig(2, 'client')
    while True:
        print("请选择加入对局的方式")
        op=int(input("1.输入对局标识码\t 2.在对局列表中选择\t"))
        if op== 1:
            uuid=input("请输入对局标志码：")
        else:
            get_gamelist()
            uuid = input("请将您想加入的对局标志码复制到此处：")
        # print("uuid=",uuid)
        url='http://172.17.173.97:9000/api/game/'+uuid
        # print("url=",url)
        response = requests.post(url=url, headers=Header)
        r = response.json()  # 将返回转化成dict类型
        #print(r)
        if r['code'] == 200:  # 判断登录状态
            print("加入对局成功")
            break
        else:
            print("加入失败，请稍后重试")
# 获取公开且未完成的对局列表
def get_gamelist():
    url='http://172.17.173.97:9000/api/game/index'
    data={
        'page_size':10,
        'page_num':1
    }
    response = requests.get(url=url, data=data, headers=Header)
    r = response.json()
    if r['code']==200:
        print("获取对局列表成功")
    else:
        print("获取失败，请稍后重试")
    game_list = r['data']['games']
    for x in game_list: # 打印输出对局列表
        y = json.dumps(x, indent=4)  # indent  缩进，可自定义，4表示缩进4个空格
        print(y)
# 获取当前对局的对局结果
def this_result():
    url = 'http://172.17.173.97:9000/api/game/' + uuid
    response = requests.get(url=url, headers=Header)
    r = response.json()
    if r['code'] == 200:
        print("获取对局结果成功")
    else:
        print("获取失败，请稍后重试")
    winner = r['data']['winner']    # 获取赢家信息
    if winner:  # 宣布结果
        winner_id= r['data']['client_id']
    else:
        winner_id = r['data']['host_id']
    print(winner_id,' is the winner, congratulations!')
    op=int(input("是否查看对局结束信息？1.是 2.否"))
    if op==1:
        print(r)
    else:
        pass
# 获取对局列表中的对局结果
def get_result():
    print("请选择您要查看的对局")     # 选择所要查看的对局
    op = int(input("1.手动输入对局标识码\t 2.在对局列表中选择\t"))
    if op == 1:
        uuid = input("请输入对局标志码：")
    else:
        get_gamelist()
        uuid = input("请将您要查看的对局标志码复制到此处：")
    url = 'http://172.17.173.97:9000/api/game/' + uuid
    response = requests.get(url=url, headers=Header)
    r = response.json()
    if r['code'] == 200:
        print("获取对局结果成功，当前对局信息如下：")
        print(r)
    else:
        print("获取失败，请稍后重试")
# 查询游戏是否开始
def get_begin():
    global r_last
    print("查询状态",end=' ')
    url = 'http://172.17.173.97:9000/api/game/' + uuid + '/last'
    response = requests.get(url=url, headers=Header)
    r = response.json()
    #print(r)
    if r['code'] == 403:    # 游戏未开始 返回0
        print(r['data']['err_msg'])
        return 0
    if r['code'] == 200:    # 游戏开始 返回1
        print(r['data']['last_msg'])
        return 1
# 获得上步操作：返回r
def get_last():
    global r_last
    url = 'http://172.17.173.97:9000/api/game/' + uuid + '/last'
    while True:
        # 上一步存储的r_last为我方操作
        # 循环获取直到对方出牌
        response = requests.get(url=url, headers=Header)
        r = response.json()
        #print("last_msg=", r['data']['last_msg'])
        if r == r_last:
            pass # print("等待对方出牌...")
        else:
            r_last=r
            print(r['data']['last_msg'])
            return r
# 发送操作:返回r
def ol_action():
    global left_card
    global r_last
    url = 'http://172.17.173.97:9000/api/game/' + uuid
    response = requests.put(url=url,data=send_data, headers=Header)
    r = response.json()     # 发送操作信息
    #print(r['data']['last_msg'])    # 输出操作信息
    r_last=r    # 更新上步操作

# ----------------------------------------------------------------------------------------
def Online_game():  #在线对战主函数
    Register()
    while True:
        #op=int(input("1.开始游戏\t 2.查看其他对局信息"))
        op=1
        if op==1 :
            op=int(input("请选择游戏开始的方式：1.创建对局\t2.加入对局"))
            if op==1:
                build_game()
            else:
                join_game()
            '''build_game()
            join_game()'''
            game_action()
            this_result()
            print("Thanks!")
            break
        else:
            get_result()
# 游戏过程
def game_action():
    global A,r0,send_data,card
    while True:  # 每隔3s查询对局是否开始
        second = sleeptime(0, 0, 3)
        time.sleep(second)
        now=get_begin()
        if now: # 开始则退出循环
            break
    print("双方已就绪，游戏开始")
    while left_card:
        get_last()  # 获取上步操作 处理 r_last
        if r_last['data']["your_turn"]: # True
            A.action()  # 进行我方操作
        else:
            A.enquire()   # 处理对方操作

# 牌局信息变量
op=0     # 出牌选择：1.摸牌 2.出牌
left_card=52 # 卡组剩余卡牌数
send_data={ } #玩家操作
# SetArea 放置区
card=["flo",1]      # 新出的牌
Up_card = "flower"  # 顶部花色
SAtotal = 0         # 放置区卡牌数
SA_Heart = []  # 红心
SA_Spade = []  # 黑桃
SA_Cube = []  # 梅花
SA_Diamond = [] # 方块       # 放置区卡牌标记

# 玩家出牌后更新放置区
def addSA(x):
    global SAtotal
    SAtotal+=1  # 放置区卡牌数加一
    if x[0]=="黑桃":
        SA_Spade.append(x)
    elif x[0]=="红心":
        SA_Heart.append(x)
    elif x[0]=="方块":
        SA_Diamond.append(x)
    elif x[0]=="梅花":
        SA_Cube.append(x)   # 将卡牌添加至放置区
# 清空放置区
def clrSA():
    global SAtotal
    global Up_card
    SAtotal=0   # 放置区卡牌数置为0
    Up_card="flower" # 放置区顶部花色置为初始值
    SA_Diamond.clear()
    SA_Spade.clear()
    SA_Cube.clear()
    SA_Heart.clear()    # 分别清空放置区牌组各卡牌列表
    #print("---------------------------放置区已清空-------------------------------------------------------------")
# 转换卡牌格式
def switchcard(opstr):  # 返回数据转换成本地出牌
    global card
    flo=opstr[4:5]
    if flo=='S': flo='黑桃'
    elif flo=='H': flo='红心'
    elif flo=='D': flo='方块'
    elif flo=='C': flo='梅花'
    num=opstr[5:]
    card=(flo,num)
def cardswitch():   # 本地出牌转换成发数据
    if card[0]=='黑桃':
        cardstr="S"+str(card[1])
    elif card[0]=='红心':
        cardstr="H"+str(card[1])
    elif card[0]=='方块':
        cardstr="D"+str(card[1])
    elif card[0]=='梅花':
        cardstr="C"+str(card[1])
    return cardstr


class online_pig():
    def __init__(self,name,type):  # 玩家初始化
        self.name=name
        self.player_type=type
        self.flower = "card花色"  # 选择出牌的花色
        self.number = 0  # 选择出牌的数字
        self.total = 0  # 当前手牌数
        self.diamond = []
        self.cube = []
        self.heart = []
        self.spade = []  # 当前手牌列表
        self.cntdiamond = 0
        self.cntcube = 0
        self.cntspade = 0
        self.cntheart = 0  # 当前各花色卡牌数
        self.manage = 0  # 托管标志位 手动为0 托管为1
        self.opponent = 0  # 存储对手卡牌数量
        self.last_SAtotal = 0  # 存放上一轮结束后存储区的卡牌数
        self.winwin = 0  # 必胜局面标志位 初始为0 必胜更新为1
    # 判断host or client
    def host_or_client(self):
        if self.name==1:    # host
            return 1
        else:   # client
            return 0
    # 玩家行动
    def action(self):
        global card
        global Up_card
        # 选择要出的卡牌
        if self.manage==1:  # 托管模式
            self.AI_action()
        else:   # 玩家模式
            self.ShowPoker()    # 显示当前手牌 询问玩家操作
            print("您当前手牌共", self.total, "张，请选择执行操作:", end=' ')
            op=int(input("1.摸牌\t2.出牌\t3.托管"))
            if op == 1:
                self.draw()     # 直接摸牌
            elif op== 2:
                self.OutPoker()    # 人工选择出牌
            elif op== 3:
                self.manage=1   # 托管置为1
                self.AI_action()    # AI出牌
        # 处理出牌过程变量
        addSA(card) # 增加放置区卡牌
        if card[0]==Up_card :   # 判断是否与放置区花色相同
            self.Allin()    # 将放置区卡牌尽数收入手牌
            clrSA()     # 清空放置区
        else:
            Up_card=card[0]    # 更新放置区卡牌
        self.last_SAtotal = SAtotal # 标记放置区此时的数量
        if self.opponent > left_card*3 +self.total:
            self.winwin=1  # 判断是否为必胜局面:对方手牌 > 放置区剩余手牌 *3 +我方手牌

    # 查询当前游戏局面
    def enquire(self):
        global Up_card
        global left_card
        code=r_last['data']['last_code']
        op=code[2:3]   # 拆分数据 获取对方操作
        switchcard(code)    # 转换成本地格式
        #print(code)
        #print("op=",op,"\tcard=",card)
        if op=='0' :  # 对方摸牌
            left_card-=1    # 未翻牌组数-1
        else :  # 对方出牌
            self.opponent-=1    # 对方卡牌数-1
        addSA(card)  # 增加放置区卡牌
        if card[0] == Up_card:  # 判断是否与放置区花色相同
            self.opponent += SAtotal # 增加对方卡牌数量
            clrSA()  # 清空放置区
        else:
            Up_card = card[0]  # 更新放置区卡牌

        if self.opponent > left_card*3 +SAtotal+ self.total:
            self.winwin=1   # 必胜局面：对方手牌 > 我方手牌 +放置区剩余手牌 +未翻卡组数*3

    # 1.摸牌
    def draw(self):
        global card,send_data,left_card,r_last
        send_data={
            "type": 0
        }
        ol_action() # 发送并转换数据
        switchcard(r_last['data']['last_code'])
        left_card-=1

    # 2.出牌
    def OutPoker(self):
        global card,send_data
        op = int(input("请选择您要出的手牌花色：1.黑桃 2.红心 3.梅花 4.方块"))
        if op == 1:     # 询问玩家出牌操作
            self.flower = "黑桃"
        elif op == 2:
            self.flower = "红心"
        elif op == 3:
            self.flower = "梅花"
        elif op == 4:
            self.flower = "方块"
        self.number = input("请选择您要出的手牌数字：")
        card = (self.flower, self.number)
        cstr=cardswitch()
        send_data={
          "type": 1,
          "card": cstr
        }
        ol_action()
        self.delcard(card)  # 删除这张牌
    # 3.托管功能
    # 游戏行动
    def AI_action(self):
        # print("---------------------------------------------------------该回合由", self.name, "出牌--------------")
        global card
        global Up_card
        # print("当前放置区顶部卡牌花色为",Up_card)
        if self.total == 0 or self.winwin == 1:  # 没有手牌或必胜
            #print("您当前没有手牌，已为您选择摸牌操作")
            self.draw()
        else:
            if self.onlydraw():  # 若仅剩与放置区顶部卡牌花色相同手牌 则只能摸牌
                self.draw()
            else:
                self.AI_OutPoker()
    # ai出牌算法：
    def AI_OutPoker(self):
        # 在已有手牌中选择非顶部花色且数量最多的卡牌
        global card
        if Up_card == "红心":
            if self.cntdiamond >= self.cntcube and self.cntdiamond >= self.cntspade:
                card=self.diamond.pop()
                self.flower="方块"
                self.cntdiamond-=1
            elif self.cntspade >= self.cntdiamond and self.cntspade>= self.cntcube:
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
        cstr = cardswitch()
        send_data = {
            "type": 1,
            "card": cstr
        }
        ol_action()
    # 出牌后删除这张牌
    def delcard(self,x):
        global card
        self.total -= 1
        if x[0] == "黑桃":
            self.spade.remove(x)
            self.cntspade-=1
        elif x[0] == "红心":
            self.heart.remove(x)
            self.cntheart-=1
        elif x[0] == "方块":
            self.diamond.remove(x)
            self.cntdiamond-=1
        elif x[0] == "梅花":
            self.cube.remove(x)
            self.cntcube-=1
    # 显示当前牌组
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
    # 判断是否只剩下与放置区顶部花色相同手牌，如是则返回1：选择摸牌
    def onlydraw(self):
        if Up_card == "红心" and self.cntdiamond + self.cntcube + self.cntspade == 0:
            return 1
        if Up_card == "黑桃" and self.cntdiamond + self.cntcube + self.cntheart == 0:
            return 1
        if Up_card == "梅花" and self.cntdiamond + self.cntheart + self.cntspade == 0:
            return 1
        if Up_card == "方块" and self.cntheart + self.cntcube + self.cntspade == 0:
            return 1
        else:
            return 0
    # 将放置区所有牌收入牌组
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
    # 显示赢家姓名
    def showname(self):
        print(self.player_type,end=' ')

#Online_game()