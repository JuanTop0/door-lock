USER=$1
REALM="admin"
PASSWORD=$2

echo user:$USER password:$PASSWORD
htdigest=$(echo -n "$USER:$REALM:" && echo -n "$USER:$REALM:$PASSWORD" | md5sum) 
echo ${htdigest} | cut -d' ' -f1 > rpc_auth

echo '[{"method": "*", "acl": "+'$USER'"},]' > rpc_acl

mos put rpc_auth
mos put rpc_acl
mos config-set rpc.auth_domain="$REALM" rpc.auth_file="rpc_auth" rpc.acl_file="rpc_acl"
