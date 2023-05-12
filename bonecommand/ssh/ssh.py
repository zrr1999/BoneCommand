#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2023/1/5 22:43
# @Author : Rongrui Zhan
# @desc : 本代码未经授权禁止商用
import typer
import paramiko, sys, socket
import netmiko

try:
    import termios
    import tty

    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan):
    if has_termios:
        posix_shell(chan)
    else:
        windows_shell(chan)


def posix_shell(chan):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print("rn*** EOFrn")
                        break
                    sys.stdout.write(x.decode())
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan):
    import threading

    sys.stdout.write(
        "Line-buffered terminal emulation. Press F6 or ^Z to send EOF.rnrn"
    )

    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write("rn*** EOF ***rnrn")
                sys.stdout.flush()
                break
            sys.stdout.write(data)
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("1.15.231.43", 22, "ubuntu")
channel = ssh.invoke_shell()
channel.exec_command()
# 建立交互式管道
interactive_shell(channel)
# 关闭连接
channel.close()
ssh.close()

app = typer.Typer()


@app.command()
def connect(
    host: str, port: int = typer.Argument(22, min=0, max=65535), save: bool = True
):
    pass


@app.command()
def connect(save: bool = True):
    pass


if __name__ == "__main__":
    app()
