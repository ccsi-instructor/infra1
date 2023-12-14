

# Linux ServerでWebサーバーを構築する

---

## 演習の意図
    演習ガイドを参照して演習の意図をあらかじめ確認してください

## 演習における役割と、環境のパラメータ
- X: ご自身のPod番号
- Linux Webサーバー役: Linux1
- クライアント デスクトップ環境: WinClient(WC1-yyMMddX)

## 注意
- 手順例の画像は<B>pod255</B>に準拠したパラメータのものです
- 手順内の<B>X</B>表記はご自身のpod番号に読み替えてください

---

## 1. Linux Webサーバー構築の準備
Linux Server1(Linux1)をLinux Webサーバーとして構築します。  

1. Linux1の管理画面に接続する  
    <kbd>![img](image/04/11.png)</kbd>
    
1. カレントディレクトリが管理者アカウントのホームディレクトリであることを確認する  
    ＞ ***hostname***
    ＞ ***whoami***
    ＞ ***pwd***

    ```
    [admin@linux1 ~]$ hostname
    linux1
    [admin@linux1 ~]$ whoami
    admin
    [admin@linux1 ~]$ pwd
    /home/admin
    [admin@linux1 ~]$ 
    ```

1. NGINXのRPMパッケージをダウンロードする

    ＞ ***wget http://nginx.org/packages/centos/7/x86_64/RPMS/nginx-1.22.1-1.el7.ngx.x86_64.rpm***  


    > 【補足】
    > 演習環境のクリップボードを直接編集することで、上のコマンドをコピーして演習環境に貼り付けることができます。 
    > 手順① [Ctrl]+[Shift]+[Alt]キーを入力する(Macの場合は[Ctrl]+[Shift]+[Command])  
    > 手順② 画面左の操作メニューのクリップボードの入力欄に、上のコマンドをコピーして貼り付ける  
    > 手順③ [Ctrl]+[Shift]+[Alt]キーを入力し、操作メニューを終了する  
    > 手順④ Linuxのプロンプト画面上で右クリックする  
    > 手順⑤ プロンプトにコマンドが入力されたことを確認する  

    ```
    [admin@linux1 ~]$ wget http://nginx.org/packages/centos/7/x86_64/RPMS/nginx-1.22.1-1.el7.ngx.x86_64.rpm
    --2023-09-05 04:56:01--  http://nginx.org/packages/centos/7/x86_64/RPMS/nginx-1.22.1-1.el7.ngx.x86_64.rpm
    Resolving nginx.org (nginx.org)... 3.125.197.172, 52.58.199.22, 2a05:d014:edb:5702::6, ...
    Connecting to nginx.org (nginx.org)|3.125.197.172|:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 816272 (797K) [application/x-redhat-package-manager]
    Saving to: ‘nginx-1.22.1-1.el7.ngx.x86_64.rpm’

    100%[==============================================================================================================================================>] 816,272      669KB/s   in 1.2s   

    2023-09-05 04:56:03 (669 KB/s) - ‘nginx-1.22.1-1.el7.ngx.x86_64.rpm’ saved [816272/816272]

    [admin@linux1 ~]$ 
    ```

1. ダウンロードしたパッケージファイルを確認する

    ＞ ***ls -l***  

    ```
    [admin@linux1 ~]$ ls -l
    total 800
    -rw-rw-r-- 1 admin admin 816272 Oct 19  2022 nginx-1.22.1-1.el7.ngx.x86_64.rpm
    [admin@linux1 ~]$ 
    ```



