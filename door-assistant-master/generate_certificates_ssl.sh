#Parameters for certificate
SUBJ="/C=AR/ST=Cordoba/L=door-assitant/O=another-project/CN=Estebanb"
mkdir -p certificates
echo "Generating certificates"
openssl req  -nodes -new -x509 -subj $SUBJ -keyout certificates/key.pem -out certificates/cert.pem
echo "Uploading certificates to fs"
mos put certificates/cert.pem
mos put certificates/key.pem
echo "Configuring SSL"
mos config-set http.listen_addr=443 http.ssl_key=key.pem http.ssl_cert=cert.pem
