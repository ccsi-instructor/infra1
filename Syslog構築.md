# Syslogによるログ管理環境を構築する  

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号  
- Syslogサーバー役: Linux1
- Syslogクライアント訳: Router1

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---


# rsyslogの構成準備をする  

1. Linux1の管理画面に接続する  

1. rsyslogが既定でインストールされていることを確認する 
    ＞ ***yum list installed | grep rsyslog***  

    ```
    [admin@linux1 ~]$ yum list installed | grep rsyslog
    rsyslog.x86_64                 8.24.0-57.el7_9.3              @updates          
    [admin@linux1 ~]$ 
    ```

1. Syslog(rsyslog)サービスのStatusを参照し、rsyslogがサービスとして認識されていることを確認する    
    ＞ ***systemctl status rsyslog***  

    ```
    [admin@linux1 ~]$ systemctl status rsyslog
    ● rsyslog.service - System Logging Service
    Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
    Active: active (running) since Fri 2023-12-01 01:23:08 UTC; 1h 27min ago
        Docs: man:rsyslogd(8)
            http://www.rsyslog.com/doc/
    Main PID: 1281 (rsyslogd)
        Tasks: 3
    Memory: 3.2M
    CGroup: /system.slice/rsyslog.service
            └─1281 /usr/sbin/rsyslogd -n

    Dec 01 01:23:06 linux1 systemd[1]: Starting System Logging Service...
    Dec 01 01:23:08 linux1 rsyslogd[1281]:  [origin software="rsyslogd" swVersion="8.24.0-57.el7_9.3" x-pid="1281" x-info="http://www.rsyslog.com"] start
    Dec 01 01:23:08 linux1 systemd[1]: Started System Logging Service.
    [admin@linux1 ~]$ 
    ```
1. rsyslogのログファイル保存先ディレクトリを作成する  
    ＞ ***sudo mkdir /var/log/rsyslog***  
    ＞ ***ls -la /var/log/rsyslog***  

    ```
    [admin@linux1 ~]$ sudo mkdir /var/log/rsyslog
    [admin@linux1 ~]$ ls -la /var/log/rsyslog
    total 4
    drwxr-xr-x   2 root root    6 Dec  1 07:14 .
    drwxr-xr-x. 12 root root 4096 Dec  1 07:14 ..
    [admin@linux1 ~]$ 
    ```

---  

# rsyslogの構成ファイルを編集する  

1. rsyslogの構成ファイル("/etc/rsyslog.conf")のバックアップを作成する  
    ＞ ***sudo cp /etc/rsyslog.conf /etc/rsyslog.conf.bak***  

1. rsyslogのconfigファイルを編集する       
    ＞ ***sudo vi /etc/rsyslog.conf ***  
    ＞ ***diff /etc/rsyslog.conf /etc/rsyslog.conf***  


    ```
    [admin@linux1 ~]$ sudo vi /etc/rsyslog.conf
    [admin@linux1 ~]$ diff /etc/rsyslog.conf /etc/rsyslog.conf.bak 
    15,16c15,16
    < $ModLoad imudp
    < $UDPServerRun 514
    ---
    > #$ModLoad imudp
    > #$UDPServerRun 514
    19,20c19,20
    < $ModLoad imtcp
    < $InputTCPServerRun 514
    ---
    > #$ModLoad imtcp
    > #$InputTCPServerRun 514
    47,48d46
    < $template perHostFile,"/var/log/rsyslog/%fromhost-ip%.log"
    < *.* ?perHostFile
    [admin@linux1 ~]$ 
    ```

1. rsyslogのconfigファイルの構成をチェックする        
    ＞ ***sudo rsyslogd -N 1***  


    ```
    [admin@linux1 ~]$ sudo rsyslogd -N 1
    rsyslogd: version 8.24.0-57.el7_9.3, config validation run (level 1), master config /etc/rsyslog.conf
    rsyslogd: End of config validation run. Bye.
    [admin@linux1 ~]$ 
    ```

    > 【確認ポイント】
    > "End of config validation run. Bye." と記述されていることを確認する  

