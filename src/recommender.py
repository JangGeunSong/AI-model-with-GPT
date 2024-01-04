import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

# Step 1: Load Data
# For this example, let's assume you have 'ratings.csv' with columns: 'userID', 'itemID', and 'rating'
data = pd.read_csv('file_path')

# Step 2: Process Data
# Convert the running list of user ratings into a matrix
ratings_matrix = data.pivot_table(index='userID', columns='itemID', values='rating')

# Fill missing values with 0s
ratings_matrix.fillna(0, inplace=True)

# Step 3: Build Model
# Calculate cosine similarity between items
item_similarity = cosine_similarity(ratings_matrix.T)

# Convert into a DataFrame
item_similarity_df = pd.DataFrame(item_similarity, index=ratings_matrix.columns, columns=ratings_matrix.columns)

# Step 4: Make Predictions
def get_similar_items(item_id, user_rating):
    similar_score = item_similarity_df[item_id] * (user_rating - 2.5) # Adjusting by mean rating
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score

# Let's say a user has rated three items:
user_rating = [
        ("쇼생크 탈출(1994)", 10), ("스파이더맨: 어크로스 더 유니버스(2023)", 3), ("12인의 성난 사람들(1957)", 5), ("대부(1972)", 7), ("펄프 픽션(1994)", 3), ("인셉션(2010)", 8)
    ]

similar_items = pd.DataFrame()
for item, rating in user_rating:
    similar_items = pd.concat([similar_items, get_similar_items(item, rating)], ignore_index=True)

# Summing up the similarity scores for the items
recommandation = similar_items.sum().sort_values(ascending=False)

# Convert the series to a DataFrame for better readability and include item names
recommandation_df = recommandation.to_frame(name='score')
recommandation_df.index.name = 'itemID'
recommandation_df.reset_index(inplace=True)

print("Recommanded items:")
print(recommandation_df.head()) # Show top 5 recommandations