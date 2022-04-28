#sed -i "s/_DOMAINNAME_/`hostname`/g" data/jenkins.conf 

sed -i "s/_DOMAINNAME_/`ec2metadata --public-hostname`/g" data/jenkins.conf 




