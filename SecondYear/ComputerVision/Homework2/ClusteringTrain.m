function centers = ClusteringTrain(descriptors, vocabularySize)
    tic;
    disp("Training!");
    [centers, ~] = vl_kmeans(descriptors, vocabularySize, 'Initialization', 'plusplus',  'algorithm', 'ann', 'MaxNumComparisons', 20, 'NumTrees', 1, 'MaxNumIterations', 50);
    disp("Training completed!");
    toc
end