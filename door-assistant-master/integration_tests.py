#!/usr/bin/env python3
import unittest
import json
import shlex
import subprocess
from time import sleep

BUILD = "mos build --arch esp8266"
FLASH = "mos flash"
USER_1 = "prueba"
USER_2 = "otra"
PASSWORD_1 = "pobaxx"
PASSWORD_2 = "tranca"
GEN_PASS_RPC = "/bin/bash generate_user_and_password_for_rpc.sh {} {}"
RPC_CRED = 'mos --rpc-creds "{}:{}"'
RPC_INV_CRED = 'mos --rpc-creds "no:existe"'
RPC_NO_CRED = "mos"
GET_CONF = "call Config.Get"
SET_CONF = "config-set"
ENABLE_DOOR = "door.enable=true"
DISABLE_DOOR = "door.enable=false"
OPEN_DOOR = "call Door.Open"
RPC_ADD_USER = "call RPC.Add_user "


def build_firmware():
    args = shlex.split(BUILD)
    p = subprocess.Popen(args)
    exit_code = p.wait()
    assert exit_code == 0


def flash_firmware():
    args = shlex.split(FLASH)
    p = subprocess.Popen(args)
    exit_code = p.wait()
    assert exit_code == 0
    sleep(3)


def bootstrap_rpc_user_and_password():
    args = shlex.split(GEN_PASS_RPC.format(USER_1, PASSWORD_1))
    p = subprocess.Popen(args)
    p.wait()  # mongoose bug, output its error when load credentials.


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_firmware()
        flash_firmware()
        bootstrap_rpc_user_and_password()

    def test_should_get_config_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(GET_CONF)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)

    def test_should_not_get_config_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(GET_CONF)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_disable_door_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(SET_CONF)
        args += shlex.split(DISABLE_DOOR)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(3)

        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), "false")
        p.stdout.close()

    def test_should_not_disable_door_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(SET_CONF)
        args += shlex.split(DISABLE_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()
        sleep(3)

        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_enable_door_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(SET_CONF)
        args += shlex.split(ENABLE_DOOR)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(3)

        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(GET_CONF)
        args.append(json.dumps({"key": "door.enable"}))
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), "true")
        p.stdout.close()

    def test_should_open_door_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        self.assertEqual(p.stdout.read().decode('utf-8').rstrip(), '{\n  "Door": "Open"\n}')
        p.stdout.close()

    def test_should_not_open_door_when_credentials_are_invalid(self):
        args = shlex.split(RPC_INV_CRED)
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("remote error 401", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_not_open_door_when_dont_have_credentials(self):
        args = shlex.split(RPC_NO_CRED)
        args += shlex.split(OPEN_DOOR)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 1)
        self.assertIn("wrong RPC creds spec", p.stderr.read().decode('utf-8').rstrip())
        p.stdout.close()
        p.stderr.close()

    def test_should_create_user_when_credentials_are_valid(self):
        args = shlex.split((RPC_CRED).format(USER_1, PASSWORD_1))
        args += shlex.split(RPC_ADD_USER)
        args.append('{}'.format(json.dumps({'user': USER_2, 'pass': PASSWORD_2})))
        print(args)
        p = subprocess.Popen(args)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        sleep(3)

        args = shlex.split((RPC_CRED).format(USER_2, PASSWORD_2))
        args += shlex.split(GET_CONF)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        exit_code = p.wait()
        self.assertEqual(exit_code, 0)
        p.stdout.close()


if __name__ == '__main__':
    unittest.main()
