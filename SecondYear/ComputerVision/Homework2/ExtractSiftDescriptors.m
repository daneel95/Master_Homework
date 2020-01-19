function descriptors = ExtractSiftDescriptors(trainingImages, resizeValue)
    descriptors = [];
    if nargin < 2
        resizeValue = 1;
    end

    for i = 1:length(trainingImages)
        if mod(i, 100) == 0
            disp(i)
        end
        grayImage = single(rgb2gray(trainingImages{i}));
        grayImage = imresize(grayImage, resizeValue);
        [~, descriptor] = vl_sift(grayImage);
        descriptor = single(descriptor);
        descriptors = [descriptors, descriptor];
    end
end