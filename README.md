# livy-ambari-service

## PREREQUISITES
This technical preview requires the following software:

- Ambari-2.2.2.0
- HDP 2.4.2
- Spark 1.6.1


## Installing Livy on an Ambari-Managed Cluster

To install Livy using Ambari, complete the following steps.

* Download the Livy Ambari Stack Definition (https://github.com/zjffdu/livy-ambari-service). On the node running Ambari server, run the following:
```
sudo git clone https://github.com/zjffdu/livy-ambari-service  /var/lib/ambari-server/resources/stacks/HDP/2.4/services/LIVY
```
* Restart the Ambari Server:
```
ambari-server restart
```
* After Ambari restarts and service indicators turn green, add the Livy Service:
At the bottom left of the Ambari dashboard, choose Actions -> Add Service:
On the Add Service screen, select the Livy service.
Step through the rest of the installation process, accepting all default values.
Click Deploy to complete the installation process.  After the installation, you can check the livy service as following ![Livy Service Screenshot](/livy.png?raw=true "Livy Service Screenshot")


## Uninstall Livy on an Ambari-Managed Cluster
This livy ambari stack definiation is only for Technical Preview. Later starting from HDP 2.5, we will move livy as a slave service of spark instead of standalone service. So before you upgrade to HDP 2.5 or later, you need to first uninstall livy. Before you uninstall livy, please first stop livy in ambari server ui, then call the ambari rest api to remove livy from ambari.
```
curl -u admin:admin -H "X-Requested-By: ambari" -X DELETE  http://${ambari-server}:8080/api/v1/clusters/${clusetr_name}/services/LIVY
```
