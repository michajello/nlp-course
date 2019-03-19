package pl.edu.agh.regexp.util;



import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public interface FileReader {

    default String getContent(String filePath) throws IOException /*throws IOException*/ {
        File directory = new File("./");
        try {
            return new String(Files.readAllBytes(Paths.get(directory.getAbsolutePath() + filePath)));
        } catch (IOException e) {
            return new String(Files.readAllBytes(Paths.get(filePath)));
        }
    }

    default String getContent(Path path) throws IOException {
        return new String(Files.readAllBytes(path));
    }
}
