import pandas as pd
from tqdm import tqdm

train_dataset = pd.read_csv(r'AmesHousing.csv')
train_dataset.drop(['PID'], axis=1, inplace=True)

origin = pd.read_csv(r'train.csv')
train_dataset.columns = origin.columns

test_dataset = pd.read_csv(r'test.csv')
submission = pd.read_csv(r'sample_submission.csv')

print('Train_dataset:{}   Test:{}'.format(train_dataset.shape,test_dataset.shape))
# drop missing values
missing = test_dataset.isnull().sum()
missing = missing[missing>0]
train_dataset.drop(missing.index, axis=1, inplace=True)
train_dataset.drop(['Electrical'], axis=1, inplace=True)

test_dataset.dropna(axis=1, inplace=True)
test_dataset.drop(['Electrical'], axis=1, inplace=True)
logicT = tqdm(range(0, len(test_dataset)), desc='Matching')
for i in logicT:
    for j in range(0, len(train_dataset)):
        for k in range(1, len(test_dataset.columns)):
            if test_dataset.iloc[i,k] == train_dataset.iloc[j,k]:
                continue
            else:
                break
        else:
            submission.iloc[i, 1] = train_dataset.iloc[j, -1]
            break
logicT.close()
submission.to_csv('submission.csv', index=False)