---  

# rsyslogサービスを再起動する  

1. rsyslogサービスを起動する  
    ＞ ***sudo systemctl restart rsyslog***  

1. Syslog(rsyslog)サービスのStatusを参照し、rsyslogサービスが起動していることを確認する    
    ＞ ***systemctl status rsyslog***  

    ```
    [admin@linux1 ~]$ systemctl status rsyslog
    ● rsyslog.service - System Logging Service
    Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
    Active: active (running) since Fri 2023-12-01 01:23:08 UTC; 1h 27min ago
        Docs: man:rsyslogd(8)
            http://www.rsyslog.com/doc/
    Main PID: 1281 (rsyslogd)
        Tasks: 3
    Memory: 3.2M
    CGroup: /system.slice/rsyslog.service
            └─1281 /usr/sbin/rsyslogd -n

    Dec 01 01:23:06 linux1 systemd[1]: Starting System Logging Service...
    Dec 01 01:23:08 linux1 rsyslogd[1281]:  [origin software="rsyslogd" swVersion="8.24.0-57.el7_9.3" x-pid="1281" x-info="http://www.rsyslog.com"] start
    Dec 01 01:23:08 linux1 systemd[1]: Started System Logging Service.
    [admin@linux1 ~]$ 
    ```

    > 【確認ポイント】  
    > 'Active:' が 'active(running)'であることを確認する  
    - [x] rsyslogサービスが起動していること   

---  

# Router(IOS-XE)のsyslogを構成する  

1. Router1の管理画面に接続する   

1. 以下のコマンドを実行し、特権モードからグローバルコンフィギュレーションモードに遷移する  
    Router1# ***conf t***  

    ```
    CSR1#conf t
    Enter configuration commands, one per line.  End with CNTL/Z.
    CSR1(config)#
    ```



1. 以下のコマンドを実行し、Syslogメッセージの送信先サーバーをLinux1に指定する    
    Router1(config)# ***logging host 10.X.1.102***  

    ```
    CSR1(config)# logging host 10.255.1.102
    ```

1. 以下のコマンドを実行し、configを保存する    
    Router1(config)# ***end***  
    Router1# ***write***  

    ```
    CSR1(config)#end
    CSR1#write
    Building configuration...
    [OK]
    CSR1#
    ```

---  

# Router(IOS-XE)のsyslogの動作を確認する    

1. Router1の管理画面に接続する   

1. 以下のコマンドを実行し、Routerを再起動させることで、syslogメッセージを送信させる    
    Router1# ***reload***  

    ```
    CSR1#reload
    Proceed with reload?[confirm]   (←Enterキーを押下する)

    ```

1. Linux1の管理画面に接続する  

1. Router1のsyslogメッセージを保存するファイルが作成されていることを確認する     
    ＞ ***ls -la /var/log/rsyslog***

    ```
    [admin@linux1 ~]$ ls -la /var/log/rsyslog
    total 12
    drwxr-xr-x   2 root root   51 Dec  1 07:19 .
    drwxr-xr-x. 12 root root 4096 Dec  1 07:14 ..
    -rw-------   1 root root  526 Dec  1 07:23 10.255.1.254.log
    -rw-------   1 root root 1816 Dec  1 07:23 127.0.0.1.log
    [admin@linux1 ~]$ 
    ```

