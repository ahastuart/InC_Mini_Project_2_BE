# def create_sentiment_chart_text(analysis_result):
#     """
#     감정 분석 결과를 텍스트 기반으로 시각화합니다.

#     Parameters:
#         analysis_result (dict): 감정 분석 결과

#     Returns:
#         str: 텍스트 기반의 감정 비율 표시
#     """
#     labels = ['Positive', 'Negative', 'Neutral', 'Mixed']
#     scores = [
#         analysis_result['positive'],
#         analysis_result['negative'],
#         analysis_result['neutral'],
#         analysis_result['mixed']
#     ]
    
#     # 텍스트 기반 출력 생성
#     chart = "\nSentiment Analysis Results:\n"
#     total = sum(scores)  # 모든 감정 점수의 합
#     for label, score in zip(labels, scores):
#         percentage = (score / total) * 100 if total > 0 else 0
#         chart += f"{label}: {percentage:.1f}%\n"

#     return chart
#test
