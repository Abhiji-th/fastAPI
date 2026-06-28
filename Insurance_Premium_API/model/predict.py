import pickle
import pandas as pd

with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

class_list = model.classes_.tolist()

def predict(data):
    input_df = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    predicted_class = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    confidence = float(max(probabilities))

    categories = dict(zip(class_list, map(lambda x: float(round(x, 4)), probabilities)))

    return {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'categories': categories
    }