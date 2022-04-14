Make sure:
Please make sure all the files have the rught permissions

chmod +x (filename)

You can run chmod +x *.sh

for it to run via sudo

also make sure to make all your paths accessible via all machines.. I read somewhere in your code "G:/...." < remove this asap and make it a relative path

How to run this?
Just run:

sh server.sh
In case you have issues and the project is not running and giving error related to paramiko and requests

then run the below command -

sudo apt install python-paramiko
