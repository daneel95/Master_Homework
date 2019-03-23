/*
 *  Copyright (c) 2019 Daniel Holteiu
 *  *
 *  * Permission is hereby granted, free of charge, to any person obtaining
 *  * a copy of this software and associated documentation files (the
 *  * "Software"), to deal in the Software without restriction, including
 *  * without limitation the rights to use, copy, modify, merge, publish,
 *  * distribute, sublicense, and/or sell copies of the Software, and to
 *  * permit persons to whom the Software is furnished to do so, subject to
 *  * the following conditions:
 *  *
 *  * The above copyright notice and this permission notice shall be
 *  * included in all copies or substantial portions of the Software.
 *  *
 *  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *  * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *  * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *  * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *  * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *  * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *  * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *  *
 */

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.Scanner;

public class Search {
    private final static String INPUT_DIR = "src\\main\\resources\\InputFiles";
    private final static String INDEX_DIR = "src\\main\\resources\\IndexedFiles";
    private final static int NUMBER_OF_SEARCH_RESULTS = 10;
    private static IndexSearcher searcher;
    private static final CustomRomanianAnalyzer CUSTOM_ROMANIAN_ANALYZER = new CustomRomanianAnalyzer();

    public static void main(String[] args) throws IOException {
        // Index files
        final Indexer indexer = new Indexer();
        indexer.indexDirectory(INPUT_DIR, INDEX_DIR);

        //Searcher
        searcher = createSearcher();

        // Search mechanism
        final Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.print("Cuvant de cautat: ");
            final String wordToFind = scanner.next().trim();
            if (wordToFind.equals("exit")) {
                break;
            }
            printResults(searchInContent(wordToFind));
        }
    }

    private static void printResults(TopDocs foundDocs) throws IOException {
        if (foundDocs == null) {
            System.out.println("Cuvant invalid!");
            return;
        }

        System.out.println("Numarul rezultatelor: " + foundDocs.totalHits);
        for (ScoreDoc scoreDoc : foundDocs.scoreDocs) {
            final Document document = searcher.doc(scoreDoc.doc);
            System.out.println("Document: " + document.get("path") + ", Scor: " + scoreDoc.score);
        }
    }

    private static IndexSearcher createSearcher() throws IOException {
        final Directory directory = FSDirectory.open(Paths.get(INDEX_DIR));
        final IndexReader reader = DirectoryReader.open(directory);
        return new IndexSearcher(reader);
    }

    private static TopDocs searchInContent(String textToFind) throws IOException {
        // Search query
        final QueryParser queryParser = new QueryParser("contents", CUSTOM_ROMANIAN_ANALYZER);
        final Query query;
        try {
            query = queryParser.parse(textToFind);
        } catch (ParseException e) {
            return null;
        }

        return searcher.search(query, NUMBER_OF_SEARCH_RESULTS);
    }
}
