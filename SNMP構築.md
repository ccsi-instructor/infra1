# SNMPによる監視環境を構築する  

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号  
- SNMPマネージャー役: Linux1
- SNMPエージェント役: Router1

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---


# Net-SNMPの構成準備をする  

1. Linux1の管理画面に接続する  

1. Net-SNMPをインストールする  

    ＞ ***sudo yum install net-snmp***  


    <details>
    <summary>[参考]yum install net-snmp ログ全文:</summary>  

    ```     
    [admin@linux1 ~]$ sudo yum install net-snmp
    Loaded plugins: langpacks
    base-openlogic                                                                                                                                                   | 3.1 kB  00:00:00     
    extras-openlogic                                                                                                                                                 | 2.5 kB  00:00:00     
    updates-openlogic                                                                                                                                                | 2.6 kB  00:00:00     
    base                                                                                                                                                             | 3.6 kB  00:00:00     
    docker-ce-stable                                                                                                                                                 | 3.5 kB  00:00:00     
    extras                                                                                                                                                           | 2.9 kB  00:00:00     
    openlogic                                                                                                                                                        | 2.9 kB  00:00:00     
    updates                                                                                                                                                          | 2.9 kB  00:00:00     
    (1/3): docker-ce-stable/7/x86_64/primary_db                                                                                                                      | 118 kB  00:00:00     
    (2/3): updates/7/x86_64/primary_db                                                                                                                               |  24 MB  00:00:00     
    (3/3): updates-openlogic/7/x86_64/primary_db                                                                                                                     |  24 MB  00:00:00     
    Resolving Dependencies
    --> Running transaction check
    ---> Package net-snmp.x86_64 1:5.7.2-49.el7_9.3 will be installed
    --> Processing Dependency: net-snmp-libs = 1:5.7.2-49.el7_9.3 for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: net-snmp-agent-libs = 1:5.7.2-49.el7_9.3 for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: perl(Data::Dumper) for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: libnetsnmptrapd.so.31()(64bit) for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: libnetsnmpmibs.so.31()(64bit) for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: libnetsnmpagent.so.31()(64bit) for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Processing Dependency: libnetsnmp.so.31()(64bit) for package: 1:net-snmp-5.7.2-49.el7_9.3.x86_64
    --> Running transaction check
    ---> Package net-snmp-agent-libs.x86_64 1:5.7.2-49.el7_9.3 will be installed
    ---> Package net-snmp-libs.x86_64 1:5.7.2-49.el7_9.3 will be installed
    ---> Package perl-Data-Dumper.x86_64 0:2.145-3.el7 will be installed
    --> Finished Dependency Resolution

    Dependencies Resolved

    ========================================================================================================================================================================================
    Package                                         Arch                               Version                                         Repository                                     Size
    ========================================================================================================================================================================================
    Installing:
    net-snmp                                        x86_64                             1:5.7.2-49.el7_9.3                              updates-openlogic                             325 k
    Installing for dependencies:
    net-snmp-agent-libs                             x86_64                             1:5.7.2-49.el7_9.3                              updates-openlogic                             707 k
    net-snmp-libs                                   x86_64                             1:5.7.2-49.el7_9.3                              updates-openlogic                             752 k
    perl-Data-Dumper                                x86_64                             2.145-3.el7                                     base-openlogic                                 47 k

    Transaction Summary
    ========================================================================================================================================================================================
    Install  1 Package (+3 Dependent packages)

    Total download size: 1.8 M
    Installed size: 5.9 M
    Is this ok [y/d/N]: y
    Downloading packages:
    (1/4): net-snmp-5.7.2-49.el7_9.3.x86_64.rpm                                                                                                                      | 325 kB  00:00:00     
    (2/4): net-snmp-agent-libs-5.7.2-49.el7_9.3.x86_64.rpm                                                                                                           | 707 kB  00:00:00     
    (3/4): net-snmp-libs-5.7.2-49.el7_9.3.x86_64.rpm                                                                                                                 | 752 kB  00:00:00     
    (4/4): perl-Data-Dumper-2.145-3.el7.x86_64.rpm                                                                                                                   |  47 kB  00:00:00     
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Total                                                                                                                                                   4.3 MB/s | 1.8 MB  00:00:00     
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
    Installing : 1:net-snmp-libs-5.7.2-49.el7_9.3.x86_64                                                                                                                              1/4 
    Installing : 1:net-snmp-agent-libs-5.7.2-49.el7_9.3.x86_64                                                                                                                        2/4 
    Installing : perl-Data-Dumper-2.145-3.el7.x86_64                                                                                                                                  3/4 
    Installing : 1:net-snmp-5.7.2-49.el7_9.3.x86_64                                                                                                                                   4/4 
    Verifying  : perl-Data-Dumper-2.145-3.el7.x86_64                                                                                                                                  1/4 
    Verifying  : 1:net-snmp-libs-5.7.2-49.el7_9.3.x86_64                                                                                                                              2/4 
    Verifying  : 1:net-snmp-5.7.2-49.el7_9.3.x86_64                                                                                                                                   3/4 
    Verifying  : 1:net-snmp-agent-libs-5.7.2-49.el7_9.3.x86_64                                                                                                                        4/4 

    Installed:
    net-snmp.x86_64 1:5.7.2-49.el7_9.3                                                                                                                                                    

    Dependency Installed:
    net-snmp-agent-libs.x86_64 1:5.7.2-49.el7_9.3                    net-snmp-libs.x86_64 1:5.7.2-49.el7_9.3                    perl-Data-Dumper.x86_64 0:2.145-3.el7                   

    Complete!
    [admin@linux1 ~]$ 
    ```

    </details>

    <!--
    detailsタグを使用する際は、3連バッククォートとの間にスペースなしの完全な空行を挿入する必要がある
    -->


