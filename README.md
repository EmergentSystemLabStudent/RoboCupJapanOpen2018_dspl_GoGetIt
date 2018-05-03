
# Go Get It

### Overview  

Go get it task for Duckers2018 in RoboCup Japan Open 

URL : https://emlab.jimdo.com/multimedia/ 

Training Phaseにおいて，ロボットが自律移動しながら地図生成を行い，その後オペレータをFollow meしながら，場所の名前情報を教示してもらうことで，マルチモーダル情報から場所のカテゴリゼーションを行う． 

Test Phaseでは，命令文から場所の名前情報を取り出し，その場所の名前が表す場所のカテゴリの尤度に基づいて場所のカテゴリを特定し，その場所のカテゴリが持つガウス分布に基づいて移動先を決定する．

### Description

###### Start

1. `roslaunch em_go_get_it em_go_get_it.launch` 

2. `roslaunch as_julius_english as_julius_english.launch` 

