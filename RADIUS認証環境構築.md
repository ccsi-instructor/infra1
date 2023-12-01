# RADIUS認証環境を構築する  

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号  
- RADIUSサーバー役: WinSrv2(WSrv2-yyMMddX)
- ユーザー データベース役(Active Directory ドメインコントローラー): WinSrv1(WSrv1-yyMMddX)  
- RADIUSクライアント役: Router2  
- ユーザー: WinClient(WC1-yyMMddX)  

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---


## RADIUS用のActive Directoryユーザーグループを作成する  

1. Active Directory サーバー(WinSrv1)の管理画面に接続する  
1. Active Directoryユーザー 管理コンソール("Active Directoryユーザーとコンピューター")を起動する  
1. [Active Directory ユーザーとコンピューター]-[example.local]-[Groups]に、新しいActive Directory ユーザーグループ(G_NwAdmins)を以下のパラメータで作成する  

    | 項目 | パラメータ |
    | :----- | :----- |
    | グループ名 | G_NwAdmins |
    | グループ名(Windows2000より以前) | G_NwAdmins |

    グループのスコープ:  
    - [ ] ドメイン ローカル  
    - [x] グローバル  
    - [ ] ユニバーサル  

    グループの種類:  
    - [x] セキュリティ  
    - [ ] 配布  

    > 【注意】  
    > "G_NwAdmins"グループのスコープは "グローバル" を選択します  

1. 作成した"G_NwAdmins"グループのメンバーとして、Active Directoryユーザーの"Tom"を追加する  

1. [Active Directory ユーザーとコンピューター]-[example.local]-[Groups]に、新しいActive Directory ユーザーグループ(DL_Router_RemoteConnect)を以下のパラメータで作成する  

    | 項目 | パラメータ |
    | :----- | :----- |
    | グループ名 | DL_Router_RemoteConnect |
    | グループ名(Windows2000より以前) | DL_Router_RemoteConnect |

    グループのスコープ:  
    - [x] ドメイン ローカル  
    - [ ] グローバル  
    - [ ] ユニバーサル  

    グループの種類:  
    - [x] セキュリティ  
    - [ ] 配布  


    > 【注意】  
    > "DL_Router_RemoteConnect"グループのスコープは "ドメインローカル" を選択します   

1. 作成した"DL_Router_RemoteConnect"グループのメンバーとして、Active Directoryグループの"G_NwAdmins"を追加する  

    > 【補足】
    > この演習では、Active DirectoryユーザーのTomがRouterに管理接続できるように構成します。  
    > 最終的に、以下のフローでTomのRouter管理接続が許可されます。  


    ```mermaid
    graph TD;
        TomがClientからRouterに管理接続-->RADIUSクライアントのRouter
        RADIUSクライアントのRouter-->RADIUSサーバーのネットワークポリシーサーバー;
        RADIUSサーバーのネットワークポリシーサーバー-->認証サーバーのActiveDirectory;
        認証サーバーのActiveDirectory-->DL_Router_RemoteConnectグループ;
        DL_Router_RemoteConnectグループ-->メンバーのG_NwAdminsグループ;
        メンバーのG_NwAdminsグループ-->メンバーのTomユーザー;
        メンバーのTomユーザー-->Tomの管理接続を許可する;
        
    ```




---   

## RADIUSサーバーの役割を追加  

1. RADIUSサーバー(WinSrv2)の管理画面に接続する  

1. 役割と機能の追加ウィザードを開始する  
    1. [スタートメニュー]をクリックする  
    1. スタートメニュー内の[サーバー マネージャー]をクリックし、サーバーマネージャを起動する    
    1. サーバーマネージャーのダッシュボード画面内の[役割と機能の追加]をクリックする   
    1. [役割と機能の追加ウィザード]ウィンドウが起動したことを確認する  

