function tfidfValues = TFIDF(histogram, visualWordsImageCount)
    histogramSize = size(histogram);
    % Count the number of images where each visual word appears
    tfidfValues = zeros(histogramSize(1), histogramSize(2));
    N = histogramSize(1);
    
    for d = 1:histogramSize(1)
        nd = 0;
        for i = 1:histogramSize(2)
           nd = nd + visualWordsImageCount(i); 
        end
        for i = 1:histogramSize(2)
            nid = histogram(d, i);
            ni = visualWordsImageCount(i);

            tfidfValues(d, i) = (nid / nd) * log(N / ni);
        end
    end
end