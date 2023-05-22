# -*- coding: utf-8 -*-
import willump
import asyncio
import json
import logging
from tkinter import messagebox
from threading import Thread


#获取当前玩家信息
async def get_current_summoner_data():
    try:
        data = await(await wllp.request("GET", "/lol-summoner/v1/current-summoner")).json()
        return data['summonerId']
    except Exception as e:
        logging.info(f"Unknown Error in get_current_summoner_data:{e}")
        messagebox.showinfo("错误",f"未能获取当前玩家信息，请重新打开脚本")

#获取游戏模式信息
async def get_mode_data():
    data = await(await wllp.request('GET', '/lol-game-queues/v1/queues')).json()
    print(data)

#获取在房间准备时玩家数据，仅有队友
async def get_lobby_members_data():
    data = await(await wllp.request('GET', '/lol-lobby/v2/lobby/members')).json()
    print(data)

#获取当前游戏信息并处理
async def get_current_game_data():
    try:
        data = await(await wllp.request('GET', '/lol-gameflow/v1/session')).json()
        # logging.info(f'{type(data)}::zzzzz::{data}')
        # logging.info(data.keys())
        team1 = data['gameData']['teamOne']
        team2 = data['gameData']['teamTwo']

        #判读应该取哪个team的id列表   
        teamid = await ana_team_data(team1)
        if(mysummonerid not in teamid):
            print("team1 is not my team, need team1id")
        else:
            teamid = await ana_team_data(team2)
            if(mysummonerid not in teamid):
                print("team2 is not my team, need team2id")
            else:
                raise Exception("Can not get correct teamid!!!")
            
        #获取敌方队伍玩家信息并分析是否是胜率队
        iswinteam = True
        for summonerid in teamid:
            record = await get_history_record(summonerid)
            recordlist = record['games']['games']
            #最多取10场比赛数据
            recordlen = 10
            if(len(recordlist)<10):
                recordlen = len(recordlist)
            
            failno = 0
            for i in range(recordlen):
                status = recordlist[i]['participants'][0]['stats']['win']
                gameduration = recordlist[i]['gameDuration']
                # logging.info(f"{type(gameduration)}-zzzzzz-{gameduration}")
                #重开局不算失败
                if(status == False and gameduration > 240):
                    failno += 1
            #敌方有玩家失败率高于20%就认为不是胜率队
            if(failno/recordlen > 0.2):
                iswinteam = False
                break
        
        return iswinteam

    except Exception as e:
        logging.info(f"Unknown Error in get_current_game_data:{e}")
        messagebox.showinfo("错误",f"未知错误{e}")

#处理队伍信息
async def ana_team_data(team):
    listid = []
    for member in team:
        listid.append(member['summonerId'])
    return listid

#获取召唤师信息
async def get_summoner_data(id):
    data = await(await wllp.request('GET', f'/lol-summoner/v1/summoners/{id}')).json()
    # logging.info(f"{json.dumps(data,indent=4)}")
    return data

#获取历史对局信息
async def get_history_record(id):
    data = await(await wllp.request('GET',f'/lol-match-history/v3/matchlist/account/{id}')).json()
    # logging.info(f"{json.dumps(data,indent=4,ensure_ascii=False)}")
    return data

#LCU事件响应函数
async def my_event_handler(eventArgument):
    #当游戏开始时获取所有玩家信息
    if(eventArgument['data']=="GameStart"):
        flag = await get_current_game_data()

        if(flag):
            t = Thread(target=thread_messagebox, args=("警告", "对面是胜率队，2分投！",))
            t.start()
        else:
            t = Thread(target=thread_messagebox, args=("提示", "对面不是胜率队，放心虐。",))
            t.start()
    
def thread_messagebox(level, message):
    messagebox.showinfo(f"{level}",f"{message}")

#建立连接，调用功能函数
async def main():  
    logging.basicConfig(level=logging.INFO,
                        filename='LCUapi.log',
                        filemode="w",
                        )
    global wllp
    global isconnect
    global mysummonerid
    isconnect = False
    while(True):
        if(isconnect):
            try:
                result = await wllp.request('GET', '/riot-messaging-service/v1/state')
                if(result.status == 200):
                    await asyncio.sleep(2)
            except:
                isconnect = False
            
        else:
            wllp = await willump.start()
            isconnect = True
            mysummonerid = await get_current_summoner_data()
            #订阅LCU事件
            my_subscription = await wllp.subscribe('OnJsonApiEvent', default_handler=my_event_handler)

if __name__ == '__main__':
    asyncio.run(main())