1. RADIUSサーバー("ネットワーク ポリシーとアクセス サービス")の役割を追加する
    1. [役割と機能の追加ウィザード]ウィンドウの[開始する前に]画面で、[次へ]をクリックする  
    1. [インストールの種類]画面で、[次へ]をクリックする  
    1. [サーバーの選択]画面で、[次へ]をクリックする  
    1. [サーバーの役割]画面で、以下のパラメータを選択する  

        - [x] ネットワーク ポリシーとアクセス サービス  

        > 【補足】  
        > "ネットワーク ポリシーとアクセス サービス"のチェックをつけると、[ネットワーク ポリシーとアクセス サービスに必要な機能を追加しますか？]の確認ポップアップが表示されます。  
        > [ネットワーク ポリシーとアクセス ービスに必要な機能を追加しますか？]ウィンドウで、[機能の追加] をクリックします。  

        <kbd>![img](image/18/001.png)</kbd> 

    1. [サーバーの役割]画面で、上のパラメータを選択したことを確認し、[次へ]をクリックする  
    1. [機能の選択]画面で、[次へ]をクリックする  
    1. [ネットワーク ポリシーとアクセス サービス]画面で、[次へ]をクリックする  
    1. [確認]画面で、[インストール]をクリックする  
    1. [結果]画面で、インストール進捗を示すプログレスバーが右端に到達するまで数分間待機する  
    1. [結果]画面で、インストールが正常に完了したことを確認し、[閉じる]をクリックする  
        <kbd>![img](image/18/002.png)</kbd> 

---  

## RADIUSクライアントをNPSに登録する    

1. ネットワーク ポリシー サーバー(NPS)管理コンソールを起動する  
    1. サーバーマネージャーウィンドウ右上の[ツール]をクリックする  
    1. メニュー内の[ネットワーク ポリシー サーバー]をクリックし、NPS管理コンソールを起動する  
        <kbd>![img](image/18/003.png)</kbd> 
    1. [ネットワーク ポリシー サーバー]管理コンソールが起動したことを確認する  
        <kbd>![img](image/18/004.png)</kbd> 

1. RADIUSクライアントを新規登録する  
    1. 左側コンソールツリーの[NPS(ローカル)]-[RADIUSクライアントとサーバー]-[RADIUSクライアント]をクリックする  
    1. [RADIUSクライアント]を右クリックし、コンテキストメニュー内の[新規]をクリックする  
        <kbd>![img](image/18/011.png)</kbd>  

    1. [新しいRADIUSクライアント]ウィンドウが表示されたことを確認する  
        <kbd>![img](image/18/012.png)</kbd>  

    1. [新しいRADIUSクライアント]ウィンドウで、以下のパラメータを入力する  

        - [x] このRADIUSクライアントを有効にする  

        - [ ] 既存のテンプレートを選択する    

        フレンドリ名:
        | Router2 | 
        | :----- | 

        アドレス(IPまたはDNS):
        | 10.X.2.254 | 
        | :----- | 

        既存の共有シークレット テンプレートを選択する:
        | なし | 
        | :----- | 

        - [x] 手動  
        - [ ] 生成     

        共有シークレット:
        | Pa\$\$w0rd | 
        | :----- | 

        共有シークレットの確認入力:
        | Pa\$\$w0rd | 
        | :----- | 

        <kbd>![img](image/18/013.png)</kbd>  

        <!--
        > 【補足】
        > アドレスはDNS名で指定することもできます。
        > 今回の演習では、Router2のどのインターフェイスからパケットが発信されるかを意識するため、IPアドレスを明示的に指定しています。
        -->


1. RADIUSクライアントの登録を確認する  

    1. [RADIUSクライアント]の一覧に、Router2の情報が追加されていることを確認する  
    
        <kbd>![img](image/18/014.png)</kbd>  


---  

## ネットワークポリシーを作成し、RADIUS認証を構成する      
 
1. 左側コンソールツリーの[NPS(ローカル)]-[ポリシー]-[ネットワーク ポリシー]をクリックする  
1. [ネットワーク ポリシー]を右クリックし、コンテキストメニュー内の[新規]をクリックする  
    <kbd>![img](image/18/021.png)</kbd>  

1. [新しいネットワーク ポリシー]ウィンドウが表示されたことを確認する  
    <kbd>![img](image/18/022.png)</kbd>  

