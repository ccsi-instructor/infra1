
# Linux ServerでDockerを操作する

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号  
- Dockerプラットフォーム役: Linux1     

- クライアント デスクトップ環境: WinClient(WC1-yyMMddX)


## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---

## Linux1にインストールされているDockerのバージョンを確認する  

1. Linux1の管理画面に接続する  

1. インストールされているDockerのバージョンを確認する   
    ＞ ***docker --version***  

    ```
    [admin@linux1 ~]$ docker --version
    Docker version 23.0.5, build bc4487a
    [admin@linux1 ~]$ 
    ```

    > 【補足】
    > 演習を円滑に進行するため、Linuxには事前にDockerがインストールされています。
    > インストールの手順については、本ページ末尾の参考資料を参照してください。



# Linux1はPython2環境であることを確認する
python
import sys
print(sys.version)

# pullする
docker pull python:3.11-alpine3.18


# alpineにログインする
docker run -it python:3.11-alpine3.18 /bin/ash

# alpineを起動してPythonを実行する
docker run -it python:3.11-alpine3.18

import sys
print(sys.version)


python3用のweb appを実行する
pipenvで


FROM python:alpine3.11



---  

## 演習完了  
ここまでの手順で、以下の項目を学習できました。  
- [x]   

## 参考資料
- Docker Engine インストール (CentOS 向け)
    - https://matsuand.github.io/docs.docker.jp.onthefly/engine/install/centos/

- Docker Hub
    - https://hub.docker.com/search?q=
