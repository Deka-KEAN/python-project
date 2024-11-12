import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Function to generate a single portfolio
def generate_portfolio():
    portfolio_id = fake.uuid4()
    portfolio_name = fake.company()
    creation_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
    risk_tolerance = random.choice(['Low', 'Moderate', 'High'])
    goal_type = random.choice(['Growth', 'Income', 'Preservation'])
    investment_strategy = random.choice(['Aggressive', 'Balanced', 'Conservative'])
    total_asset_value = round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2)

    asset_distribution = [
        {'Asset_Type': 'Stocks', 'Percentage': round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)},
        {'Asset_Type': 'Bonds', 'Percentage': round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)},
        {'Asset_Type': 'Cash', 'Percentage': round(fake.pyfloat(left_digits=2, right_digits=1, positive=True), 1)}
    ]

    transactions = [
        {
            'Transaction_ID': fake.uuid4(),
            'Asset_ID': fake.uuid4(),
            'Transaction_Type': random.choice(['Buy', 'Sell']),
            'Transaction_Date': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
            'Transaction_Amount': round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2),
            'Units': fake.pyint(min_value=1, max_value=100),
            'Transaction_Price': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'Total_Transaction_Value': round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2),
            'Transaction_Fees': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
        } for _ in range(random.randint(1, 5))
    ]

    performance_metrics = [
        {
            'Performance_ID': fake.uuid4(),
            'Asset_ID': fake.uuid4(),
            'Time_Period': f'Q{fake.pyint(min_value=1, max_value=4)} {fake.year()}',
            'Return_Percentage': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
            'Price_Change': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'Risk_Adjusted_Return': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
            'Benchmark_Performance': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
            'Dividend_Payouts': round(fake.pyfloat(left_digits=4, right_digits=2, positive=True), 2)
        } for _ in range(random.randint(1, 4))
    ]

    return {
        'Portfolio_ID': portfolio_id,
        'Portfolio_Name': portfolio_name,
        'Creation_Date': creation_date,
        'Risk_Tolerance': risk_tolerance,
        'Goal_Type': goal_type,
        'Investment_Strategy': investment_strategy,
        'Total_Asset_Value': total_asset_value,
        'Asset_Distribution': asset_distribution,
        'Transactions': transactions,
        'Performance_Metrics': performance_metrics
    }

# Generate user data
user = {
    'User_ID': 1,
    'Name': fake.name(),
    'Age': fake.pyint(min_value=18, max_value=65),
    'Gender': random.choice(['Male', 'Female', 'Non-binary']),
    'Location': f"{fake.city()}, {fake.state()}",
    'Occupation': fake.job(),
    'Income_Bracket': random.choice(['Low', 'Middle', 'High']),
    'Investment_Experience_Level': random.choice(['Beginner', 'Intermediate', 'Advanced']),
    'Ethical_Preferences': random.choice(['Environmental', 'Social', 'Governance']),
    'Financial_Goals': random.choice(['Retirement', 'Wealth Accumulation', 'Debt Reduction']),
    'Risk_Tolerance': random.choice(['Low', 'Moderate', 'High']),
    'Portfolios': [generate_portfolio() for _ in range(random.randint(1, 3))]
}

# Generate investment asset data
investment_asset = {
    'Asset_ID': fake.uuid4(),
    'Asset_Name': fake.company(),
    'Ticker_Symbol': fake.lexify('????').upper(),
    'Asset_Type': random.choice(['Equity', 'Bond', 'ETF', 'Mutual Fund']),
    'Sector': fake.job(),
    'Market': random.choice(['NYSE', 'NASDAQ', 'LSE']),
    'Risk_Level': random.choice(['Low', 'Moderate', 'High']),
    'Expected_Return_Rate': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
    'Dividend_Yield': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
    'ESG_Score': fake.pyint(min_value=0, max_value=100),
    'Ethical_Alignment': random.choice(['Environmental', 'Social', 'Governance']),
    'Market_Cap': round(fake.pyfloat(left_digits=9, right_digits=2, positive=True), 2),
    'Inception_Date': fake.date_between(start_date='-20y', end_date='today').strftime('%Y-%m-%d'),
    'Market_Data_and_Trends': [
        {
            'Market_Data_ID': fake.uuid4(),
            'Date': (datetime.now() - timedelta(days=fake.pyint(min_value=1, max_value=365))).strftime('%Y-%m-%d'),
            'Open_Price': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'Close_Price': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'High_Price': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'Low_Price': round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            'Trading_Volume': fake.pyint(min_value=1000, max_value=1000000),
            'News_Sentiment_Score': round(fake.pyfloat(left_digits=1, right_digits=1, positive=True), 1),
            'Social_Media_Sentiment_Score': round(fake.pyfloat(left_digits=1, right_digits=1, positive=True), 1)
        } for _ in range(random.randint(1, 5))
    ],
    'Ethical_and_Sustainable_Investment': {
        'Ethical_Investment_ID': fake.uuid4(),
        'ESG_Score': fake.pyint(min_value=0, max_value=100),
        'Environmental_Impact': random.choice(['Low', 'Moderate', 'High']),
        'Social_Impact': random.choice(['Positive', 'Neutral', 'Negative']),
        'Governance_Score': round(fake.pyfloat(left_digits=1, right_digits=1, positive=True), 1),
        'Cause_Alignment': random.choice(['Climate Change', 'Human Rights', 'Corporate Governance']),
        'Sustainability_Certification': random.choice(['Certified B Corp', 'LEED Certified', 'ISO 14001'])
    }
}