1. [新しいネットワーク ポリシー]ウィンドウで、以下の手順の操作をする  

    1. [ネットワークポリシー名と接続の種類の指定]画面で、以下のパラメータを入力する  

        ポリシー名:  
        `Active Directory Authentication`   

        - [x] ネットワークアクセスサーバーの種類    
        `指定なし`   

        - [ ] ベンダー固有
        `10`   

        <kbd>![img](image/18/023.png)</kbd>  

    1. [ネットワークポリシー名と接続の種類の指定]画面で、[次へ]をクリックする  

    1. [条件の指定]画面で、[追加]をクリックする   
        <kbd>![img](image/18/024.png)</kbd>  
    1. [条件の選択]ウィンドウが表示されたことを確認する   
    1. [条件の選択]ウィンドウで、[ユーザーグループ]をクリックして選択する    
    1. [条件の選択]ウィンドウで、[追加]をクリックする  
        <kbd>![img](image/18/025.png)</kbd>  
    1. [ユーザーグループ]ウィンドウが表示されたことを確認する   
        <kbd>![img](image/18/026.png)</kbd>  
    1. [ユーザーグループ]ウィンドウで、[グループの追加]をクリックする  
    1. [グループの選択]ウィンドウが表示されたことを確認する   
        <kbd>![img](image/18/027.png)</kbd>  

    1. [グループの選択]ウィンドウで、以下のパラメータを入力する  

        選択するオブジェクト名を入力してください:  
        `DL_Router_RemoteConnect`
    
    1. [グループの選択]ウィンドウで、[名前の確認]をクリックする  
    1. [ネットワーク資格情報の入力]ウィンドウが表示されたことを確認する   
    1. [ネットワーク資格情報の入力]ウィンドウで、以下のパラメータを入力する  
        
        ユーザー名:  
        `Spike`  

        パスワード:  
        `Pa$$w0rd`

        <kbd>![img](image/18/028.png)</kbd>  


    1. [ネットワーク資格情報の入力]ウィンドウで、[OK]をクリックする    
    1. [グループの選択]ウィンドウで、[OK]をクリックする  
    1. [ユーザーグループ]ウィンドウで、[OK]をクリックする

        <kbd>![img](image/18/029.png)</kbd>  

    1. [条件の指定]画面で、[次へ]をクリックする  
        <kbd>![img](image/18/030.png)</kbd>  

    1. [アクセス許可の指定]画面で、[次へ]をクリックする  
        <kbd>![img](image/18/031.png)</kbd>  

    1. [認証方法の構成]画面で、以下のパラメータを選択する  
    
        EAPの種類:  
        `<空欄>`  

        セキュリティレベルの低い認証方法:  
        - [x] Microsoft暗号化認証バージョン 2 (MS-CHAP v2)   
            - [x] パスワードの期限が切れた後も、ユーザーにパスワードの変更を許可する   
        - [x] Microsoft暗号化認証 (MS-CHAP)   
            - [x] パスワードの期限が切れた後も、ユーザーにパスワードの変更を許可する  
        - [ ] 暗号化認証 (CHAP)  
        - [x] 暗号化されていない認証 (PAP、SAP)  
        - [ ] 認証方法をネゴシエートせずにクライアントに接続を許可する   
        
        <kbd>![img](image/18/032.png)</kbd>  
        
    1. [認証方法の構成]画面で、[次へ]をクリックする  

    1. [接続要求ポリシー]のポップアップで、[いいえ]をクリックする  

        <kbd>![img](image/18/033.png)</kbd>  

    1. [制約の構成]画面で、[次へ]をクリックする   

        <kbd>![img](image/18/034.png)</kbd>  

    1. [設定の構成]画面で、[次へ]をクリックする  

        <kbd>![img](image/18/035.png)</kbd>  

    1. [新しいネットワーク ポリシーの完了]画面で、[完了]をクリックする  

        <kbd>![img](image/18/036.png)</kbd>  

1. ネットワークポリシーを確認する  

    1. [ネットワーク ポリシー]の一覧に、[Active Directory Authentication]が追加されていることを確認する  
    
        <kbd>![img](image/18/037.png)</kbd>  

---   

## Cisco IOS-XEのAAAを構成し、RADIUS認証で管理ログインする  

1. Router2の管理画面に接続する   

1. 以下のコマンドを実行し、特権モードからグローバルコンフィギュレーションモードに遷移する  
    Router2# ***conf t***  

    ```
    CSR2#conf t
    Enter configuration commands, one per line.  End with CNTL/Z.
    CSR2(config)#
    ```

1. 以下のコマンドを実行し、RADIUSサーバー(WinSrv2)の接続情報を定義する     
    Router2(config)# ***radius server WINRADIUS***  
    Router2(config-radius-server)# ***address ipv4 10.X.2.105***    
    Router2(config-radius-server)# ***key Pa\$\$w0rd***   
    Router2(config-radius-server)# ***exit***   
    Router2(config)# ***exit***   

    ```
    CSR2(config)#radius server WINRADIUS
    CSR2(config-radius-server)#address ipv4 10.255.2.105
    CSR2(config-radius-server)#key Pa$$w0rd
    CSR2(config-radius-server)#exit
    CSR2(config)#
    ```


