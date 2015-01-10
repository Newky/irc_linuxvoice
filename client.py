import argparse
import socket
import time


def create_irc_socket(host, port):
    sock = socket.socket()
    sock.connect((host, port))
    return sock


def nick_msg(nick):
    return "NICK {}\r\n".format(nick)


def user_msg(nick, real_name):
    return "USER {} 0 * :{}\r\n".format(nick, real_name)


def pong_msg(body):
    return "PONG {}\r\n".format(body)


def join_msg(channel):
    return "JOIN {}\r\n".format(channel)


def register(sock, nick, real_name):
    sock.send(nick_msg(nick))
    sock.send(user_msg(nick, real_name))


def join_channel(sock, channel):
    sock.send(join_msg(channel))


def parse_message(msg):
    # get rid of newlines and whitespace.
    msg = msg.rstrip()
    # split by space
    components = msg.split()

    # if the first part starts with a : the message includes a
    # source.
    if components[0].startswith(":"):
        source = components[0]
        command = components[1]
        rest = ' '.join(components[2:])
    else:
        source = None
        command = components[0]
        rest = ' '.join(components[1:])

    print "MESSAGE HAS A SOURCE: {}".format(source)
    print "MESSAGE HAS A COMMAND: {}".format(command)
    print "MESSAGE HAS A REST: {}".format(rest)
    return source, command, rest


def priv_msg(target, message):
    return "PRIVMSG {} :{}\r\n".format(target, message)


def get_nick_from_source(source):
    # Source will look something like :<NICK>!<USER>@<IP ADDRESS>
    # strip preceding ":"
    source = source[1:]
    source = source[:source.find("!")]
    return source


def priv_msg_responder(sock, source, rest):
    # split up the rest of the privmsg to get the target
    target, message = rest.split(" ", 1)
    if 'What is the time?' in message:
        sock.send(
            priv_msg(
                target, 'Hello, {}. The time is {}'.format(
                    get_nick_from_source(source),
                    time.asctime()
                )
            )
        )

def join_responder(sock, source, room_joined):
    sock.send(
       priv_msg(
           room_joined,
           'Welcome to {}, {}!'.format(
               room_joined,
               get_nick_from_source(source)
           )
       )
    )


def pong_msg_responder(sock, source, rest):
    sock.send(pong_msg(rest))


COMMANDS = {
    "PING": pong_msg_responder,
    "PRIVMSG": priv_msg_responder,
    "JOIN": join_responder
}


def action_on_commands(sock, source, command, rest):
    def do_nothing(sock, s, r):
        return

    return COMMANDS.get(command, do_nothing)(sock, source, rest)


def read_loop(sock):
    try:
        while 1:
            data = sock.recv(1024)
            # if the data ends with a \r\n everything is fine.
            # if it doesn't we need to keep appending until it does
            while not data.endswith("\r\n"):
                data += sock.recv(1024)

            for message in data.split("\r\n"):
                if not message:
                    continue
                source, command, rest = parse_message(message)
                action_on_commands(sock, source, command, rest)
    except KeyboardInterrupt:
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host",
        help="IRC host to connect to", default="irc.freenode.org")
    parser.add_argument("--port", "-p", dest="port",
        help="IRC port to connect to", default=6667)
    parser.add_argument("--nick", "-n", dest="nick",
        help="IRC nick to use.", default="LinuxVoiceTest")
    parser.add_argument("--real-name", "-r", dest="real_name",
        help="IRC real name to use.", default="Linux Voice IRC Test")
    parser.add_argument("--channel", "-c", dest="channel",
        help="Channel for bot to join.", default="#linuxvoice_test")
    return parser.parse_args()


def main():
    args = parse_args()
    sock = create_irc_socket(args.host, args.port)
    register(sock, args.nick, args.real_name)
    join_channel(sock, args.channel)
    read_loop(sock)
    sock.close()


if __name__ == "__main__":
    main()
