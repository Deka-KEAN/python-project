import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from datetime import datetime, timedelta

class FinancialRecommender:
    def __init__(self):
        self.user_holdings = {}
        self.instrument_features = {}
        self.similarity_matrix = None
        self.sector_performance = {}
        self.sector_momentum = {}
        
    def add_market_data(self, market_data):
        """
        Add historical market data for sector analysis
        market_data: DataFrame with columns:
        - date
        - instrument_id
        - sector
        - price
        - volume
        """
        # Calculate sector performance
        self._calculate_sector_metrics(market_data)
        
    def _calculate_sector_metrics(self, market_data):
        """
        Calculate various sector performance metrics
        """
        # Convert date to datetime if it's not already
        market_data['date'] = pd.to_datetime(market_data['date'])
        
        # Calculate daily returns
        market_data['daily_return'] = market_data.groupby('instrument_id')['price'].pct_change()
        
        # Get the latest date in the data
        latest_date = market_data['date'].max()
        
        # Time windows for analysis (in days)
        windows = {
            'week': 7,
            'month': 30,
            'quarter': 90
        }
        
        # Calculate sector performance for different time windows
        self.sector_performance = {}
        self.sector_momentum = {}
        
        for window_name, days in windows.items():
            start_date = latest_date - timedelta(days=days)
            window_data = market_data[market_data['date'] >= start_date]
            
            # Calculate sector returns
            sector_returns = window_data.groupby('sector')['daily_return'].agg([
                ('return', lambda x: (1 + x).prod() - 1),
                ('volatility', 'std'),
                ('volume_change', lambda x: window_data.groupby('sector')['volume'].pct_change().mean())
            ])
            
            # Calculate momentum score
            sector_returns['momentum_score'] = (
                sector_returns['return'] / sector_returns['volatility'] * 
                (1 + sector_returns['volume_change'])
            )
            
            self.sector_performance[window_name] = sector_returns
            
            # Store sector momentum rankings
            self.sector_momentum[window_name] = sector_returns['momentum_score'].rank(ascending=False)

    def get_trending_sectors(self, timeframe='month', top_n=3):
        """
        Get the top trending sectors based on momentum
        """
        if timeframe not in self.sector_momentum:
            raise ValueError(f"Invalid timeframe. Choose from: {list(self.sector_momentum.keys())}")
            
        momentum_ranks = self.sector_momentum[timeframe]
        top_sectors = momentum_ranks.nsmallest(top_n).index.tolist()
        
        # Get detailed performance metrics for top sectors
        performance = self.sector_performance[timeframe].loc[top_sectors]
        
        return {
            sector: {
                'rank': momentum_ranks[sector],
                'return': performance.loc[sector, 'return'],
                'volatility': performance.loc[sector, 'volatility'],
                'momentum_score': performance.loc[sector, 'momentum_score']
            }
            for sector in top_sectors
        }
    
    def add_instrument_features(self, instrument_data):
        """
        Enhanced version that includes sector momentum in features
        """
        # Convert categorical variables to dummy variables
        sector_dummies = pd.get_dummies(instrument_data['sector'])
        
        # Normalize numerical features
        numerical_features = ['market_cap', 'pe_ratio', 'dividend_yield', 'volatility', 'beta']
        normalized_features = instrument_data[numerical_features].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )
        
        # Add sector momentum scores if available
        if self.sector_momentum:
            # Use monthly momentum by default
            sector_scores = pd.Series(
                index=instrument_data['sector'],
                data=instrument_data['sector'].map(
                    lambda x: self.sector_performance['month'].loc[x, 'momentum_score']
                )
            )
            normalized_features['sector_momentum'] = (
                sector_scores - sector_scores.min()
            ) / (sector_scores.max() - sector_scores.min())
        
        # Combine features
        features = pd.concat([normalized_features, sector_dummies], axis=1)
        
        # Create dictionary with instrument_id as key and features as value
        self.instrument_features = {
            instrument_id: features.loc[idx].values 
            for idx, instrument_id in enumerate(instrument_data['instrument_id'])
        }
        
        # Calculate similarity matrix
        feature_matrix = np.array([features for features in self.instrument_features.values()])
        self.similarity_matrix = cosine_similarity(feature_matrix)
    
    def get_sector_based_recommendations(self, n_recommendations=5, timeframe='month'):
        """
        Get recommendations based on trending sectors
        """
        trending_sectors = self.get_trending_sectors(timeframe=timeframe)
        recommendations = []
        
        # Get instrument features DataFrame
        feature_df = pd.DataFrame(self.instrument_features).T
        
        for sector in trending_sectors:
            # Filter instruments in the trending sector
            sector_instruments = feature_df[feature_df[sector] == 1]
            
            # Sort by sector momentum if available
            if 'sector_momentum' in feature_df.columns:
                sector_instruments = sector_instruments.sort_values('sector_momentum', ascending=False)
            
            # Get top instruments from sector
            top_sector_instruments = sector_instruments.head(
                max(1, n_recommendations // len(trending_sectors))
            )
            
            for instrument_id in top_sector_instruments.index:
                recommendations.append({
                    'instrument_id': instrument_id,
                    'sector': sector,
                    'sector_metrics': trending_sectors[sector]
                })
        
        return recommendations[:n_recommendations]

# Example usage
def demo_recommender_with_trends():
    # Create sample historical market data
    dates = pd.date_range(end=pd.Timestamp.now(), periods=90, freq='D')
    instruments = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'NFLX', 'TSLA']
    sectors = ['Technology', 'Technology', 'Technology', 'Consumer', 'Technology', 'Technology', 'Automotive']
    
    # Generate sample market data
    market_data = []
    for instrument, sector in zip(instruments, sectors):
        base_price = np.random.uniform(100, 1000)
        for date in dates:
            price = base_price * (1 + np.random.normal(0, 0.02))
            volume = np.random.uniform(1000000, 5000000)
            market_data.append({
                'date': date,
                'instrument_id': instrument,
                'sector': sector,
                'price': price,
                'volume': volume
            })
    
    market_data = pd.DataFrame(market_data)
    
    # Create sample instrument data
    instrument_data = pd.DataFrame({
        'instrument_id': instruments,
        'sector': sectors,
        'market_cap': [2000, 1500, 1800, 1600, 800, 300, 700],
        'pe_ratio': [25, 28, 30, 70, 25, 90, 100],
        'dividend_yield': [0.5, 0, 1, 0, 0, 0, 0],
        'volatility': [0.2, 0.25, 0.2, 0.3, 0.35, 0.4, 0.5],
        'beta': [1.1, 1.2, 1.0, 1.3, 1.4, 1.6, 1.8]
    })
    
    # Initialize and set up recommender
    recommender = FinancialRecommender()
    recommender.add_market_data(market_data)
    recommender.add_instrument_features(instrument_data)
    
    # Get trending sectors
    print("\nTrending Sectors:")
    trending_sectors = recommender.get_trending_sectors()
    for sector, metrics in trending_sectors.items():
        print(f"\n{sector}:")
        print(f"Rank: {metrics['rank']}")
        print(f"Return: {metrics['return']:.2%}")
        print(f"Momentum Score: {metrics['momentum_score']:.2f}")
    
    # Get sector-based recommendations
    print("\nSector-Based Recommendations:")
    recommendations = recommender.get_sector_based_recommendations()
    for rec in recommendations:
        print(f"\nRecommended: {rec['instrument_id']}")
        print(f"Sector: {rec['sector']}")
        print(f"Sector Momentum Rank: {rec['sector_metrics']['rank']}")
        print(f"Sector Return: {rec['sector_metrics']['return']:.2%}")
    
    return recommender

if __name__ == "__main__":
    demo_recommender_with_trends()