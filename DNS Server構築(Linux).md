
# Linux ServerでDNSサーバーを構築する

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号  
- Windows DNSサーバー役: WinSrv1(WSrv1-yyMMddX)  
    - example.local ゾーンの権威サーバーとして、"sub.example.local" ゾーンをLinux1に委譲する    
    - Linux2にDNS問い合わせをフォワーディングする  

- Linux DNSサーバー役: Linux2(WSrv2-yyMMddX)  
    - example.comゾーンの権威サーバー   

- クライアント デスクトップ環境: WinClient(WC1-yyMMddX)

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---


## Linux Server(Linux)にBINDをインストールする

1. Linux2にBINDをインストールする  


## BINDを構成する  

## ゾーンファイルを作成する  

## サービスの起動を確認する  


## DNSフォワーディングを構成する  
1.1 

## ACLを構成する
NW1からは受け付けるが、NW2からは受け付けない






# レコード変更とキャッシュ削除
CSRのレコード変更でいいかな
フォワーディングしてからのほうがいいかな




---  

## 演習完了  
ここまでの手順で、以下の項目を学習できました。  
- [x] Windows DNSサーバーにDNSレコードを登録する  
- [x] セカンダリDNSサーバーを構成する  

- [x] (オプション) Linux DNSでACLを実装する  
- [x] 再帰問い合わせを実装する

