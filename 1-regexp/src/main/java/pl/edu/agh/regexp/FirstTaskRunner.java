package pl.edu.agh.regexp;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;
import pl.edu.agh.regexp.config.PropertiesValidator;
import pl.edu.agh.regexp.config.PropertyConstants;
import pl.edu.agh.regexp.config.PropertyParameters;
import pl.edu.agh.regexp.task1.BillData;
import pl.edu.agh.regexp.util.DirectoryExplorer;
import pl.edu.agh.regexp.util.FileReader;

import java.io.IOException;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;


@ConditionalOnProperty(name = PropertyConstants.TASK, havingValue = PropertyConstants.TASK1)
@Component
public class FirstTaskRunner implements CommandLineRunner{

    private final PropertyParameters propertyParameters;
    private final FileReader fileReader;
    private final StatisticExtractor<Collection<BillData>> statisticExtractor;
    private final PropertiesValidator propertiesValidator;
    private final DirectoryExplorer directoryExplorer;

    @Autowired
    public FirstTaskRunner(PropertyParameters propertyParameters, FileReader fileReader, StatisticExtractor<Collection<BillData>> statisticExtractor, PropertiesValidator propertiesValidator, DirectoryExplorer directoryExplorer) {
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
            System.out.println(statisticExtractor.getStatistics(content));
        } else {
            Stream<Path> files = directoryExplorer.extractFilePaths(propertyParameters.getDirPath());
            Map<BillData, Integer> stats = new HashMap<>();

            List<BillData> collection = files.map(f -> {
                try {
                    return statisticExtractor.getStatistics(fileReader.getContent(f));
                } catch (IOException e) {
                    e.printStackTrace();
                }
                return new HashSet<BillData>();
            }).flatMap(f -> f.stream()).collect(Collectors.toList());

            collection.forEach( e -> {
                if (stats.containsKey(e)){
                    stats.put(e, stats.get(e) + 1);
                }else {
                    stats.put(e, 1);
                }
            });
            System.out.println(stats);
        }
    }
}
