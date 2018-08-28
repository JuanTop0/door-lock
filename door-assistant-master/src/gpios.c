#include "mgos.h"
#define DOOR_GPIO (4)

static void close_door(){
    mgos_gpio_write(DOOR_GPIO, false);
}

void init_gpios(){
    mgos_gpio_set_mode(DOOR_GPIO, MGOS_GPIO_MODE_OUTPUT);
    mgos_gpio_set_pull(DOOR_GPIO, MGOS_GPIO_PULL_NONE);
}

bool open_door(){
    if(get_cfg()->door.enable == false) return false;
    mgos_gpio_write(DOOR_GPIO, true);
    mgos_set_timer(get_cfg()->door.keep_open_ms, false, close_door, NULL);
    return true;
}
