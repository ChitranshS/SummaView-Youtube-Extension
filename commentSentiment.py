from urllib.parse import urlparse, parse_qs
from config import youtube_api_key
def commentSent(url):
    def extract_video_id(youtube_url):
        # Parse the URL
        parsed_url = urlparse(youtube_url)
        
        # Extract the query parameters
        query_params = parse_qs(parsed_url.query)
        
        # Retrieve the 'v' parameter (video ID)
        video_id = query_params.get('v')
        
        if video_id:
            return video_id[0]
        else:
            return None

    # YouTube URL
    youtube_url = url

    # Extract the video ID
    video_id = extract_video_id(youtube_url)

    import os
    import googleapiclient.discovery

    api_key = youtube_api_key

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    # Request comments for the specified video with pagination
    next_page_token = None
    comments = []

    while True:
        response = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=next_page_token
        ).execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if there are more pages to retrieve
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    doc_complete = []
    for comment in comments:
        doc_complete.append(comment)
        
    from collections import Counter
    counted = Counter(doc_complete)
    spam_comments = [sentence for sentence, count in counted.items() if count > 1]
    spam_number = [count for sentence, count in counted.items() if count >= 2]
    spam_number_total =0
    for i in spam_number:
        i-=1
        spam_number_total +=i
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    analyzer = SentimentIntensityAnalyzer()
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    # Create an instance of the Vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    sentiment_data =[]
    # Loop through the texts and get the sentiment scores for each one
    for comment in comments:
        scores = analyzer.polarity_scores(comment)
        sentiment_data.append({"comment":comment,"scores":scores})
    pos_number = 0
    pos_sum = 0
    neg_number = 0
    neg_sum = 0
    neutral_number = 0
    for doc in sentiment_data:
        if(doc['scores']['compound'] > 0.0):
            pos_number+=1
            pos_sum+=doc['scores']['compound']
        if(doc['scores']['compound'] < 0.0):
            neg_number+=1
            neg_sum-=doc['scores']['compound']
        if(doc['scores']['compound'] == 0.0):
            neutral_number+=1
    # Percentage breakdown:
    pos_per = (pos_number/len(comments))*100
    neg_per = (neg_number/len(comments))*100
    neutral_per = (neutral_number/len(comments))*100
    dominance_1 = min(pos_per,neg_per,neutral_per)
    dominance_1
    if pos_per > neg_per and pos_per > neutral_per:
        overall_sentiment = 'Positive'
    elif neg_per > pos_per and neg_per > neutral_per:
        overall_sentiment = 'Negative'
    elif neutral_per > pos_per and neutral_per > neg_per:
        overall_sentiment = 'Neutral'
    else:
        overall_sentiment = 'Mixed' 
        
    total_unique_comments = len(comments)-spam_number_total
    sending_result = {"overall":overall_sentiment,
                        "numbers":{"pos":pos_number,"neg":neg_number,"neutral":neutral_number},
                        "per":{"pos":pos_per,"neg":neg_per,"neutral":neutral_per},
                        "spam":spam_number_total,
                        "unique":total_unique_comments}
    return sending_result 