1. 以下のコマンドを実行し、IOS-XEのAAA(aaa new-model)機能を有効化する       
    Router2(config)# ***aaa new-model***   

    ```
    CSR2(config)#aaa new-model  
    ```

1. 以下のコマンドを実行し、AAAで使用するRADIUS サーバーのグループを構成する          
    Router2(config)# ***aaa group server radius RADIUSSERVERS***  
    Router2(config-sg-radius)# ***server name WINRADIUS***  
    Router2(config-sg-radius)# ***exit***  

    ```
    CSR2(config)#aaa group server radius RADIUSSERVERS
    CSR2(config-sg-radius)#server name WINRADIUS
    CSR2(config-sg-radius)#exit
    CSR2(config)#
    ```

1. 以下のコマンドを実行し、管理ログイン時に使用する認証方式を指定する           
    Router2(config)# ***aaa authentication login LOGINRADIUS group RADIUSSERVERS local***  
    
    ```
    CSR2(config)#aaa authentication login LOGINRADIUS group RADIUSSERVERS local 
    ```

    > 【補足】  
    > このコマンドでは、"LOGINRADIUS"という名称の認証プロファイルとして、以下の認証方式を指定しています。  
    > ① 管理ログイン時の認証方式として、RADIUSサーバー グループ(RADIUSSERVERS)を最優先で使用する  
    > ② ただし、RADIUSサーバーに接続できない場合は、ローカルユーザーDB(local)を使用する(フォールバック認証)    


1. 以下のコマンドを実行し、管理接続の通信プロトコルと認証方式を指定する             
    Router2(config)# ***line vty 14 15***  
    Router2(config-line)# ***transport input all***  
    Router2(config-line)# ***login authentication LOGINRADIUS***  
    Router2(config-line)# ***exit***  

     
    ```
    CSR2(config)#line vty 14 15
    CSR2(config-line)#transport input all
    CSR2(config-line)#login authentication LOGINRADIUS
    CSR2(config-line)#exit
    CSR2(config)#
    ```

    > 【補足】
    > 演習環境のIOS-XEには、0から20までの仮想端末回線(vty)が設けられています。    
    > そのうちの一部(14から15まで)の設定を変更します。    
    > 管理接続プロトコルとしてall(SSHとTelnet)を許可し、接続時の認証方式としてLOGINRADIUSを採用します。    
    > なお、この後の動作確認においては、作業の混乱を避けるためにTelnetを使用してRouterに管理接続します。  

---  

# RAIDUS認証の動作を確認する  

1. Clientでターミナルソフト(Teraterm)を起動する    
    1. 操作コンピュータを変更するため、演習環境のトップページに戻る  
    1. Windows Client(WinClient)の管理画面に "admin" で接続する   
    1. [スタートメニュー]-[T]-[Tera Term]-[Tera Term]をクリックする  
        <kbd>![img](image/18/051.png)</kbd>  
    1. [Tera Term]が起動されたことを確認する  
        <kbd>![img](image/18/052.png)</kbd>  

1. Router2にTelnetで接続し、RADIUS認証が成功することを確認する     

    1. [Tera Term:新しい接続]ポップアップで以下のパラメータを入力する

        - [x] TCP/IP  
            ホスト:
            `10.X.2.254`

            - [x] ヒストリ

            サービス:
            - [x] Telnet  
            - [ ] SSH  
            - [ ] その他

            TCPポート番号:
            `23`

            SSHバージョン:
            `SSH2`

            IPバージョン:
            `AUTO`

        - [ ] シリアル  
            ポート:
            `COM2 CoOmmunications Port(COM2)`

        <kbd>![img](image/18/053.png)</kbd>  

    1. [Tera Term:新しい接続]ポップアップで[OK]をクリックする  
    1. Telnet接続のための認証プロンプトが表示されたことを確認する  
        <kbd>![img](image/18/054.png)</kbd>  

    1. Telnet接続の認証情報としてTomのユーザー名とパスワードを入力する    
        

        User Access Verification    
        username: ***Tom***    
        Password: ***Pa\$\$w0rd***

    1. Router2に接続できたことを確認する  

        <kbd>![img](image/18/055.png)</kbd>  

