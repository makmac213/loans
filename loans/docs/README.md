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


Virtualenv
----------
$ pip install virtualenvwrapper
$ mkdir ~/.virtualenvs
$ cat ~/.bashrc
# add lines to the end of .bashrc
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
# reload
$ source ~/.bashrc
# create virtual env
$ mkvirtualenv loans
$ workon loans


MongoDB
-------
http://docs.mongodb.org/manual/tutorial/install-mongodb-on-amazon/