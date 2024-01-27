% AMBE (ABSOLUTE MEAN BRIGHTNESS ERROR)
% Lower AMBE implies better brightness preservation. BBHE
function ambe_value = AMBE(im_original, im_enhanced)

ambe_value = abs(mean(im_original(:)) - mean(im_enhanced(:)));