1. 特権モードで操作する認可がないことを確認する
    1. Tera Termのプロンプトで以下のコマンドを実行し、特権モードに遷移できないことを確認する  

        Router2> ***enable***  
        
        ```
        CSR2>enable
        % Error in authentication.

        CSR2>
        ```

        > 【補足】  
        > 管理接続開始時は、ユーザーモード状態です。ユーザーモードは管理操作を実行できません。  
        > ユーザーモード状態でenableコマンドを実行することで、特権モードに遷移できます。  
        > しかし、この時点ではRADIUS認証後の認可をまだ構成していないため、Tomはenableコマンドで特権モードにログインできません。
        > この後の演習手順を進めることで、特権モードにログインできるようになります。


        <kbd>![img](image/18/056.png)</kbd>  


---  

## ネットワークポリシーを編集し、RADIUS認可を構成する     

1. RADIUSサーバー(WinSrv2)の管理画面に接続する  

1. ネットワーク ポリシー サーバー(NPS)管理コンソールを起動する  

1. 左側コンソールツリーの[NPS(ローカル)]-[ポリシー]-[ネットワーク ポリシー]をクリックする  

1. 右側ペインのネットワーク ポリシー一覧の[Active Directory Authentication]を右クリックし、コンテキストメニュー内の[プロパティ]をクリックする  
    <kbd>![img](image/18/061.png)</kbd>  

1. [Active Directory AUthenticationのプロパティ]ウィンドウが表示されたことを確認する  

    <kbd>![img](image/18/063.png)</kbd>  

1. [設定]タブをクリックして選択する  

1. [RADIUS属性]-[標準]をクリックして選択する  

1. "属性:"欄の[Service-Type]をクリックして選択し、[編集]をクリックする  

    <kbd>![img](image/18/081.png)</kbd>  

1. [属性の情報]ウィンドウが表示されたことを確認する  

    <kbd>![img](image/18/082.png)</kbd>  

1. [属性の情報]ウィンドウで、以下のパラメータを選択する  

    - [ ] ダイヤルアップまたはVPNで一般的に使用する  
    - [ ] 802.1Xで一般的に使用する  
    - [x] その他
        `Adminitrative`

    <kbd>![img](image/18/083.png)</kbd>  

1. [属性の情報]ウィンドウで、[OK]をクリックする    

1. "属性:"欄の[Service-Type]の値が "Adminitrative" であることを確認する  

    <kbd>![img](image/18/084.png)</kbd>  

1. [RADIUS属性]-[ベンダー固有]をクリックして選択し、[追加]をクリックする  
    <kbd>![img](image/18/062.png)</kbd>  

1. [ベンダー固有の属性の追加]ウィンドウが表示されたことを確認する  

    <kbd>![img](image/18/064.png)</kbd> 

1. [ベンダー固有の属性の追加]ウィンドウで、以下のパラメータを選択する  

    ベンダー(V):
    `Cisco`

    <kbd>![img](image/18/065.png)</kbd> 

1. [ベンダー固有の属性の追加]ウィンドウで、以下のパラメータをクリックして選択する  

    属性:
    `Cisco-AV-Pair    Cisco`

    <kbd>![img](image/18/066.png)</kbd> 

1. [ベンダー固有の属性の追加]ウィンドウで、[追加]をクリックする  

1. [属性の情報]ウィンドウが表示されたことを確認する  

    <kbd>![img](image/18/067.png)</kbd> 

1. [属性の情報]ウィンドウで、[追加]をクリックする  

1. [属性の情報]ウィンドウが表示されたことを確認する  

    <kbd>![img](image/18/068.png)</kbd> 

1. [属性の情報]ウィンドウで、以下のパラメータを入力する  

    属性値:  
    `shell:priv-lvl=15`

    > 【補足】
    > このRADIUS属性値は、ログイン認証後の管理操作(SHell)における権利レベル(Privilege Level)が、特権モード(15)であることを意味します。  

    <kbd>![img](image/18/069.png)</kbd>     

1. [属性の情報]ウィンドウで、[OK]をクリックする  

1. [属性の情報]ウィンドウで、属性値が追加されていることを確認し、[OK]をクリックする  

    <kbd>![img](image/18/070.png)</kbd>  

1. [ベンダー固有の属性の追加]ウィンドウで、属性値が追加されていることを確認し、[閉じる]をクリックする  

    <kbd>![img](image/18/071.png)</kbd>  

1. [Active Directory AUthenticationのプロパティ]ウィンドウで、属性が追加されていることを確認し、[OK]をクリックする  

    <kbd>![img](image/18/072.png)</kbd>  




---   

## Cisco AAAのRADIUS認可を構成し、Active DirecotryユーザーTomの特権モード アクセスを許可する    

1. Router2の管理画面に接続する   

