from src.preparation.data_access.obtained_text_da import ObtainedTextDA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from src.modeling.utils.utils import print_scores
from src.processing.constants import BASE_DIRECTORY

import pickle

print(BASE_DIRECTORY)
texts = ObtainedTextDA().select_all_as_dataframe().drop(columns=['id', 'filename', 'category', 'cluster_grade'])
data_columns = [c for c in texts.columns if c not in ['category', 'filename', 'grade', 'id']]
# SCALER
scaler = MinMaxScaler()
scaler.fit(texts[data_columns])

texts[data_columns] = scaler.transform(texts[data_columns])
# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(texts.drop(columns=['grade']), texts[['grade']], random_state=43, test_size=0.2, stratify=texts[['grade']])
# MODEL TRAINING
knn = KNeighborsClassifier(algorithm='auto', n_neighbors=1, p=1, weights='uniform')
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print_scores(y_test, y_pred)

pickle.dump(knn, open(f'{BASE_DIRECTORY}/model/classifier.pkl', 'ab'))
pickle.dump(scaler, open(f'{BASE_DIRECTORY}/model/scaler.pkl', 'ab'))