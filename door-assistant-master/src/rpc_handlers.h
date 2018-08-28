#include "mgos.h"
#include "mgos_rpc.h"
#include "gpios.h"

void rpc_open_door_handler(struct mg_rpc_request_info *ri, void *cb_arg,
                   struct mg_rpc_frame_info *fi, struct mg_str args);
