function trainingImages = ReadImages(numberOfClasses, imagePath)
    trainingImages = [];
    
    for i = 1:numberOfClasses
        for j = 1:10
            img = imread(sprintf(imagePath, i, i, j));
            trainingImages{(i - 1) * 10 + j} = img;
        end
    end
end