# Room-Occupancy-Machine-Learning-Estimation
A statistical analysis of room occupancy data. Includes Machine Learning-based inference on sensor data for estimating the number of occupants in a room. 

My analysis includes:

analysis.py - Preprocessing the data (normalization, train-test split) training and testing the performance (test set F1 score) of Random Forest and QDA classifiers in two scenarios:
1. Data is distributed as collected originally.
2. Dataset is balanced using SMOTE (data augmentation technique).

streamlit_visualization.py - Creates a streamlit dashboard including the main sensors data (4 time series measurements of light, sound and temperature) and the trained QDA model's predictions (added in analysis.py and saced in Occupancy_Estimation_Prediction.csv).

create_final_html.py - Creates a sharable HTML file of the interactive dashboard showing the data.

* Files should be run in the mentioned order to run properly.

Data was created, collected and analyzed in the following paper: A. P. Singh, V. Jain, S. Chaudhari, F. A. Kraemer, S. Werner and V. Garg, "Machine Learning-Based Occupancy Estimation Using Multivariate Sensor Nodes," 2018 IEEE Globecom Workshops (GC Wkshps), Abu Dhabi, United Arab Emirates, 2018, pp. 1-6, doi: 10.1109/GLOCOMW.2018.8644432. keywords: {Support vector machines;Estimation;Measurement;Temperature sensors;Principal component analysis;Radio frequency;Hidden Markov models;Internet of Things;Machine Learning;Occupancy Estimation;Wireless Sensor Network}

Link to the paper: https://ieeexplore.ieee.org/document/8644432

Data source: Singh, A. & Chaudhari, S. (2018). Room Occupancy Estimation [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5P605.

Link to the data source: https://archive.ics.uci.edu/dataset/864/room+occupancy+estimation
