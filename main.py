# This is our code
"""

                              _
                           _ooOoo_
                          o8888888o
                          88" . "88
                          (| -_- |)
                          O\  =  /O
                       ____/`---'\____
                     .'  \\|     |//  `.
                    /  \\|||  :  |||//  \
                   /  _||||| -:- |||||_  \
                   |   | \\\  -  /'| |   |
                   | \_|  `\`---'//  |_/ |
                   \  .-\__ `-. -'__/-.  /
                 ___`. .'  /--.--\  `. .'___
              ."" '<  `.___\_<|>_/___.' _> \"".
             | | :  `- \`. ;`. _/; .'/ /  .' ; |
             \  \ `-.   \_\_`. _.'_/_/  -' _.' /
   ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
               Believe in Buddha, no bug in code
"""
import socket
import time
from threading import Thread

import analyzer, book, parser

__author__ = "Kai Kang, Hongyu Li, Shaojie Bai"

""" Initialization Section """

TCP_IP = '1.1.1.1'
TCP_PORT = 20000
BUFFER_SIZE = 1024
MESSAGE = "HELLO CANNON"
INFO = []

TCP_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


BOOK = book.Book()
PARSER = parser.Parser(BOOK)
ANALYZER = analyzer.Analyser(BOOK)

""" Initialization Section Ends """


def initReceive():
    """
    Handles the receipt of information and messages from the TCP socket and put them on the buffer.

    :return: None
    """
    TCP_SOCK.sendall(MESSAGE + "\n")

    while 1:
        data = TCP_SOCK.recv(BUFFER_SIZE)
        if data == "":
            break
        INFO.append(data)

    print "Connection closed."


def naiveBondStart():
    TCP_SOCK.sendall("ADD 3 BOND BUY 999 100\n")


def naiveBondAnalyze(msg):
    id = 5
    # Assume the type is fill
    if msg["dir"] == "SELL":
        size = msg["size"]
        transaction_msg = "ADD %d BOND SELL 1001 %d\n" % (id, size)
        TCP_SOCK.sendall(transaction_msg)
    elif msg["dir"] == "BUY":
        size = msg["size"]
        transaction_msg = "ADD %d BOND BUY 999 %d\n" % (id, size)
        TCP_SOCK.sendall(transaction_msg)

    print "Transaction Msg: %s" % transaction_msg
    id += 1


def main():
    TCP_SOCK.connect((TCP_IP, TCP_PORT))
    chant = Thread(target=initReceive, name="KeepReceiving", args=())
    chant.start()

    while 1:
        if not INFO:
            time.sleep(1)
            continue
        else:
            PARSER.parseMsg(INFO.pop(0))

    # Close the socket
    TCP_SOCK.close()
    print "\nCannon etc bot closed.\n"
    chant.join(timeout=20)


if __name__ == '__main__':
    main()