1. Net-SNMPがインストールされたことを確認する  

    ＞ ***yum list installed | grep net-snmp***  


    ```
    [admin@linux1 ~]$ yum list installed | grep net-snmp
    net-snmp.x86_64                1:5.7.2-49.el7_9.3             @updates-openlogic
    net-snmp-agent-libs.x86_64     1:5.7.2-49.el7_9.3             @updates-openlogic
    net-snmp-libs.x86_64           1:5.7.2-49.el7_9.3             @updates-openlogic
    [admin@linux1 ~]$ 
    ```


1. Net-SNMP(snmpd)サービスがまだ起動していないことを確認する  
    ＞ ***systemctl status snmpd***  

    ```  
    [admin@linux1 ~]$ systemctl status snmpd
    ● snmpd.service - Simple Network Management Protocol (SNMP) Daemon.
    Loaded: loaded (/usr/lib/systemd/system/snmpd.service; disabled; vendor preset: disabled)
    Active: inactive (dead)
    [admin@linux1 ~]$ 
    ```  

    > 【確認ポイント】  
    > 'Active:' が 'inactive (dead)'であることを確認する  
    - [x] Net-SNMP(snmpd)が、サービスとして認識されていること  
    - [x] Net-SNMP(snmpd)サービスが、まだ起動していないこと  


1. Net-SNMP Utilsをインストールする  

    ＞ ***sudo yum install net-snmp-utils***  

    <details>
    <summary>[参考]yum install net-snmp-utils ログ全文:</summary>  
    ```
    [admin@linux1 ~]$ sudo yum install net-snmp-utils
    Loaded plugins: langpacks
    Resolving Dependencies
    --> Running transaction check
    ---> Package net-snmp-utils.x86_64 1:5.7.2-49.el7_9.3 will be installed
    --> Finished Dependency Resolution

    Dependencies Resolved

    ========================================================================================================================================================================================
    Package                                     Arch                                Version                                           Repository                                      Size
    ========================================================================================================================================================================================
    Installing:
    net-snmp-utils                              x86_64                              1:5.7.2-49.el7_9.3                                updates-openlogic                              201 k

    Transaction Summary
    ========================================================================================================================================================================================
    Install  1 Package

    Total download size: 201 k
    Installed size: 408 k
    Is this ok [y/d/N]: y
    Downloading packages:
    net-snmp-utils-5.7.2-49.el7_9.3.x86_64.rpm                                                                                                                       | 201 kB  00:00:00     
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
    Installing : 1:net-snmp-utils-5.7.2-49.el7_9.3.x86_64                                                                                                                             1/1 
    Verifying  : 1:net-snmp-utils-5.7.2-49.el7_9.3.x86_64                                                                                                                             1/1 

    Installed:
    net-snmp-utils.x86_64 1:5.7.2-49.el7_9.3                                                                                                                                              

    Complete!
    [admin@linux1 ~]$ 
    ```
    </details>

1. Net-SNMP Utilsがインストールされたことを確認する  

    ＞ ***yum list installed | grep net-snmp-utils***  

    ```
    [admin@linux1 ~]$ yum list installed | grep net-snmp-utils
    net-snmp-utils.x86_64          1:5.7.2-49.el7_9.3             @updates-openlogic
    [admin@linux1 ~]$ 
    ```

---


# Net-SNMPを構成する  

1. Net-SNMP("/etc/snmp/snmpd.conf")のバックアップを作成する  
    ＞ ***sudo cp /etc/named.conf /etc/named.conf.bak***  

    ```
    [admin@linux1 ~]$ sudo cp /etc/snmp/snmpd.conf /etc/snmp/snmpd.conf.bak 
    ```






---

# 演習完了  
ここまでの手順で、以下の項目を学習できました。  
- [x] rsyslogを構成して、Syslogサービスを提供する   
- [x] IOS-XEのloggingを構成して、Syslogサーバーにログを保存する  
- [x] (オプション)パケットフィルタのACLルールを修正する  
- [x] (オプション)loggerでSyslogの動作を確認する  




