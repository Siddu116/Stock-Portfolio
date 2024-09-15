try:
    import requests # type: ignore
except ImportError:
    print("The 'requests' library is not installed. Please install it using 'pip install requests'.")

class StockPortfolioTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.portfolio = {}
    
    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol] += shares
        else:
            self.portfolio[symbol] = shares
    
    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol] -= shares
            if self.portfolio[symbol] <= 0:
                del self.portfolio[symbol]
        else:
            print("Stock not in portfolio.")
    
    def get_stock_price(self, symbol):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={self.api_key}"
        response = requests.get(url)
        data = response.json()
        try:
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            price = data['Time Series (1min)'][last_refreshed]['4. close']
            return float(price)
        except KeyError:
            print(f"Error fetching data for {symbol}.")
            return None
    
    def get_portfolio_value(self):
        total_value = 0.0
        for symbol, shares in self.portfolio.items():
            price = self.get_stock_price(symbol)
            if price:
                total_value += shares * price
        return total_value
    
    def display_portfolio(self):
        for symbol, shares in self.portfolio.items():
            price = self.get_stock_price(symbol)
            if price:
                value = shares * price
                print(f"{symbol}: {shares} shares @ ${price:.2f} = ${value:.2f}")
        print(f"Total Portfolio Value: ${self.get_portfolio_value():.2f}")

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    tracker = StockPortfolioTracker(api_key)
    
    tracker.add_stock("AAPL", 10)
    tracker.add_stock("GOOGL", 5)
    tracker.display_portfolio()
    
    tracker.remove_stock("AAPL", 5)
    tracker.display_portfolio()
