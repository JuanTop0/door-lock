#include "rpc_handlers.h"
void rpc_open_door_handler(struct mg_rpc_request_info *ri, void *cb_arg,
                   struct mg_rpc_frame_info *fi, struct mg_str args) {
    if(open_door() == true){
        mg_rpc_send_responsef(ri, "{Door: Open}");
    }else{
        mg_rpc_send_responsef(ri, "{Door: Disabled}");
    }
    (void) fi;
    (void) args;
    (void) cb_arg;
}

