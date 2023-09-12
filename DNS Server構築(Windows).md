
# Windows ServerでDNSサーバーを構築する

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号
- Windows DNSサーバー役: WinSrv1(WSrv1-yyMMddX)
    - example.local ゾーンの権威サーバー(プライマリ)  
- Windows DNSサーバー役: WinSrv2(WSrv2-yyMMddX)
    - example.local ゾーンの権威サーバー(セカンダリ)  
    - sub.example.local ゾーンの権威サーバー

- クライアント デスクトップ環境: WinClient(WC1-yyMMddX)

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---

## Windows ServerでDNSサーバーを構築する   


## Wndows Server 1のDNSサーバーの状態を確認する
Active Directoryドメインコントローラー構築時に自動的にDNSサーバーの役割も追加されています。  
"example.local" Active Directoryドメインのサービスを提供するために、DNSサーバーには "example.local" DNSゾーンが構成されていることを確認します。  

1. DNSサーバー管理コンソールを起動する

    <!--
        Active DirectoryのセクションでDNSの学習を深堀しすぎるのを防止するために、Active Directory学習後にDNSを学習します。  
    -->

1. "example.local" ゾーンが作成されていることを確認する  
1. "example.local" ゾーンに登録されているDNSレコードを確認する  

## Windows Server 2にDNSサーバー役割をインストールする  
1. DNS サーバーの役割を追加する  

## DNSレコードを登録する  
- Web1
- Web2    
- File1 
- File2   
- Linux1  
- Linux2  
- DNS  
- AD  
- Client  
- CSR1  
- CSR2  

## Windows Server 2にDNSサーバー役割をインストールする  
1. "example.local" のセカンダリDNSサーバーとして構成する  

## 名前解決の動作を確認する  

1. nslookupで名前解決を問い合わせる  
1. セカンダリにも問い合わせる  
 


# 委譲を構成する
1. Windows Server 1で委譲する
1. Windows Server 2でゾーンをつくる （できるか？）

---  

## 演習完了  
ここまでの手順で、以下の項目を学習できました。  
- [x] Windows DNSサーバーにDNSレコードを登録する  
- [x] セカンダリDNSサーバーを構成する  

