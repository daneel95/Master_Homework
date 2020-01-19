function similarity = CalculateCosineSimilarity(feature1, feature2)
    similarity = dot(feature1, feature2) / (norm(feature1) * norm(feature2));
end