1. 以下のコマンドを実行し、特権モードからグローバルコンフィギュレーションモードに遷移する  
    Router2# ***conf t***  

    ```
    CSR2#conf t
    Enter configuration commands, one per line.  End with CNTL/Z.
    CSR2(config)#
    ```

1. 以下のコマンドを実行し、管理ログイン時に使用する認証方式を指定する           
    Router2(config)# ***aaa authorization exec EXECRADIUS group RADIUSSERVERS local ***  
    
    ```
    CSR2(config)#aaa authorization exec EXECRADIUS group RADIUSSERVERS local
    ```

    > 【補足】  
    > このコマンドでは、"EXECRADIUS"という名称の認可プロファイルを構成しています。    
    > ① ログイン認証後に与える認可レベルの決定方式として、RADIUSサーバー グループ(RADIUSSERVERS)を最優先で使用する  
    > ② ただし、RADIUSサーバーに接続できない場合は、ローカルユーザーDB(local)を使用する    

1. 以下のコマンドを実行し、管理接続時の認可方式を指定する        
    Router2(config)# ***line vty 14 15***  
    Router2(config-line)# ***authorization exec EXECRADIUS***  
    Router2(config-line)# ***exit***  

     
    ```
    CSR2(config)#line vty 14 15
    CSR2(config-line)#authorization exec EXECRADIUS
    CSR2(config-line)#exit
    CSR2(config)#
    ```


---  

# RAIDUS認証と認可の動作を確認する  

1. Clientでターミナルソフト(Teraterm)を起動する    
    1. 操作コンピュータを変更するため、演習環境のトップページに戻る  
    1. Windows Client(WinClient)の管理画面に "admin" で接続する   
    1. [スタートメニュー]-[T]-[Tera Term]-[Tera Term]をクリックする  
    1. [Tera Term]が起動されたことを確認する  


1. Router2にTelnetで接続し、RADIUS認証が成功することを確認する     

    1. [Tera Term:新しい接続]ポップアップで以下のパラメータを入力する

        - [x] TCP/IP  
            ホスト:
            `10.X.2.254`

            - [x] ヒストリ

            サービス:
            - [x] Telnet  
            - [ ] SSH  
            - [ ] その他

            TCPポート番号:
            `23`

            SSHバージョン:
            `SSH2`

            IPバージョン:
            `AUTO`

        - [ ] シリアル  
            ポート:
            `COM2 CoOmmunications Port(COM2)`

        <kbd>![img](image/18/053.png)</kbd>  

    1. [Tera Term:新しい接続]ポップアップで[OK]をクリックする  
    1. Telnet接続のための認証プロンプトが表示されたことを確認する  
        <kbd>![img](image/18/054.png)</kbd>  

    1. Telnet接続の認証情報としてTomのユーザー名とパスワードを入力する    
        

        User Access Verification    
        username: ***Tom***    
        Password: ***Pa\$\$w0rd***

    1. Router2に接続できたことを確認する  

        <kbd>![img](image/18/091.png)</kbd>  

1. 特権モードでログインしていることを確認する  

    1. 以下のコマンドを実行し、特権モード(privilege level 15)でログインしていることを確認する  
        Router2# ***show privilege***  

        ```
        CSR2#show privilege
        Current privilege level is 15
        CSR2#
        ```

        <kbd>![img](image/18/092.png)</kbd>  

    1. 以下のコマンドを実行し、特権モードの管理操作(config保存)が実行できることを確認する  

        Router2# ***write***  

        ```
        CSR2#write
        Building configuration...
        [OK]
        CSR2#
        ```

        <kbd>![img](image/18/093.png)</kbd>  



<!--
> 【補足1】
> トラブルシュートに使用できるIOSコマンドは以下のとおりです。
> # debug aaa authorization
> # debug aaa authentication
> # debug radius
> # terminal monitor
 
> 【補足2】
> aaaのMethod(プロファイル)は、内部的にIDで識別されています。
> そのため、同じ名前のaaa authorizationコマンドを複数回実行すると、line vtyとの紐づけに齟齬が生じる恐れがあります。
> 対処方法:
> line vty 14 15
>   no authorization exec EXECRADIUS
>   authorization exec EXECRADIUS
-->




---

## 演習完了  
ここまでの手順で、以下の項目を学習できました。
- [x] WindowsのネットワークポリシーサーバーでRADIUSサーバーを構築する  
- [x] Cisco IOS-XEのAAAを設定し、RADIUS認証を構成する  
- [x] RADIUS属性を指定して、RADIUS認可を構成する  





