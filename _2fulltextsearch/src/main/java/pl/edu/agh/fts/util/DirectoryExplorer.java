package pl.edu.agh.fts.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public interface DirectoryExplorer {

    default Stream<Path> extractFilePaths(String dirPath) throws IOException /*throws IOException*/ {
        return Files.walk(Paths.get(dirPath))
                .filter(Files::isRegularFile);
    }
}
