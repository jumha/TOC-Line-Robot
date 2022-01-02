# BULLs & COWs LINEBot


A Line bot based on a finite state machine



## Setup

### Prerequisite

* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency

```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
  * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
  * [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)






## Finite State Machine
![](https://i.imgur.com/FGxjz5t.png)



## Usage

The initial state is set to `initial`.

Every time `initial` state is triggered by `start` to `gaming` state. Then, it will be triggered to `finish` state by `correct` or `loss` or return to itself by `wrong`. For `finish` state, it can be triggered by `restart` to `gaming`. Every state can be triggered by `quit` to `initial` state.

* initial
  * Input: "新遊戲"
    * Reply: "遊戲開始，總共有8次機會 請輸入四位數，數字不重複"
        *  Generate a random number with for digits
* gaming
    * Input: 4 digits number and no duplicates, like "1234"
        * Reply: "XAYB, 你還有n次機會" if you guess wrong
        * Reply: "XAYB, 答案是abcd 遊戲結束你輸了" if you guess wrong 8 times
        * Reply: "4A0B, 賓果，答對了!" if you get the answer
    * Input: 4 digits number with duplicates
        * Reply: "數字不要重複，請再輸入一次:"
    * Input: 1000 < number < 9999
        * Reply: "輸入四位數就好，請再輸入一次:"
    * Input: "答案是abcd 結束遊戲，你輸了! 輸入新遊戲即可開始進行遊戲"
* finish
    * Input: "再玩一次"
        * Reply: "遊戲開始，總共有8次機會 請輸入四位數，數字不重複"
            * Generate a random number with for digits
    * Input: "結束遊戲"
        * Reply: "結束遊戲 輸入新遊戲即可開始進行遊戲"

## Demo
![](https://i.imgur.com/ZS8j19b.jpg)
![](https://i.imgur.com/2OavJvn.jpg)
![](https://i.imgur.com/3fggXXF.jpg)
![](https://i.imgur.com/EFNeXkC.jpg)
![](https://i.imgur.com/ldPYhOr.jpg)


## Deploy

Setting to deploy webhooks on Heroku.https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
