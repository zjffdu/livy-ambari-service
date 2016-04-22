# livy-ambari-service

## PREREQUISITES
This technical preview requires the following software:

Ambari-2.2.2.0
HDP 2.4.2
Spark 1.6.1


## Installing Livy on an Ambari-Managed Cluster

To install Livy using Ambari, complete the following steps.

* Download the Livy Ambari Stack Definition (https://github.com/zjffdu/livy-ambari-service). On the node running Ambari server, run the following:
```
sudo git clone https://github.com/zjffdu/livy-ambari-service  /var/lib/ambari-server/resources/stacks/HDP/2.4/services/LIVY
```
* Restart the Ambari Server:
```
sudo service ambari-server restart
```
* After Ambari restarts and service indicators turn green, add the Livy Service:
At the bottom left of the Ambari dashboard, choose Actions -> Add Service:
On the Add Service screen, select the Livy service.
Step through the rest of the installation process, accepting all default values.
Click Deploy to complete the installation process.
