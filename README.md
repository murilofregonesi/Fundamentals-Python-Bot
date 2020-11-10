# FundamentalsPythonBot
Python application which models the stocks market regarding its fundamentals and then predicts the expected price to a symbol selected by the user.

How does it work?
1.Enter a symbol for analysis (e.g. bbas3)

2.Market is modeled according to its fundamentals
  - Target Variable: P/VP
  - Most significant variables are selected for the model
  - Polynomial regression (variable degree)
	- Deprecated (master branch)
  - Ridge regression (variable polynomial degree)
  - Grid search for parameters selection
  - Cross-validation considered

3.Actual price and expected price (with deviation included) are exhibited onto the GUI
  - Prices are calculated based on the P/VP predictions and VPA calculated
  - Outliers predictions are removed from standard deviation calculation