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

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.LongPoint;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.tika.Tika;
import org.apache.tika.exception.TikaException;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;

import static org.apache.lucene.document.Field.Store;
import static org.apache.lucene.index.IndexWriterConfig.OpenMode;

class Indexer {
    private final Tika tika = new Tika();

    void indexDirectory(String inputDirectory, String indexDirectory) throws IOException {
        final Path inputPath = Paths.get(inputDirectory);
        final Directory directory = FSDirectory.open(Paths.get(indexDirectory));

        final Analyzer analyzer = new CustomRomanianAnalyzer();
        final IndexWriterConfig config = new IndexWriterConfig(analyzer);
        config.setOpenMode(OpenMode.CREATE_OR_APPEND);
        final IndexWriter writer = new IndexWriter(directory, config);
        indexDocs(writer, inputPath);

        writer.close();
    }

    private void indexDocs(final IndexWriter writer, Path path) throws IOException {
        if (!Files.isDirectory(path)) {
            return;
        }

        Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
            @Override
            public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) throws IOException
            {
                //Index this file
                try {
                    indexDoc(writer, file, attrs.lastModifiedTime().toMillis());
                } catch (TikaException e) {
                    e.printStackTrace();
                }
                return FileVisitResult.CONTINUE;
            }
        });
    }

    private void indexDoc(IndexWriter writer, Path file, long lastModified) throws IOException, TikaException {
        final Document document = new Document();
        document.add(new StringField("path", file.toString(), Store.YES));
        document.add(new LongPoint("modified", lastModified));
        document.add(new TextField("contents", tika.parseToString(file), Store.YES));

        writer.updateDocument(new Term("path", file.toString()), document);
    }
}
