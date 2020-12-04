# Fundamentals Python Bot  
Python application which models the stocks market regarding its fundamentals and then predicts the expected price to a symbol selected by the user.

## [Executable Link](https://drive.google.com/file/d/1-mnJ5p6G4yGt5sujzHsBHui1BEDZejh9/view?usp=sharing)

> How does it work?

1. Enter a symbol for analysis (e.g. bbas3)
2. Market is modeled according to its fundamentals
    1. Target Variable: P/VP
    2. Most significant variables are selected for the model
    3.- Polynomial regression (variable degree) - Deprecated
    4. Ridge regression (variable polynomial degree)
    5. Grid search for parameters selection
    6. Cross-validation considered
3. Actual price and expected price (with deviation included) are exhibited onto the GUI
    1. Prices are calculated based on the P/VP predictions and VPA calculated
    2. Outliers predictions are removed from standard deviation calculation
