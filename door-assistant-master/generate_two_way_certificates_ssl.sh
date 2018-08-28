mkdir -p certificates
#Common parameters
SUBJ="/C=IE/ST=Dublin/L=Docks/O=MyCompany/CN=howdy"

# Generate CA
openssl genrsa -out certificates/ca.key 2048
openssl req -new -x509 -days 365 -subj $SUBJ -key certificates/ca.key -out certificates/ca.crt

# Generate client cert
openssl genrsa -out certificates/client.key 2048
openssl req -new -key certificates/client.key -out certificates/client.csr -subj $SUBJ
openssl x509 -req -days 365 -in certificates/client.csr -CA certificates/ca.crt \
    -CAkey certificates/ca.key -set_serial 01 -out certificates/client.crt

# Generate server cert
openssl genrsa -out certificates/server.key 2048
openssl req -new -key certificates/server.key -out certificates/server.csr -subj $SUBJ
openssl x509 -req -days 365 -in certificates/server.csr -CA certificates/ca.crt \
    -CAkey certificates/ca.key -set_serial 01 -out certificates/server.crt

# Upload server key, cert & ca cert to the device
mos put certificates/ca.crt
mos put certificates/server.key
mos put certificates/server.crt

# Update HTTP server settings to use mutual TLS
mos config-set http.ssl_ca_cert=ca.crt http.ssl_cert=server.crt \
    http.ssl_key=server.key http.listen_addr=443

