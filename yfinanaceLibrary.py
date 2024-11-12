import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SectorRecommender:
    def __init__(self):
        # Major sector ETFs for tracking sector performance
        self.sector_etfs = {
            'Technology': 'XLK',
            'Financial': 'XLF',
            'Healthcare': 'XLV',
            'Consumer Discretionary': 'XLY',
            'Consumer Staples': 'XLP',
            'Energy': 'XLE',
            'Materials': 'XLB',
            'Industrial': 'XLI',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Communication Services': 'XLC'
        }
        
        # Dictionary to store sector components
        self.sector_components = {
            'Technology': ['AAPL', 'MSFT', 'NVDA', 'ADBE', 'CRM', 'ACN', 'ORCL', 'CSCO', 'IBM', 'AMD'],
            'Financial': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'BLK', 'C', 'SPGI', 'AXP', 'V'],
            'Healthcare': ['JNJ', 'UNH', 'PFE', 'ABT', 'TMO', 'MRK', 'DHR', 'ABBV', 'BMY', 'LLY'],
            'Consumer Discretionary': ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'BKNG', 'MAR'],
            'Consumer Staples': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'PM', 'MO', 'EL', 'CL', 'KMB'],
            'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'KMI'],
            'Materials': ['LIN', 'APD', 'ECL', 'SHW', 'FCX', 'NEM', 'DOW', 'DD', 'NUE', 'VMC'],
            'Industrial': ['HON', 'UPS', 'BA', 'CAT', 'DE', 'LMT', 'GE', 'MMM', 'RTX', 'UNP'],
            'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL', 'PEG', 'WEC'],
            'Real Estate': ['PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'DLR', 'O', 'WELL', 'AVB', 'EQR'],
            'Communication Services': ['GOOGL', 'META', 'NFLX', 'TMUS', 'CMCSA', 'VZ', 'T', 'DIS', 'ATVI', 'EA']
        }
        
    def fetch_sector_data(self, period='1mo', interval='1d'):
        """
        Fetch sector ETF data to analyze sector performance
        """
        sector_data = {}
        
        for sector, etf in self.sector_etfs.items():
            try:
                etf_data = yf.download(etf, period=period, interval=interval, progress=False)
                sector_data[sector] = etf_data
            except Exception as e:
                print(f"Error fetching data for {sector} ({etf}): {str(e)}")
                
        return sector_data
    
    def calculate_sector_metrics(self, sector_data):
        """
        Calculate various performance metrics for each sector
        """
        metrics = {}
        
        for sector, data in sector_data.items():
            if not data.empty and len(data) >= 5:
                # Calculate returns using proper indexing
                latest_close = data['Adj Close'].iloc[-1]
                five_days_ago_close = data['Adj Close'].iloc[-5]
                first_close = data['Adj Close'].iloc[0]
                
                # Calculate returns
                returns = data['Adj Close'].pct_change()
                cumulative_return = (latest_close / first_close) - 1
                last_5d_return = (latest_close / five_days_ago_close) - 1
                
                # Calculate volatility
                volatility = data['Adj Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
                
                # Calculate momentum
                momentum_score = (2 * last_5d_return + cumulative_return) / 3
                
                # Calculate volume trend
                volume_trend = data['Volume'].pct_change().mean()
                
                # Calculate RSI
                delta = data['Adj Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs.iloc[-1])) if not rs.empty else 50
                
                risk = 0
                if not volatility.empty:
                    risk = cumulative_return / volatility

                metrics[sector] = {
                    'return': cumulative_return,
                    'last_5d_return': last_5d_return,
                    'volatility': volatility,
                    'momentum_score': momentum_score,
                    'volume_trend': volume_trend,
                    'rsi': rsi,
                    'risk_adjusted_return': risk
                }
        
        return metrics
    
    def get_top_sectors(self, metrics, top_n=3):
        """
        Identify top performing sectors based on multiple metrics
        """
        # Create DataFrame from metrics
        df_metrics = pd.DataFrame(metrics).T
        
        print(df_metrics.columns)
        # Calculate composite score
        df_metrics['composite_score'] = (
            df_metrics['momentum_score'] * 0.3 +
            df_metrics['risk_adjusted_return'] * 0.3 +
            (df_metrics['rsi'] / 100) * 0.2 +
            df_metrics['volume_trend'] * 0.2
        )
        
        # Sort sectors by composite score
        top_sectors = df_metrics.sort_values('composite_score', ascending=False).head(top_n)
        
        return top_sectors
    
    def get_sector_recommendations(self, top_sectors, num_stocks_per_sector=3):
        """
        Get stock recommendations for top performing sectors
        """
        recommendations = []
        
        for sector in top_sectors.index:
            sector_stocks = self.sector_components[sector]
            
            # Fetch recent data for sector components
            stock_data = {}
            for stock in sector_stocks:
                try:
                    data = yf.download(stock, period='1mo', interval='1d', progress=False)
                    if len(data) > 0:
                        returns = data['Adj Close'].pct_change()
                        momentum = (data['Adj Close'][-1] / data['Adj Close'][0]) - 1
                        volatility = returns.std() * np.sqrt(252)
                        stock_data[stock] = {
                            'return': momentum,
                            'volatility': volatility,
                            'risk_adjusted_return': momentum / volatility if volatility != 0 else 0
                        }
                except Exception as e:
                    print(f"Error fetching data for {stock}: {str(e)}")
            
            # Sort stocks by risk-adjusted return
            sorted_stocks = sorted(
                stock_data.items(),
                key=lambda x: x[1]['risk_adjusted_return'],
                reverse=True
            )
            
            # Add top stocks from sector to recommendations
            for stock, metrics in sorted_stocks[:num_stocks_per_sector]:
                recommendations.append({
                    'stock': stock,
                    'sector': sector,
                    'sector_score': top_sectors.loc[sector, 'composite_score'],
                    'return': metrics['return'],
                    'volatility': metrics['volatility'],
                    'risk_adjusted_return': metrics['risk_adjusted_return']
                })
        
        return recommendations

def main():
    # Initialize recommender
    recommender = SectorRecommender()
    
    print("Fetching sector data...")
    sector_data = recommender.fetch_sector_data()

    # print(sector_data)
    
    print("\nCalculating sector metrics...")
    metrics = recommender.calculate_sector_metrics(sector_data)

    print(metrics)

    print("\nIdentifying top sectors...")
    top_sectors = recommender.get_top_sectors(metrics)
    
    print("\nTop Performing Sectors:")
    print("----------------------")
    for sector in top_sectors.index:
        print(f"\n{sector}:")
        print(f"Composite Score: {top_sectors.loc[sector, 'composite_score']:.4f}")
        print(f"Return: {metrics[sector]['return']:.2%}")
        print(f"RSI: {metrics[sector]['rsi']:.2f}")
        print(f"Risk-Adjusted Return: {metrics[sector]['risk_adjusted_return']:.4f}")
    
    print("\nGetting stock recommendations...")
    recommendations = recommender.get_sector_recommendations(top_sectors)
    
    print("\nStock Recommendations:")
    print("---------------------")
    for rec in recommendations:
        print(f"\nStock: {rec['stock']}")
        print(f"Sector: {rec['sector']}")
        print(f"1-Month Return: {rec['return']:.2%}")
        print(f"Risk-Adjusted Return: {rec['risk_adjusted_return']:.4f}")

if __name__ == "__main__":
    main()