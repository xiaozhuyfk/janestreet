MSG_LEFTOVER = ""

class Parser(object):

    def __init__(self, book):
        self.book = book

    def parseMsg(self, msg):
        global MSG_LEFTOVER

        msg = MSG_LEFTOVER + msg
        lines = msg.split("\n")

        # To handle possible wraparound error during TCP connection
        MSG_LEFTOVER = lines.pop()

        # otherwise drop
        for line in lines:
            args = line.split(" ")
            if args[0] == "TRADE":
                return self.tradeParse(args[1::])
            elif args[0] == "BOOK":
                return self.bookParse(args[1::])
            elif args[0] == "FILL":
                return self.fillParse(args[1::])
            elif args[0] == "OUT":
                return self.outParse(args[1::])

    def bookParse(self, args):
        symbol = args[0]

        args = args[1::]
        buyList = []
        sellList = []
        mode = args[0]
        args = args[1::]

        while args:
            if mode == 'BUY':
                if args[0] == 'SELL':
                    mode = 'SELL'
                else:
                    buyList.append(self.parseTransaction(args[0]))
            else:
                sellList.append(self.parseTransaction(args[0]))
            args = args[1::]

        self.book._update(symbol, buyList=buyList, sellList=sellList)

        return self.book.book

    def tradeParse(self, args):
        # SYMBOL PRICE SIZE
        return {
            "symbol": args[0],
            "price": int(args[1])
        }

    def parseTransaction(self, s):
        s = s.split(":")
        tradePrice = int(s[0])
        tradeAmount = int(s[1])
        return (tradePrice, tradeAmount)


    def fillParse(self, args):
        # ID SYMBOL DIR PRICE SIZE
        return {
            "symbol": args[0],
            "dir": args[1],
            "price": int(args[2]),
            "size": int(args[3])
        }


    def outParse(self, args):
        # ID
        return {
            "id": args[0]
        }