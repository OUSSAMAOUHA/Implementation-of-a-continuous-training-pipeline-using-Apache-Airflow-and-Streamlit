import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle

# Load your dataset
# Assuming 'Weather_Data.csv' is the name of your CSV file and 'Description' is the name of your target column
# data = pd.read_csv("/opt/airflow/dags/scripts/Weather_Data.csv")
data = pd.read_csv("/opt/airflow/dags/scripts/dataset/Weather_Data.csv")


# Drop unnecessary columns
data = data.drop(['Date', 'City', 'Country'], axis=1).dropna()

# Encode the target variable 'Description'
label_encoder = LabelEncoder()
data['Description'] = label_encoder.fit_transform(data['Description'])

# Separate features and target
X = data.drop('Description', axis=1)
y = data['Description']

# Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)


# Specify the merge parameters
new_data = pd.merge(X_train, y_train, how='inner', on=None, left_index=True, right_index=True, validate=None)


# Undersample the majority class using RandomUnderSampler
undersampler = RandomUnderSampler(sampling_strategy='not minority', random_state=42)
X_train_balanced, y_train_balanced = undersampler.fit_resample(X_train, y_train)

# Display class distribution after balancing
print("Class distribution after balancing:", Counter(y_train_balanced))

# Scale numerical features
scaler = StandardScaler()
X_train_balanced_scaled = scaler.fit_transform(X_train_balanced)
X_test_scaled = scaler.transform(X_test)

# Save the LabelEncoder
with open('label_encoder.pkl', 'wb') as encoder_file:
    pickle.dump(label_encoder, encoder_file)

# Train different models on the balanced and scaled dataset
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "SVM": SVC(kernel='linear', random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
    "Decision Tree": DecisionTreeClassifier(criterion='entropy', random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=40, random_state=42),
    "XGBoost": XGBClassifier()
}

results = {}

for model_name, model in models.items():
    model.fit(X_train_balanced_scaled, y_train_balanced)
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    results[model_name] = accuracy

# Find the best model
best_model_name = max(results, key=results.get)
best_accuracy = results[best_model_name]

print("Results:")
for model, accuracy in results.items():
    print(f"{model}: {accuracy:.2%}")

print(f"Best Model: {best_model_name} with Accuracy: {best_accuracy:.2%}")

# Save the best model as a pickle file with a new name
new_file_name = 'dags\scripts\pickle_files\modele_classification13.pkl'
with open(new_file_name, 'wb') as file:
    pickle.dump(models[best_model_name], file)
