load('api_rpc.js');
load('api_file.js');

function add_entry_to_rpc_auth(user, pass){
    let _md5 = ffi('void cs_md5(char *, char *, int, int)');
    let hash = 'd2c63372113b6fecb9dfa34629bcc4db';
    let raw_digest = user+':admin:'+pass;
    _md5(hash, raw_digest, raw_digest.length, 0);
    let hashed_digest = args.user+':admin:'+hash;
    File.write(hashed_digest+'\n', 'rpc_auth', 'a');
}

function add_user_to_rpc_acl(user){
    let rpc_acl = JSON.parse(File.read('rpc_acl'));
    if (rpc_acl){
        //return rpc_acl.acl;
        rpc_acl[0].acl = rpc_acl[0].acl + ',+'+ user;
        //return rpc_acl;
        File.write(JSON.stringify(rpc_acl), 'rpc_acl');
        return "OK";
    }
    return "rpc_acl not found";
}

RPC.addHandler('RPC.Add_user', function(args) {
    add_entry_to_rpc_auth(args.user, args.pass);
    return add_user_to_rpc_acl(args.user);
});
