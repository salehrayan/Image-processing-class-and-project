function mccee_val = MCCEE(original, enhanced)

%%% Evaluate Steerable Pyramid Wavelet transforms for original and enhanced images
% cd toolbox_wavelets
options.nb_orientations = 2;
spyr = perform_steerable_transform(double(original),log2(size(original,1))-2,options);
A11 = spyr{1,6};
O11 = spyr{1,2};
O21 = spyr{1,3};
O12 = spyr{1,4};
O22 = spyr{1,5};

spyr_enh = perform_steerable_transform(double(enhanced),log2(size(enhanced,1))-2,options);
A11e = spyr_enh{1,6};
O11e = spyr_enh{1,2};
O21e = spyr_enh{1,3};
O12e = spyr_enh{1,4};
O22e = spyr_enh{1,5};

%%% Evaluate four metrics for the four criteria
smo_o2_lev2 = SMO(uint8(O22),uint8(O22e)); % SMO for O22 subband
lom_approx = LOM(uint8(A11),uint8(A11e));  % LOM for approx subband
ambe = AMBE(original, enhanced);  % AMBE
Emee = emee(double(enhanced),8,1); % EMEE

feature_vector = [lom_approx ambe smo_o2_lev2 Emee];

%%% Minimum and Range of a training set for normalization
train_mins = [0.5150 0.0874 0.0734 0.3547];
train_range = [258.5662 57.7410 56.2966 404.2183];
 
feature_vector_norm = (feature_vector - train_mins) ./ train_range;
 
load('model_q_ceed')
%%% Use the trained model with LibSVM library to predict the MCCEE metric for the enhanced image
[mccee_val] = svmpredict(0.5, feature_vector_norm, model_q, '-q');