1. Router1のログファイルを参照し、再起動のログ(%SYS-5-RELOAD)が記録されていることを確認する  

    ＞ ***sudo tail -n 10 /var/log/rsyslog/10.X.1.254.log***

    ```
    [admin@linux1 ~]$ sudo tail -n 10 /var/log/rsyslog/10.255.1.254.log 
    Dec  1 07:19:02 csr1.internal.cloudapp.net 70: *Dec  1 07:19:01.625: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: trainocatenwadmin] [Source: 10.0.0.4] [localport: 22] at 07:19:01 UTC Fri Dec 1 2023
    Dec  1 07:22:34 csr1.internal.cloudapp.net 71: *Dec  1 07:22:33.712: %SYS-5-CONFIG_I: Configured from console by trainocatenwadmin on vty0 (10.0.0.4)
    Dec  1 07:23:15 csr1.internal.cloudapp.net 72: *Dec  1 07:23:14.576: %SYS-5-RELOAD: Reload requested by trainocatenwadmin on vty0 (10.0.0.4). Reload Reason: Reload Command.
    Dec  1 07:25:59 csr1.internal.cloudapp.net 64: *Dec  1 07:25:58.460: %PKI-2-NON_AUTHORITATIVE_CLOCK: PKI functions can not be initialized until an authoritative time source, like NTP, can be obtained.
    Dec  1 07:26:01 csr1.internal.cloudapp.net 65: *Dec  1 07:26:01.132: %DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet2 assigned DHCP address 10.255.2.253, mask 255.255.255.0, hostname CSR1
    Dec  1 07:26:03 csr1.internal.cloudapp.net 66: *Dec  1 07:26:01.427: %BGP-5-ADJCHANGE: neighbor 10.255.2.254 Up 
    Dec  1 07:26:12 csr1.internal.cloudapp.net 67: *Dec  1 07:26:10.687: %IM-6-IOX_ENABLEMENT: R0/0: ioxman: IOX is ready.
    Dec  1 07:26:15 csr1.internal.cloudapp.net 68: *Dec  1 07:26:15.839: %SMART_LIC-6-EXPORT_CONTROLLED: Usage of export controlled features is not allowed
    Dec  1 07:26:16 csr1.internal.cloudapp.net 69: *Dec  1 07:26:15.839: %CALL_HOME-6-CALL_HOME_ENABLED: Call-home is enabled by Smart Agent for Licensing.
    [admin@linux1 ~]$ 
    ```

---

# (オプション) Linux2からSyslogのテストメッセージを送信する  


1. Linux2からLinux1に通信できないことを確認する  

    1. Linux2の管理画面に接続する  

    1. Linux2からLinux1に通信できないことを確認する  
        ＞ ***ping 10.X.1.102 -c 4***  

        ```
        [admin@linux2 ~]$ ping 10.255.1.102 -c 4
        PING 10.255.1.102 (10.255.1.102) 56(84) bytes of data.
        From 10.255.3.254 icmp_seq=1 Packet filtered
        From 10.255.3.254 icmp_seq=2 Packet filtered
        From 10.255.3.254 icmp_seq=3 Packet filtered
        From 10.255.3.254 icmp_seq=4 Packet filtered

        --- 10.255.1.102 ping statistics ---
        4 packets transmitted, 0 received, +4 errors, 100% packet loss, time 3002ms

        [admin@linux2 ~]$ 
        ```

        > 【補足】
        > Router2のパケットフィルタによってFilterされているため、Linux1とLinux2の間で通信できない状態です。
        > 次の手順でパケットフィルタのルールを変更することで、通信できるようになります。