1. NGINXをRPMファイルからローカルインストールする

    ＞ ***sudo yum localinstall nginx-1.22.1-1.el7.ngx.x86_64.rpm***  

    ＞ <略>

    ＞ Is this ok [y/d/N]: ***y***

    ```
    [admin@linux1 ~]$ sudo yum localinstall nginx-1.22.1-1.el7.ngx.x86_64.rpm
    Loaded plugins: langpacks
    Examining nginx-1.22.1-1.el7.ngx.x86_64.rpm: 1:nginx-1.22.1-1.el7.ngx.x86_64
    Marking nginx-1.22.1-1.el7.ngx.x86_64.rpm to be installed
    Resolving Dependencies
    --> Running transaction check
    ---> Package nginx.x86_64 1:1.22.1-1.el7.ngx will be installed
    --> Processing Dependency: libpcre2-8.so.0()(64bit) for package: 1:nginx-1.22.1-1.el7.ngx.x86_64
    --> Running transaction check
    ---> Package pcre2.x86_64 0:10.23-2.el7 will be installed
    --> Finished Dependency Resolution

    Dependencies Resolved

    ========================================================================================================================================================================================
    Package                           Arch                               Version                                          Repository                                                  Size
    ========================================================================================================================================================================================
    Installing:
    nginx                             x86_64                             1:1.22.1-1.el7.ngx                               /nginx-1.22.1-1.el7.ngx.x86_64                             2.8 M
    Installing for dependencies:
    pcre2                             x86_64                             10.23-2.el7                                      base-openlogic                                             201 k

    Transaction Summary
    ========================================================================================================================================================================================
    Install  1 Package (+1 Dependent package)

    Total size: 3.0 M
    Total download size: 201 k
    Installed size: 3.3 M
    Is this ok [y/d/N]: y
    Downloading packages:
    pcre2-10.23-2.el7.x86_64.rpm                                                                                                                                     | 201 kB  00:00:00     
    Running transaction check
    Running transaction test
    Transaction test succeeded
    Running transaction
    Installing : pcre2-10.23-2.el7.x86_64                                                                                                                                             1/2 
    Installing : 1:nginx-1.22.1-1.el7.ngx.x86_64                                                                                                                                      2/2 
    ----------------------------------------------------------------------

    Thanks for using nginx!

    Please find the official documentation for nginx here:
    * https://nginx.org/en/docs/

    Please subscribe to nginx-announce mailing list to get
    the most important news about nginx:
    * https://nginx.org/en/support.html

    Commercial subscriptions for nginx are available on:
    * https://nginx.com/products/

    ----------------------------------------------------------------------
    Verifying  : pcre2-10.23-2.el7.x86_64                                                                                                                                             1/2 
    Verifying  : 1:nginx-1.22.1-1.el7.ngx.x86_64                                                                                                                                      2/2 

    Installed:
    nginx.x86_64 1:1.22.1-1.el7.ngx                                                                                                                                                       

    Dependency Installed:
    pcre2.x86_64 0:10.23-2.el7                                                                                                                                                            

    Complete!
    [admin@linux1 ~]$ 
    ```


1. NGINX(nginx)サービスのStatusを確認する  
    ＞ ***systemctl status nginx***  
 
    > 【確認ポイント】  
    > 'Active:' が 'inactive (dead)'であることを確認する  
    - [x] NGINX(nginx)が、サービスとして認識されていること  
    - [x] NGINX(nginx)サービスが、まだ起動していないこと  

    ```
    [admin@linux1 ~]$ systemctl status nginx
    ● nginx.service - nginx - high performance web server
    Loaded: loaded (/usr/lib/systemd/system/nginx.service; disabled; vendor preset: disabled)
    Active: inactive (dead)
        Docs: http://nginx.org/en/docs/
    [admin@linux1 ~]$ 
    ```

1. NGINX(nginx)サービスを自動起動に設定する  
    ＞ ***sudo systemctl enable nginx***  
 
1. NGINX(nginx)サービスを起動する  
    ＞ ***sudo systemctl start nginx***  

