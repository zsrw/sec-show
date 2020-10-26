#! /usr/bin/bash
echo 正在监控绑定与解绑---------------

function set_eip()
{
type="Content-Type: application/json"
bind="{\"port\":{\"allowed_address_pairs\":[{\"ip_address\":\"172.16.0.52\"}]}}"
url="https://iecs.myhuaweicloud.com/v1/ports/0398ddef-c32d-4b4e-a0e7-b360c376ec0c"
curl -k -w "@e.txt" -o /dev/null -s -L -XPUT $url -H $type -H "@token1.txt" -d $bind >> result.txt
sleep 10s
set_eip
}
set_eip
