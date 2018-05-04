
# Go Get It

### Overview  

Go get it task for Duckers2018 in RoboCup Japan Open 

URL : https://emlab.jimdo.com/multimedia/ 

###### Training Phase 

DoorOpenによって競技がスタートすると，ロボットは田渕らのActiveSLAM[1]を用いて未知環境の地図生成を行う．ActiveSLAMはロボットが自律移動しながら地図生成を行う手法である．環境の地図が完成したら，ロボットはPerson Tracking（Follow me）を行い，オペレータの後をついて場所の名前情報を教示してもらう．ロボットは環境内で得たマルチモーダル情報を用い，石伏らの手法[2][3]に谷口らの手法[4]を組み合わせ，場所の名前情報・位置情報・画像情報を用いて場所のカテゴリゼーションを行う．石伏らの手法は画像情報と位置情報を用いて場所のカテゴリゼーションを行った手法であり，谷口らの手法は言語情報と位置情報から場所を表す名前と場所のカテゴリを同時に獲得する手法である． 

###### Test Phase 

命令文から場所の名前情報を取り出し，その場所の名前が表す場所のカテゴリの尤度に基づいて場所のカテゴリを特定し，その場所のカテゴリが持つガウス分布に基づいて移動先を決定する．

### Description

###### Start

1. `roslaunch em_go_get_it em_go_get_it.launch` 

2. `roslaunch as_julius_english as_julius_english.launch` 

### Paper

1. 田渕義基，谷口彰，萩原良信，谷口忠大：「家庭環境における移動ロボットの能動的地図生成と場所概念形成」第32回人工知能学会全国大会(JSAI2018)，2018年5月，名古屋．
2. 石伏智，谷口彰，萩原良信，高野敏明，谷口忠大「自己位置と高次特徴量を用いた教師なし場所領域学習」第30回人工知能学会全国大会(JSAI2016)，2016年5月，福岡，同上論文集，2I3-4. 
3. Satoshi Ishibushi, Akira Taniguchi, Toshiaki Takano, Yoshinobu Hagiwara and Tadahiro Taniguchi: “Statistical Localization Exploiting Convolutional Neural Network for an Autonomous Vehicle”, 41st Annual Conference of the IEEE Industrial Electronics Society (IECON’15), Nov. 9-12, 2015 in Yokohama (Japan). The proceedings of IECON’15, pp. 1369-1375. 
4. Akira Taniguchi, Tadahiro Taniguchi, and Tetsunari Inamura: “Spatial concept acquisition for a mobile robot that integrates self-localization and unsupervised word discovery from spoken sentences,” IEEE Transactions on Cognitive and Developmental Systems, vol. 8, no. 4, pp. 285–297, 2016.


