import tweepy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
bearer_token = os.getenv("X_ACCESS_TOKEN")
# consumer_key = os.getenv("X_API_KEY") # Not strictly needed for bearer token auth / recent search
# consumer_secret = os.getenv("X_API_SECRET") # Not strictly needed for bearer token auth / recent search

# Using App-only authentication (Bearer Token)
client = tweepy.Client(bearer_token=bearer_token)

search_query = "feminism"

try:
    # Search for recent tweets.
    # You can use max_results to get more (up to 100 per request for standard access).
    # You can also specify tweet_fields like before.
    response = client.search_recent_tweets(
        search_query, 
        tweet_fields=["text", "created_at", "author_id"],
        max_results=10 # Fetch up to 10 tweets
    )

    if response.data:
        print(f"Found {len(response.data)} tweet(s) for query: '{search_query}'\n")
        for tweet in response.data:
            print(f"Tweet ID: {tweet.id}")
            print(f"Author ID: {tweet.author_id}")
            print(f"Created at: {tweet.created_at}")
            print(f"Text: {tweet.text}")
            print("---")
    else:
        print(f"No recent tweets found for query: '{search_query}'")
        if response.errors:
            print("Errors:")
            for error in response.errors:
                print(f"- {error}")

except tweepy.TweepyException as e:
    print(f"Error during Tweepy operation: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
