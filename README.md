# FundamentalsPythonBot
Python application which models the stocks market regarding its fundamentals and predicts the expected price to a symbol selected by the user.

How does it work?
1.Enter a symbol for analysis

2.Market is modeled according to its fundamentals
  - Target Variable: P/VP
  - Most significant variables are selected for the model
  - Polynomial regression (variable degree)
	- Deprecated (master branch)
  - Ridge regression (variable polynomial degree)
  - Grid search for parameters selection
  - Cross-validation considered

3.Expected and actual prices are compared for insights
  - Prices are calculated based on the P/VP predictions and VPA calculated