# Modeling and Prediction

## simple_model.ipynb
This notebook uses Linear Regression, Random Forest, and KNN to try and predict both minimum and maximum prices for a concert. Data processing is done to both create useful columns and remove those that are not useful, and to correct or drop rows with null values. Then, each combination of model type and target variable is tried, some with Grid-Search Cross Validation in order to find the optimal hyperparameters. Ultimately, Random Forest Regression to predict maximum price of a concert ticket performs the best, with an R^2 value of 0.73 . This model is then examined in more detail.

## treeffuser.ipynb
This notebook uses a state-of-the-art diffusion model made for regression, Treeffuser, on our dataset. Link to docs: https://blei-lab.github.io/treeffuser/docs/treeffuser.html . The same features and roughly the same pre-processing as the other models are used here as well. Ultimately, it does not perform as well as the Random Forest Regressor. 

## just_random_forest.ipynb
This notebook built a random forest regressor to predict min ticket price on data without venue capacity information. 