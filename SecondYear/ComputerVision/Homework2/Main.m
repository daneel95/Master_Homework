% Import vlfeat
run('C:\Users\Daniel\Desktop\vlfeat-0.9.21-bin.tar\vlfeat-0.9.21-bin\vlfeat-0.9.21\toolbox\vl_setup')


isTraining = false;

imagePath = 'C:\\Users\\Daniel\\Desktop\\tema2\\database\\%d\\%d_%d.jpg'; % path to training images
centersPath = 'C:\\Users\\Daniel\\Desktop\\ComputerVision-BagOfWordsHomework\\saved_files\\centers.mat';
histogramPath = 'C:\\Users\\Daniel\\Desktop\\ComputerVision-BagOfWordsHomework\\saved_files\\histogram.mat';
tfidfPath = 'C:\\Users\\Daniel\\Desktop\\ComputerVision-BagOfWordsHomework\\saved_files\\tfidf.mat';
visualWordsImageCountPath = 'C:\\Users\\Daniel\\Desktop\\ComputerVision-BagOfWordsHomework\\saved_files\\visualWordsImageCount.mat';
numberOfClasses = 50;
vocabularySize = 100000;
resizeValue = 1;

if isTraining
    % Read training images
    disp("Read training data!");
    trainingImages = ReadImages(numberOfClasses, imagePath);
    % Extract SIFT descriptors
    disp("Extract Descriptors");
    descriptors = ExtractSiftDescriptors(trainingImages, resizeValue);
    % Train KMeans model
    disp("Train clustering model");
    centers = ClusteringTrain(descriptors, vocabularySize);
    % Create training histogram
    disp("Create histogram!");
    histogram = CreateHistogram(trainingImages, vocabularySize, centers, resizeValue);
    
    % save the kmeans centers
    save(centersPath, 'centers');
    % save the histogram of the training images
    save(histogramPath, 'histogram');
    
    % TFIDF Values
    disp("Get TF-IDF values!");
    % Used for TFIDF, no reason to calculate it all the time
    histogramSize = size(histogram);
    visualWordsImageCount = zeros(1, histogramSize(2));
    for i = 1:histogramSize(1)
        for j = 1:histogramSize(2)
            if histogram(i, j) > 0
                visualWordsImageCount(j) = visualWordsImageCount(j) + 1;
            end
        end
    end
    
    tfidfValues = TFIDF(histogram, visualWordsImageCount);
    save(tfidfPath, 'tfidfValues');
    save(visualWordsImageCountPath, 'visualWordsImageCount');
else
    disp("Calculating similarity");
    queryImagePath = 'C:\\Users\\Daniel\\Desktop\\tema2\\queries\\1\\1_11.jpg';
    centersFile = matfile(centersPath);
    centers = centersFile.centers;
    histogramFile = matfile(histogramPath);
    histogram = histogramFile.histogram;
    tfidfValuesFile = matfile(tfidfPath);
    tfidfValues = tfidfValuesFile.tfidfValues;
    visualWordsImageCountFile = matfile(visualWordsImageCountPath);
    visualWordsImageCount = visualWordsImageCountFile.visualWordsImageCount;
    kdtree = vl_kdtreebuild(centers);

    tic;
    similarities = CalculateAllSimilarities(histogram, centers, kdtree, tfidfValues, visualWordsImageCount, vocabularySize, queryImagePath, resizeValue);
    toc
    
    disp("Read training data!");
    trainingImages = ReadImages(numberOfClasses, imagePath);
    ShowSimilarImages(trainingImages, similarities, 10);
end