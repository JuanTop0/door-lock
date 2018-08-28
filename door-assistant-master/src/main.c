#include "mgos.h"
#include "mgos_rpc.h"
#include "gpios.h"
#include "rpc_handlers.h"

enum mgos_app_init_result mgos_app_init(void) {
    mg_rpc_add_handler(mgos_rpc_get_global(), "Door.Open", "", rpc_open_door_handler, NULL);
    init_gpios();
    return MGOS_APP_INIT_SUCCESS;
}

