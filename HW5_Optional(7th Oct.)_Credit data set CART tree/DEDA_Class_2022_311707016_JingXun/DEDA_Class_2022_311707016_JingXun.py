import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

credit = pd.read_csv('data_sample.csv')
credit.columns = 'Cash, Inventories, Current Assets, Tangible Assets, Intangible Assets, Total Assets, Accounts Receivable, Lands and Buildings, Equity, Accrual for Pension Liabilities, Total Current Liabilities, Total Longterm Liabilities, Bank Debt, Accounts Payable, Sales, Amortization Depreciation, Interest Expenses, EBIT, Operating Income, Net Income, Increase Inventories, Increase Liabilities, Increase Cash, Number Employees, Insolvent'.split(', ')

X = credit.drop('Insolvent', axis=1)
y = credit['Insolvent']

DTClassifier = DecisionTreeClassifier(max_depth=4)
DTClassifier.fit(X, y)
fig = plt.figure(figsize=(20, 20))
tree.plot_tree(
    DTClassifier,
    feature_names=credit.columns,
    class_names=['solvent', 'insolvent'],
    filled=True
)

fig.savefig('decision_tree_creditreform.png', transparent=True)