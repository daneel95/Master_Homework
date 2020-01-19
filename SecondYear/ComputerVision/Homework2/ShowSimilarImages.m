function ShowSimilarImages(trainingImages, similarities, numberOfImagesToShow)
    for i = 1:min(numberOfImagesToShow, length(trainingImages))
        figure(i);
        image(trainingImages{similarities(i, 2)});
    end
end