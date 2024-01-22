import pandas as pd
import dill
from sklearn.pipeline import make_pipeline, make_union, FeatureUnion, Pipeline
from sklearn.compose import make_column_transformer, make_column_selector, ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, RobustScaler, FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from utilities import Utilities

def calculate_occupied_area(data):
    data["occupied_area"] = data['building_gfa'] * (data['occupancy'] * 0.01)
    return data

def calculate_new_build(data):
    data["new_build"] = 0  # Initialize to 0
    data.loc[data['year_built'] >= 2000, 'new_build'] = 1
    return data

def energy_demand_pipeline():
    # Load cleaned data
    data = Utilities().get_training_data()

    # Drop unnecessary ID and plot information
    data.drop(columns=['building_id', 'plot_id'], inplace=True)

    # Create X and y
    X = data.drop(columns='electricity_demmand')
    y = data['electricity_demmand']

    # Create train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature engineering transformers
    occupied_area = FunctionTransformer(calculate_occupied_area, validate=False)
    new_build = FunctionTransformer(calculate_new_build, validate=False)

    feature_engineering = ColumnTransformer([
        ("occupied_area", occupied_area, ['building_gfa', 'occupancy']),
        ("new_build", new_build, ['year_built']),
    ], remainder="passthrough").set_output(transform="pandas")

    # Encoding and Scaling transformers
    num_preproc = Pipeline([
        ("num_imputer", SimpleImputer(strategy="constant", fill_value=0.)),
        ("scaler", RobustScaler())
    ])

    cat_preproc = Pipeline([
        ("cat_imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ("num_transformer", num_preproc, make_column_selector(dtype_include=["float64", "int64"])),
        ("cat_transformer", cat_preproc, make_column_selector(dtype_include=["object"]))
    ])

    # Full preprocessing pipeline
    full_preprocessor = Pipeline([
        ("feature_engineering", feature_engineering),
        ("preprocessing", preprocessor)
    ]).set_output(transform="pandas")

    X_train_transformed = full_preprocessor.fit_transform(X_train)

    # Model pipeline
    model_pipeline = make_pipeline(full_preprocessor, GradientBoostingRegressor())

    # Train the pipeline
    model_pipeline.fit(X_train, y_train)

    # Hyperparameter tuning
    param_distributions = {
        'pipeline__preprocessing__num_transformer__num_imputer__strategy': ['mean', 'constant', 'most_frequent'],
        'gradientboostingregressor__max_depth': [3, 5, 7, 9],
        'gradientboostingregressor__min_samples_split': [2, 5, 10],
        'gradientboostingregressor__min_samples_leaf': [1, 2, 4],
        'gradientboostingregressor__subsample': [0.8, 0.9, 1.0]
    }

    randomized_search = RandomizedSearchCV(
        model_pipeline,
        param_distributions=param_distributions,
        n_iter=10,
        cv=5,
        scoring='r2'
    )

    randomized_search.fit(X_train, y_train)

    # Get the best estimator
    tuned_pipeline = randomized_search.best_estimator_

    # Score tuned model
    tuned_score = tuned_pipeline.score(X_test, y_test)
    print(f'Tuned Score: {round(tuned_score, 2)}')

    # Check intermediate steps
    print("Before preprocessing, X_train.shape = ", X_train.shape)
    print("After preprocessing, X_train_preprocessed.shape = ", tuned_pipeline.named_steps["pipeline"].fit_transform(X_train).shape)

    # Export the pipeline as a pickle file
    with open('pipeline/pipeline.pkl', 'wb') as file:
        dill.dump(tuned_pipeline, file)

if __name__ == "__main__":
    energy_demand_pipeline()
