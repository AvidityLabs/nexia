def rename_sentiment_labels(data):
    labels = {'LABEL_0': 'negative', 'LABEL_1': 'neutral', 'LABEL_2': 'positive'}
    for item in data:
        for label in item:
            label['label'] = labels[label['label']]
            label['percentage'] = round(label['score'] * 100, 2)
    return data

def add_emotion_percentages(scores_list):
    for item in scores_list:
        total_score = sum([x['score'] for x in item])
        for obj in item:
            obj['percentage'] = round(obj['score'] / total_score * 100, 2)
    return scores_list
