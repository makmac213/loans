AWS Setup
---------

# Install apache
$ sudo yum install httpd
$ sudo service httpd start

# Install MySQL
$ sudo yum install mysql-server
$ sudo service mysqld start
# $ sudo /usr/bin/mysql_secure_installation


GIT
---

# install git
$ sudo yum install git


SSH to AWS
----------
# may change depending on the server and other creds
$ ssh -i [pem file] ec2-user@52.11.209.91

