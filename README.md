# LOLWinTeamJudge
Use LCU api get players' history to help judge if enemy team is a winning team.
调用LCU api获取LOL敌方队伍玩家历史对局信息并判断对方是否是胜率队  
  
## 如何使用
本脚本需要Python3环境并使用了Willump库进行websocket连接，使用了QT5绘制了简单的主界面  
可用以下命令安装相关包：  
```
pip install willump
pip install PyQt5
```
运行main.py即可弹出主界面，当游戏进入加载画面时，便会弹出提示窗口，如下图所示：  
![image](https://github.com/shallbedif/Picture/blob/main/LOLWinTeamJudge/messagewindow.png)  

## 判断规则
获取敌方玩家最近十场游戏对局记录，当其中任意一位玩家有两局以上对局失败，即敌方任意一名玩家的失败率超过20%，就认为敌方队伍不是胜率队。重开局不视作失败场次。  

## 免责声明
LOLWinTeamJudge isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

## 如果可以
如果你觉得这个小脚本对你的LOL游戏体验有提升并且手有余力的话，可以请我喝杯咖啡共享喜悦噢！
![image](https://github.com/shallbedif/Picture/blob/main/Awards/combine.png)
