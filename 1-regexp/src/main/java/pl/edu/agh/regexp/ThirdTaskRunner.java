package pl.edu.agh.regexp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;
import pl.edu.agh.regexp.config.PropertiesValidator;
import pl.edu.agh.regexp.config.PropertyConstants;
import pl.edu.agh.regexp.config.PropertyParameters;
import pl.edu.agh.regexp.util.DirectoryExplorer;
import pl.edu.agh.regexp.util.FileReader;

import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;


@ConditionalOnProperty(name = PropertyConstants.TASK, havingValue = PropertyConstants.TASK3)
@Component
public class ThirdTaskRunner implements CommandLineRunner {

    private final PropertyParameters propertyParameters;
    private final FileReader fileReader;
    private final StatisticExtractor<Integer> statisticExtractor;
    private final PropertiesValidator propertiesValidator;
    private final DirectoryExplorer directoryExplorer;

    @Autowired
    public ThirdTaskRunner(PropertyParameters propertyParameters, FileReader fileReader, StatisticExtractor<Integer> statisticExtractor, PropertiesValidator propertiesValidator, DirectoryExplorer directoryExplorer) {
        this.propertyParameters = propertyParameters;
        this.fileReader = fileReader;
        this.statisticExtractor = statisticExtractor;
        this.propertiesValidator = propertiesValidator;
        this.directoryExplorer = directoryExplorer;
    }


    @Override
    public void run(String... args) throws Exception {
        propertiesValidator.validateProperties(propertyParameters);
        Integer sum;
        if (propertyParameters.getFilePathname() != null) {
            String content = fileReader.getContent(propertyParameters.getFilePathname());
            sum = statisticExtractor.getStatistics(content);
            System.out.println(sum);
        } else {
            Stream<Path> files = directoryExplorer.extractFilePaths(propertyParameters.getDirPath());

            sum = files.mapToInt(f -> {
                try {
                    return statisticExtractor.getStatistics(fileReader.getContent(f));
                } catch (IOException e) {
                    e.printStackTrace();
                    return 0;
                }
            }).sum();

            System.out.println(sum);
        }

    }
}
