function histogram = CreateHistogram(images, vocabularySize, centers, kdtree, resizeValue)
    if nargin < 4
        resizeValue = 1;
    end
    
    histogram = zeros(length(images), vocabularySize);

    for i = 1:length(images)
        if mod(i, 100) == 0
            disp(i)
        end
        grayImage = single(rgb2gray(images{i}));
        grayImage = imresize(grayImage, resizeValue);
        [~, descriptor] = vl_sift(grayImage);
        for j = 1:length(descriptor)
            [~, k] = min(vl_alldist(single(descriptor(:, j)), centers));
            histogram(i, k) = histogram(i, k) + 1;
        end
    end
end