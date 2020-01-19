function newTfidf = TFIDFNewEntry(histogramRow, visualWordsImageCount, vocabularySize, N)
    nd = 0;
    for i = 1:vocabularySize
        nd = nd + visualWordsImageCount(i);
    end
    
    newTfidf = zeros(1, vocabularySize);
    for i = 1:vocabularySize
        nid = histogramRow(i);
        ni = visualWordsImageCount(i);
        newTfidf(i) = (nid / nd) * log(N / ni);
    end
end