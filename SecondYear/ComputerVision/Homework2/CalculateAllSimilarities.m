function similarities = CalculateAllSimilarities(histogram, centers, kdtree, tfidfValues, visualWordsImageCount, vocabularySize, newImagePath, resizeValue)
    % Read image
    image = imread(newImagePath);
    % Extract descriptors
    grayImage = single(rgb2gray(image));
    grayImage = imresize(grayImage, resizeValue);
    [~, descriptor] = vl_sift(grayImage);
    descriptor = single(descriptor);
    % Calculate histogram
    %imageArray = [];
    %imageArray{1} = image;
    histogramImage = zeros(1, vocabularySize);
    [indexes, ~] = vl_kdtreequery(kdtree, centers, single(descriptor), 'MaxComparisons', 10000);
    for i = 1:length(descriptor)
        histogramImage(1, indexes(i)) = histogramImage(1, indexes(i)) + 1;
    end
    % histogramImage = CreateHistogram(imageArray, vocabularySize, centers, resizeValue);
    histogramSize = size(histogram);
    % histogram(histogramSize(1) + 1, :) = histogramImage(1, :);
    % Calculate TFIDF
    %tfidfValues = TFIDF(histogram, visualWordsImageCount);
    newTfidf = TFIDFNewEntry(histogramImage(1, :), visualWordsImageCount, vocabularySize, histogramSize(1));
    tfidfValues(histogramSize(1) + 1, :) = newTfidf(1, :);
    % Calculate similarities
    
    similarities = zeros(histogramSize(1), 2);
    for i = 1:histogramSize(1)
        similarities(i, 1) = CalculateCosineSimilarity(tfidfValues(i, :), tfidfValues(histogramSize(1) + 1, :));
        similarities(i, 2) = i;
    end
    
    similarities = sortrows(similarities, 1, 'descend');
end