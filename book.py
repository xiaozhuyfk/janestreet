class Book(object):
	
	def __init__(self):
		self.book = dict()
		self.BUY = 0
		self.SELL = 1
		
	def getBuyList(self, symbol):
		if symbol in self.book:
			return self.book[symbol][self.BUY]
		else:
			return []
	
	def getSellList(self, symbol):
		if symbol in self.book:
			return self.book[symbol][self.SELL]
		else:
			return []
	
	def show(self):
		print "--------------BOOK---------------"
		for symbol in self.book:
			print symbol
			print self.book[symbol][self.BUY]
			print self.book[symbol][self.SELL]
			print "---------------------------"
		print "--------------END----------------"

	def getHighestBuyPrice(self, symbol):
		if symbol not in self.book:
			return -1
		f = lambda x, y: if x[0] > y[0] then x else y
		return reduce(f, self.book[symbol][self.BUY])[0]
	
	def getLowestSellPrice(self, symbol):
		if symbol not in self.book:
			return -1
		f = lambda x, y: if x[0] < y[0] then x else y
		return reduce(f, self.book[symbol][self.SELL])[0]
	
	def _update(self, symbol, buyList, sellList):
		self.book[symbol] = (buyList, sellList)