1. Router2の拡張ACL "ACL_PACKETFILTER" にLinux2からLinux1への通信を許可するルールを追加する

    1. Router2(CSR2)の管理画面に接続する  

    1. 拡張ACL "ACL_PACKETFILTER" の現在の状態を確認する  
        Router2# ***show ip access-list ACL_PACKETFILTER***  

        ```
        CSR2#show ip access-list ACL_PACKETFILTER
        Extended IP access list ACL_PACKETFILTER
            10 permit udp host 10.255.3.106 host 10.255.1.104 eq domain
            20 deny ip 10.255.3.0 0.0.0.255 10.255.1.0 0.0.0.255 time-range WEEKDAYS (active) (26 matches)
            30 permit tcp any host 10.255.2.105 eq www 443 1080
            99 deny ip any any log (158 matches)
        CSR2#
        ```

    1. 拡張ACL "ACL_PACKETFILTER" にLinux2からLinux1への通信を許可するルールを追加する
        Router2# ***conf t***  
        Router2(config)# ***ip access-list extended ACL_PACKETFILTER***  
        Router2(config-ext-nacl)#15 permit ip host 10.X.3.106 host 10.X.1.102   
        Router2(config-ext-nacl)#end

        ```
        CSR2#conf t
        Enter configuration commands, one per line.  End with CNTL/Z.
        CSR2(config)#ip access-list extended ACL_PACKETFILTER
        CSR2(config-ext-nacl)#15 permit ip host 10.255.3.106 host 10.255.1.102     
        CSR2(config-ext-nacl)#end
        CSR2#
        ```


    1. 拡張ACL "ACL_PACKETFILTER" の変更後の状態を確認する  
        Router2# ***show ip access-list ACL_PACKETFILTER***  

        ```
        CSR2#show ip access-list ACL_PACKETFILTER
        Extended IP access list ACL_PACKETFILTER
            10 permit udp host 10.255.3.106 host 10.255.1.104 eq domain
            15 permit ip host 10.255.3.106 host 10.255.1.102
            20 deny ip 10.255.3.0 0.0.0.255 10.255.1.0 0.0.0.255 time-range WEEKDAYS (active) (26 matches)
            30 permit tcp any host 10.255.2.105 eq www 443 1080
            99 deny ip any any log (158 matches)
        CSR2#
        ```

        > 【確認ポイント】
        > シーケンス番号15番として、Linux2(host 10.X.3.106)からLinux1(host 10.X.1.102)へのIP通信を許可(Permit)するルールが追加されていることを確認する  

    1. configを保存する  
        Router2# ***write***  

        ```
        CSR2#write
        Building configuration...
        [OK]
        CSR2#     
        ```

1. Linux2からLinux1に通信できることを確認する  

    1. Linux2の管理画面に接続する  

    1. Linux2からLinux1に通信できることを確認する  
        ＞ ***ping 10.X.1.102 -c 4***  

        ```
        [admin@linux2 ~]$ ping 10.255.1.102 -c 4
        PING 10.255.1.102 (10.255.1.102) 56(84) bytes of data.
        64 bytes from 10.255.1.102: icmp_seq=1 ttl=62 time=5.85 ms
        64 bytes from 10.255.1.102: icmp_seq=2 ttl=62 time=3.91 ms
        64 bytes from 10.255.1.102: icmp_seq=3 ttl=62 time=4.19 ms
        64 bytes from 10.255.1.102: icmp_seq=4 ttl=62 time=7.21 ms

        --- 10.255.1.102 ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3005ms
        rtt min/avg/max/mdev = 3.917/5.295/7.218/1.335 ms
        [admin@linux2 ~]$ 
        ```

1. Linux2からSyslogのテストメッセージを送信する  

    1. Linux2の管理画面に接続する  

    1. loggerツールで、Linux2からLinux1にSyslogのテストメッセージを送信する    

        ＞ ***logger -n 10.X.1.102 "this is test message"***  
    
        ```
        [admin@linux2 ~]$ logger -n 10.255.1.102 "this is test message"
        [admin@linux2 ~]$ 
        ```

1. Linux1でSyslogのログファイルを確認する  

    1. Linux1の管理画面に接続する  

    1. Linux2のログファイルを参照し、テストメッセージが記録されていることを確認する  

        ＞ ***sudo tail -n 10 /var/log/rsyslog/10.X.3.106.log***
        
        ```
        [admin@linux1 ~]$ tail -n 10 /var/log/rsyslog/10.255.3.106.log 
        Dec  1 08:09:14 10.255.3.106 admin: this is test message
        [admin@linux1 ~]$ 
        ```

---

# 演習完了  
ここまでの手順で、以下の項目を学習できました。  
- [x] rsyslogを構成して、Syslogサービスを提供する   
- [x] IOS-XEのloggingを構成して、Syslogサーバーにログを保存する  
- [x] (オプション)パケットフィルタのACLルールを修正する  
- [x] (オプション)loggerでSyslogの動作を確認する  




