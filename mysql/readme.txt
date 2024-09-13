Kubernetes mysql : https://medium.com/@midejoseph24/deploying-mysql-on-kubernetes-16758a42a746
From Kubernetes Deshboard
Go to Namespace : Data-platform
Service > Services > mysql
Endpoints
Host            : Ports (Name, Port, Protocol)    : Node           : Ready
10.42.3.56      : <unset>,3306,TCP                : nodeone        : true

Connect to dremio :- 
Host                   Port
10.42.3.56             3306

Authentication
Username               password
root                   sonu@sonu


Connection using Vs code :-
SQLTools                    :- https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools
SQLTools MySQL/MariaDB/TiDB :- https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools-driver-mysql

Connection Assistant
Connection Settings

Connection name*     : mysql
Connection group     :
Connect using*       : Server and Port
Server Address*      : 10.42.3.56
Port*                : 3306
Database*            : mysql
Username*            : root
Password mode        : SQLTools Driver Credentials

MySQL driver specific options
Authentication Protocol     : default  # Try to switch protocols in case you have problems.
SSL                         : Disabled
Connection Timeout          :
Show records default limit  : 50

Save Connection.
