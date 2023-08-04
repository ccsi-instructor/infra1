

# Windowsの基本的なルーティングを設定する
---

## 概要
この演習では、Windows Serverのルーティングを手作業で設定します。
ルーティングテーブルに静的経路(Static Route)を作成するコマンドを実行し、新しいルーティングエントリを追加します。

Windows Server1では、2つのネットワーク(Network2とNetwork3)の経路情報として、Router1をNextHopに指定したStatic Routeを2つ作成します。

Windows Server2では、Network1の経路情報としてRouter1をNextHopに指定し、Network3の経路情報としてRouter2をNextHopに指定します。


## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください
[ppt]
- staticルートを構成し、Windows Serverからリモートネットワーク宛のルーティングを構成する


## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号
- Windows Server1: WSrv1-yyMMddX (年月日とPod番号)
- Windows Server2: WSrv2-yyMMddX (年月日とPod番号)
- Windows Client: WinClient
- Router1: CSR1
- Router2: CSR2
- Network1: 10.X.1.0/24
- Network2: 10.X.2.0/24
- Network3: 10.X.3.0/24


## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---

## 1. Windows Server1のStatic Routeを作成する

1. Windows Server1の管理画面に接続する  
<kbd>![img](image/03/11.png)</kbd>
1. [スタートメニュー]を右クリックし、コンテキストメニュー内の[Windows PowerShell(管理者)]をクリックする  
<kbd>![img](image/03/12.png)</kbd>
1. [ユーザー アカウント制御]のポップアップで[はい]をクリックする  
<kbd>![img](image/03/13.png)</kbd>
1. Windows PowerShellのウィンドウが表示されたことを確認する  
<kbd>![img](image/03/14.png)</kbd>
1. 以下のコマンドを実行し、Windows Server1に接続していることを確認する  
    ＞ ***hostname***  
<kbd>![img](image/03/15.png)</kbd>
    
    > 【補足】
    > hostnameコマンドはコンピュータの名前を表示します。
    > 複数のWindowsコンピュータを操作する環境において、操作対象のコンピュータを取り違えるトラブルを予防するのに効果的です。
     Windows Server1のコンピュータ名には、"WSrv1-"という接頭辞がつけられています。
    
1. 以下のコマンドを実行し、Windows Server1のStatic Routeを作成する  
    ＞ ***route add -p 10.X.2.0 mask 255.255.255.0 10.X.1.254***  
    ＞ ***route add -p 10.X.3.0 mask 255.255.255.0 10.X.1.254***
<kbd>![img](image/03/16.png)</kbd>
    > 【補足1】
    > route addコマンドは、WindowsコンピュータにStatic Routeを作成します。
    > 以下の書式でパラメータを指定します。
    > route add <ネットワークアドレス> mask <サブネットマスク> <ネクストホップ>

    > 【補足2】
    > このコマンドで作成したStatic RouteはOSの再起動により削除される一時的な設定です。
    > "-p"オプションを付与することで永続的(Permanent)な設定として保存されます。

---

## 2. Windows Server1のStatic Routeを確認する

1. Windows Server1のWindows PowerShellで以下のコマンドを実行し、Windows Server1のルーティングテーブルを確認する 
    ＞ ***route print***  
<kbd>![img](image/03/17.png)</kbd>
    > 【確認ポイント】
    > [アクティブ ルート]として、10.X.2.0宛と10.X.3.0宛のルーティングエントリ行が作成されており、NextHop(ゲートウェイ)としてRouter1のIPアドレス(10.X.1.254)が指定されていることを確認します。
    > [固定ルート]としても、同じルーティング情報が登録されています。
1. 以下のコマンドを実行し、Windows Server1からNetwork2宛とNetwork3宛の疎通を確認する  
    ＞ ***ping 10.X.2.254 -S 10.X.1.104***  
    ＞ ***ping 10.X.3.254 -S 10.X.1.104***  
