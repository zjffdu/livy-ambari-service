#!/usr/bin/python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""


import status_params

from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import hdp_select
from resource_management.libraries.functions import format
from resource_management.libraries.functions.version import format_hdp_stack_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path

from resource_management.libraries.script.script import Script
from resource_management.libraries.resources import HdfsResource

# a map of the Ambari role to the component name
# for use with <stack-root>/current/<component>
SERVER_ROLE_DIRECTORY_MAP = {
  'LIVY_SERVER' : 'livy-server',
  'LIVY_CLIENT' : 'livy-client',
}

component_directory = Script.get_component_from_role(SERVER_ROLE_DIRECTORY_MAP, "LIVY_SERVER")

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

stack_name = default("/hostLevelParams/stack_name", None)
stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
stack_version_formatted = format_hdp_stack_version(stack_version_unformatted)
host_sys_prepped = default("/hostLevelParams/host_sys_prepped", False)

# New Cluster Stack Version that is defined during the RESTART of a Stack Upgrade
version = default("/commandParams/version", None)

# TODO! FIXME! Version check is not working as of today :
#   $ yum list installed | grep <stack-selector-tool>
#   <stack-selector-tool>.noarch                            2.2.1.0-2340.el6           @HDP-2.2
# And stack_version_formatted returned from hostLevelParams/stack_version is : 2.2.0.0
# Commenting out for time being
#stack_is_hdp22_or_further = stack_version_formatted != "" and compare_versions(stack_version_formatted, '2.2.1.0') >= 0

livy_conf = '/etc/livy/conf'
hadoop_conf_dir = conf_select.get_hadoop_conf_dir()
hadoop_bin_dir = hdp_select.get_hadoop_dir("bin")

hadoop_home = hdp_select.get_hadoop_dir("home")
livy_conf = format("/usr/hdp/current/{component_directory}/conf")
livy_log_dir = config['configurations']['livy-env']['livy_log_dir']
livy_pid_dir = status_params.livy_pid_dir
livy_home = format("/usr/hdp/current/{component_directory}")

java_home = config['hostLevelParams']['java_home']

hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
hdfs_principal_name = config['configurations']['hadoop-env']['hdfs_principal_name']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
user_group = config['configurations']['cluster-env']['user_group']

livy_user = status_params.livy_user
livy_group = status_params.livy_group
user_group = status_params.user_group
livy_hdfs_user_dir = format("/user/{livy_user}")

livy_server_pid_file = status_params.livy_server_pid_file

livy_server_start = format("{livy_home}/bin/livy-server start")
livy_server_stop = format("{livy_home}/bin/livy-server stop")
livy_logs_dir = format("{livy_home}/logs")

livy_env_sh = config['configurations']['livy-env']['content']
livy_log4j_properties = config['configurations']['livy-log4j-properties']['content']

security_enabled = config['configurations']['cluster-env']['security_enabled']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))
livy_kerberos_keytab =  config['configurations']['livy-defaults']['livy.server.kerberos.keytab']
livy_kerberos_principal = config['configurations']['livy-defaults']['livy.server.kerberos.principal']

default_fs = config['configurations']['core-site']['fs.defaultFS']
hdfs_site = config['configurations']['hdfs-site']

dfs_type = default("/commandParams/dfs_type", "")

livy_livyserver_hosts = default("/clusterHostInfo/livy_server_hosts", [])

if len(livy_livyserver_hosts) > 0:
  livy_livyserver_host = livy_livyserver_hosts[0]
else:
  livy_livyserver_host = "localhost"

livy_livyserver_port = default('configurations/livy-defaults/livy.server.port',8998)

import functools
#create partial functions with common arguments for every HdfsResource call
#to create/delete hdfs directory/file/copyfromlocal we need to call params.HdfsResource in code
HdfsResource = functools.partial(
  HdfsResource,
  user=hdfs_user,
  hdfs_resource_ignore_file = "/var/lib/ambari-agent/data/.hdfs_resource_ignore",
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  hadoop_bin_dir = hadoop_bin_dir,
  hadoop_conf_dir = hadoop_conf_dir,
  principal_name = hdfs_principal_name,
  hdfs_site = hdfs_site,
  default_fs = default_fs
)