1. NGINX(nginx)サービスのStatusを確認する  
    ＞ ***systemctl status nginx***  
 
    > 【確認ポイント】  
    > 'Active:' が 'active(running)'であることを確認する  
    - [x] NGINX(nginx)サービスが起動していること   

    ```
    [admin@linux1 ~]$ sudo systemctl enable nginx
    Created symlink from /etc/systemd/system/multi-user.target.wants/nginx.service to /usr/lib/systemd/system/nginx.service.
    [admin@linux1 ~]$ sudo systemctl start nginx
    [admin@linux1 ~]$ 
    [admin@linux1 ~]$ systemctl status nginx
    ● nginx.service - nginx - high performance web server
    Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
    Active: active (running) since Tue 2023-09-05 06:07:32 UTC; 4s ago
        Docs: http://nginx.org/en/docs/
    Process: 3418 ExecStart=/usr/sbin/nginx -c /etc/nginx/nginx.conf (code=exited, status=0/SUCCESS)
    Main PID: 3419 (nginx)
        Tasks: 2
    Memory: 3.3M
    CGroup: /system.slice/nginx.service
            ├─3419 nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
            └─3420 nginx: worker process

    Sep 05 06:07:32 linux1 systemd[1]: Starting nginx - high performance web server...
    Sep 05 06:07:32 linux1 systemd[1]: Can't open PID file /var/run/nginx.pid (yet?) after start: No such file or directory
    Sep 05 06:07:32 linux1 systemd[1]: Started nginx - high performance web server.
    [admin@linux1 ~]$ 
    ```

---

## 2. Webサーバーのコンテンツを公開する
  
1. NGINXのconfigファイルを編集し、Webサーバーとしての要件を実装する   
    ＞ ***sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak***  
    ＞ ***sudo vi /etc/nginx/nginx.conf***  
    ＞ ***diff /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak***  

    【要件】  
    - [x] /var/www/html ディレクトリをWebコンテンツとして公開する      

    ```
    [admin@linux1 ~]$ diff /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
    31,38c31
    <     #include /etc/nginx/conf.d/*.conf;
    < 
    <     server {
    <         listen80;
    <         location / {
    <         root /var/www/html;
    <         }
    <     }
    ---
    >     include /etc/nginx/conf.d/*.conf;
    [admin@linux1 ~]$ 
    ```

    ```
    [admin@linux1 ~]$ cat  /etc/nginx/nginx.conf

    user  nginx;
    worker_processes  auto;

    error_log  /var/log/nginx/error.log notice;
    pid        /var/run/nginx.pid;


    events {
        worker_connections  1024;
    }


    http {
        include       /etc/nginx/mime.types;
        default_type  application/octet-stream;

        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                        '$status $body_bytes_sent "$http_referer" '
                        '"$http_user_agent" "$http_x_forwarded_for"';

        access_log  /var/log/nginx/access.log  main;

        sendfile        on;
        #tcp_nopush     on;

        keepalive_timeout  65;

        #gzip  on;

        #include /etc/nginx/conf.d/*.conf;

        server {
            listen80;
            location / {
            root /var/www/html;
            }
        }
    }
    [admin@linux1 ~]$ 
    ```

1. NGINX(nginx)サービスを再起動する  
    ＞ ***sudo systemctl restart nginx***  

1. Webコンテンツのディレクトリを作成する  
    ＞ ***sudo mkdir -p /var/www/html***  

1. WebコンテンツとしてのHTMLファイル(/var/www/html/index.html)を作成し、任意の文言を記入して保存する  
    ＞ ***sudo touch /var/www/html/index.html***  
    ＞ ***sudo cp /var/www/html/index.html /var/www/html/index.html.bak***  
    ＞ ***sudo vi /var/www/html/index.html***  
    ＞ ***diff /var/www/html/index.html /var/www/html/index.html.bak***  

    ```
    [admin@linux1 ~]$ diff /var/www/html/index.html /var/www/html/index.html.bak
    1,6d0
    < <html>
    < 
    < Why was nginx so goot at yoga? <br>
    < Because...
    < 
    < </html>
    [admin@linux1 ~]$ 
    ```



---

## 3. ClientからWebサーバーにアクセスする
1. 操作コンピュータを変更するため、演習環境のトップページに戻る  
1. Windows Client(WinClient)の管理画面に "admin" で接続する   
1. WinClientでWebブラウザ(Google Chrome)を起動する  
1. Webブラウザのアドレス欄に [http://10.X.1.102/index.html] と入力し、[Enter]キーを押下する  
    <kbd>![img](image/08/21.png)</kbd> 

    > 【動作テストの観点】  
    > NGINXで基本的なWebサーバーを構築できたことを確認する     

    - [x] WebブラウザでHTMLファイルを表示できること    

---

## 演習完了  
ここまでの手順で、以下の項目を学習できました。
- [x] NGINXをインストールする
- [x] Webコンテンツを公開する



