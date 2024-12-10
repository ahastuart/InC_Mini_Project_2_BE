import boto3

# AWS Comprehend 클라이언트 생성
comprehend = boto3.client('comprehend', region_name='ap-northeast-2')

def analyze_dream_content(dream_text, language_code='en'):
    """
    꿈 내용을 분석하여 감정 분석 결과와 키워드를 반환

    Parameters:
        dream_text (str): 분석할 텍스트
        language_code (str): 텍스트 언어 코드 

    Returns:
        dict: {
            "negative": float,
            "positive": float,
            "neutral": float,
            "mixed": float,
            "sentiment": str,
            "keyword": str
        }
    """
    if not dream_text:
        raise ValueError("꿈 내용이 비어 있습니다. 텍스트를 입력하세요.")

    try:
        # 1. 감정 분석
        sentiment_response = comprehend.detect_sentiment(
            Text=dream_text,
            LanguageCode=language_code
        )
        sentiment_scores = sentiment_response['SentimentScore']
        sentiment = sentiment_response['Sentiment'] 

        # 2. 키워드 도출
        key_phrases_response = comprehend.detect_key_phrases(
            Text=dream_text,
            LanguageCode=language_code
        )
        key_phrases = [
            {'Text': phrase['Text'], 'Score': phrase['Score']}
            for phrase in key_phrases_response['KeyPhrases']
        ]

        # 가장 높은 신뢰도의 키워드 선택
        keyword = (
            max(key_phrases, key=lambda x: x['Score'])['Text']
            if key_phrases else None
        )

        # 결과 반환
        return {
            "negative": sentiment_scores['Negative'],
            "positive": sentiment_scores['Positive'],
            "neutral": sentiment_scores['Neutral'],
            "mixed": sentiment_scores['Mixed'],
            "sentiment": sentiment,
            "keyword": keyword
        }

    except Exception as e:
        raise RuntimeError(f"Comprehend 처리 중 오류 발생: {e}")