<kbd>![img](image/03/22.png)</kbd>
    > 【補足】
    > "-S"オプションを付与することで、ping送信時の送信元IPアドレスを指定できます。
1. 以下のコマンドを実行し、Windows Server1からNetwork2宛とNetwork3宛の経路を確認する  
    ＞ ***tracert 10.X.2.254***  
    ＞ ***tracert 10.X.3.254***  
<kbd>![img](image/03/23.png)</kbd>
    > 【確認ポイント】
    > route addコマンドでNextHopとして指定した10.X.1.254(Router1)を経由して宛先まで通信していることを確認する。

---

## 3. Windows Server2のStatic Routeを作成する

1. Windows Server2の管理画面に接続する  
<kbd>![img](image/03/31.png)</kbd>
1. [スタートメニュー]を右クリックし、コンテキストメニュー内の[Windows PowerShell(管理者)]をクリックする  
1. [ユーザー アカウント制御]のポップアップで[はい]をクリックする  
1. Windows PowerShellのウィンドウが表示されたことを確認する  
1. 以下のコマンドを実行し、Windows Server2に接続していることを確認する  
    ＞ ***hostname***  
<kbd>![img](image/03/32.png)</kbd>
    > 【補足】
    > Windows Server1のコンピュータ名には、"WSrv2-"という接頭辞がつけられています。
1. 以下のコマンドを実行し、Windows Server2のStatic Routeを作成する  
    ＞ ***route add -p 10.X.1.0 mask 255.255.255.0 10.X.2.253***  
    ＞ ***route add -p 10.X.3.0 mask 255.255.255.0 10.X.2.254***
<kbd>![img](image/03/33.png)</kbd>
    > 【学習のポイント】
    > 演習ガイドのNetwork構成図も参照し、宛先ネットワークごとのNextHopに注目してください。
    > Windows Server2がNetwork1(10.X.1.0/24)と通信するためのNextHopはRouter1(10.X.2.253)ですが、Network3(10.X.3.0/24)と通信するためのNextHopはRouter2(10.X.2.254)です。

---

## 4. Windows Server2のStatic Routeを確認する

1. Windows Server2のWindows PowerShellで以下のコマンドを実行し、Windows Server2のルーティングテーブルを確認する 
    ＞ ***route print***  
<kbd>![img](image/03/41.png)</kbd>
    > 【確認ポイント】
    > [アクティブ ルート]として、以下のルーティングエントリが存在することを確認します。
    > ・ 10.X.1.0宛のNextHop(ゲートウェイ)としてRouter1のIPアドレス(10.X.1.253)が指定されている
    > ・ 10.X.3.0宛のNextHop(ゲートウェイ)としてRouter2のIPアドレス(10.X.1.254)が指定されている
    > [固定ルート]としても、同じルーティング情報が登録されています。
1. 以下のコマンドを実行し、Windows Server2からNetwork1宛とNetwork3宛の疎通を確認する  
    ＞ ***ping 10.X.1.254 -S 10.X.2.105***  
    ＞ ***ping 10.X.3.254 -S 10.X.2.105***  
<kbd>![img](image/03/42.png)</kbd>
    > 【補足】
    > "-S"オプションを付与することで、ping送信時の送信元IPアドレスを指定できます。
1. 以下のコマンドを実行し、Windows Server2(10.X.2.105)からWindows Server1(10.X.1.104)宛の経路を確認する  
    ＞ ***ping 10.X.1.104 -S 10.X.2.105*** 
    ＞ ***tracert 10.X.1.104***  
<kbd>![img](image/03/43.png)</kbd>
    > 【学習のポイント】
    > 別サブネットのIPアドレスと通信するためには、L3デバイスによるルーティングが必要です。
    > 今回の環境では、Router1が2つのネットワーク(10.X.1.0/24と10.X.2.0/24)を相互に接続しています。
    > Windows Server1とWindows Server2は、Router1をNextHopとするStatic Routeを構成したため、相互に通信できる状態です。



---
