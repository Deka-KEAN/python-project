import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

class FinancialRecommender:
    def __init__(self):
        self.user_holdings = {}
        self.instrument_features = {}
        self.similarity_matrix = None
        
    def add_user_holdings(self, user_id, holdings):
        """
        Add user holdings data
        holdings: dict with instrument_id as key and holding details as value
        """
        self.user_holdings[user_id] = holdings
        
    def add_instrument_features(self, instrument_data):
        """
        Add instrument features for similarity calculation
        instrument_data: DataFrame with columns:
        - instrument_id
        - sector
        - market_cap
        - pe_ratio
        - dividend_yield
        - volatility
        - beta
        """
        # Convert categorical variables to dummy variables
        sector_dummies = pd.get_dummies(instrument_data['sector'])
        
        # Normalize numerical features
        numerical_features = ['market_cap', 'pe_ratio', 'dividend_yield', 'volatility', 'beta']
        normalized_features = instrument_data[numerical_features].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        
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
        
    def get_recommendations(self, user_id, n_recommendations=5):
        """
        Generate recommendations for a user based on their current holdings
        """
        if user_id not in self.user_holdings:
            raise ValueError("User holdings not found")
            
        # Get user's current holdings
        current_holdings = set(self.user_holdings[user_id].keys())
        
        # Calculate recommendation scores
        recommendation_scores = defaultdict(float)
        
        for held_instrument in current_holdings:
            held_idx = list(self.instrument_features.keys()).index(held_instrument)
            
            # Get similar instruments
            similarities = self.similarity_matrix[held_idx]
            
            # Add similarity scores to recommendation scores
            for idx, score in enumerate(similarities):
                instrument_id = list(self.instrument_features.keys())[idx]
                if instrument_id not in current_holdings:
                    recommendation_scores[instrument_id] += score
                    
        # Sort recommendations by score
        recommendations = sorted(
            recommendation_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return recommendations
    
    def explain_recommendation(self, recommended_id, user_holdings):
        """
        Provide explanation for why an instrument was recommended
        """
        rec_idx = list(self.instrument_features.keys()).index(recommended_id)
        explanations = []
        
        for held_id in user_holdings:
            held_idx = list(self.instrument_features.keys()).index(held_id)
            similarity = self.similarity_matrix[held_idx][rec_idx]
            
            if similarity > 0.7:  # Threshold for significant similarity
                explanations.append(f"Similar to your holding {held_id} (similarity: {similarity:.2f})")
                
        return explanations

# Example usage
def demo_recommender():
    # Create sample data
    instrument_data = pd.DataFrame({
        'instrument_id': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'NFLX', 'TSLA'],
        'sector': ['Technology', 'Technology', 'Technology', 'Consumer', 'Technology', 'Technology', 'Automotive'],
        'market_cap': [2000, 1500, 1800, 1600, 800, 300, 700],
        'pe_ratio': [25, 28, 30, 70, 25, 90, 100],
        'dividend_yield': [0.5, 0, 1, 0, 0, 0, 0],
        'volatility': [0.2, 0.25, 0.2, 0.3, 0.35, 0.4, 0.5],
        'beta': [1.1, 1.2, 1.0, 1.3, 1.4, 1.6, 1.8]
    })
    
    # Initialize recommender
    recommender = FinancialRecommender()
    
    # Add instrument features
    recommender.add_instrument_features(instrument_data)
    
    # Add user holdings
    user_holdings = {
        'user1': {
            'AAPL': {'quantity': 100, 'purchase_price': 150},
            'GOOGL': {'quantity': 50, 'purchase_price': 2500}
        }
    }
    recommender.add_user_holdings('user1', user_holdings['user1'])
    
    # Get recommendations
    recommendations = recommender.get_recommendations('user1')
    
    # Get explanations
    for instrument_id, score in recommendations:
        print(f"\nRecommendation: {instrument_id} (Score: {score:.2f})")
        explanations = recommender.explain_recommendation(instrument_id, user_holdings['user1'])
        for explanation in explanations:
            print(f"- {explanation}")
            
    return recommender

if __name__ == "__main__":
    demo_recommender()