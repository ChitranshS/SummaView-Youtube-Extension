from urllib.parse import urlparse, parse_qs
def commenter(url):
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

    # Set your API key here
    api_key = 'AIzaSyCAWqqd43cGIsFQbXUNYd3cSowwB4gIwF4'

    # Create a YouTube Data API client
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
        
    unique_comments = list(dict.fromkeys(doc_complete))
    import re

    def remove_emojis(text):
        emoji_pattern = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002500-\U00002BEF"  # chinese char
                                u"\U00002702-\U000027B0"
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u"\U00010000-\U0010ffff"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u200d"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\ufe0f"  # dingbats
                                u"\u3030"
                                "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    doc_complete_noemoji = []
    for line in unique_comments:
        doc_complete_noemoji.append(remove_emojis(line))

    from nltk.corpus import stopwords
    from nltk.stem.wordnet import WordNetLemmatizer
    import string
    stop = set(stopwords.words('english'))
    stop.update(stopwords.words('hinglish'))
    stop.update(stopwords.words('hindi'))


    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split() if len(word) > 3)
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete_noemoji]  


    # Importing Gensim
    import gensim
    from gensim import corpora
    from gensim.models import CoherenceModel


    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)

    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.LdaModel
    num_topics=4
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=12,alpha = 0.2,eta=0.84)

    highlighted_words =[]
    dominant_topics_list = []
    import re
    import pandas as pd


    # Using regular expression to extract the word after the first star until the plus sign
    for i in range(num_topics):
        text = ldamodel.print_topics()[i][1]
        match = re.search(r'\*(.*?)\+', text)
        if match:
            extracted_word = match.group(1).strip()
            highlighted_words.append(re.sub(r'\"(.*?)\"', r'\1', extracted_word))
        else:
            print("No match found.")

    for i,row in enumerate(ldamodel[doc_term_matrix]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        topic_num, prop_topic = row[0]
        wp = ldamodel.show_topic(topic_num)
        topic_keywords = ", ".join([word for word, prop in wp])
        dominant_topics_list.append(topic_keywords)
    dominant_topics_list_unique = list(dict.fromkeys(dominant_topics_list))
    dominant_topics_unique = list(dict.fromkeys(word.strip() for sentence in dominant_topics_list for word in sentence.split(',')))
    sending_result = {"text":dominant_topics_unique}
    return sending_result