# Generate investment recommendation
investment_recommendation = {
    'Recommendation_ID': fake.uuid4(),
    'User_ID': user['User_ID'],
    'Portfolio_ID': user['Portfolios'][0]['Portfolio_ID'],
    'Asset_ID': investment_asset['Asset_ID'],
    'Recommendation_Date': fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
    'Reason': fake.sentence(nb_words=10),
    'Expected_Return': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
    'Risk_Level': random.choice(['Low', 'Moderate', 'High']),
    'Ethical_Alignment': random.choice(['Environmental', 'Social', 'Governance']),
    'Investment_Horizon': f"{fake.pyint(min_value=1, max_value=10)} years"
}

# Generate dashboard layout
dashboard_layout = {
    'Layout_ID': fake.uuid4(),
    'User_ID': user['User_ID'],
    'Section_Order': [
        {'Section': 'Portfolio Summary', 'Order': 1},
        {'Section': 'Investment Recommendations', 'Order': 2},
        {'Section': 'Performance Metrics', 'Order': 3},
        {'Section': 'Asset Details', 'Order': 4}
    ],
    'Most_Used_Sections': ['Portfolio Summary', 'Performance Metrics', 'Asset Details'],
    'User_Customization': {
        'Theme': random.choice(['Light', 'Dark']),
        'Font_Size': random.choice(['Small', 'Medium', 'Large'])
    },
    'Preferred_View_Mode': random.choice(['Grid', 'List'])
}

# Generate educational resource
educational_resource = {
    'Resource_ID': fake.uuid4(),
    'Content_Type': 'Article',
    'Topic': 'Investing Basics',
    'Difficulty_Level': random.choice(['Beginner', 'Intermediate', 'Advanced']),
    'URL': 'https://example.com/investing-basics',
    'Recommended_Users': [user['User_ID'], fake.pyint(min_value=2, max_value=100)],
    'Engagement_Rate': round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
}

# Generate user behavior and preferences
user_behavior_and_preferences = {
    'User_ID': user['User_ID'],
    'Preferred_Asset_Types': random.sample(['Equities', 'Bonds', 'ETFs', 'Mutual Funds'], k=random.randint(1, 4)),
    'Historical_Investment_Choices': [
        {
            'Asset_ID': investment_asset['Asset_ID'],
            'Amount_Invested': round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2)
        } for _ in range(random.randint(1, 5))
    ],
    'Sector_Preferences': random.sample(['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Goods'], k=random.randint(1, 3)),
    'Sentiment_Sensitivity': round(fake.pyfloat(left_digits=1, right_digits=1, positive=True), 1),
    'Content_Consumption_Habits': {
        'Articles_Read': fake.pyint(min_value=0, max_value=50),
        'Videos_Watched': fake.pyint(min_value=0, max_value=30)
    },
    'Learning_Preferences': random.sample(['Text', 'Video', 'Audio'], k=random.randint(1, 3))
}

# Combine all the data into a single dictionary
synthetic_data = {
    'User': user,
    'Investment_Asset': investment_asset,
    'Investment_Recommendation': investment_recommendation,
    'Dashboard_Layout': dashboard_layout,
    'Educational_Resources': educational_resource,
    'User_Behavior_and_Preferences': user_behavior_and_preferences
}

print(synthetic_data)