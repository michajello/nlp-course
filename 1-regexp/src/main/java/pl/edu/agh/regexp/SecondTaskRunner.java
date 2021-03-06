package pl.edu.agh.regexp;

import com.sun.javafx.collections.MappingChange;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;
import pl.edu.agh.regexp.config.PropertiesValidator;
import pl.edu.agh.regexp.config.PropertyConstants;
import pl.edu.agh.regexp.config.PropertyParameters;
import pl.edu.agh.regexp.task2.InternalReference;
import pl.edu.agh.regexp.util.DirectoryExplorer;
import pl.edu.agh.regexp.util.FileReader;

import java.io.IOException;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;


@ConditionalOnProperty(name = PropertyConstants.TASK, havingValue = PropertyConstants.TASK2)
@Component
public class SecondTaskRunner implements CommandLineRunner {

    private final PropertyParameters propertyParameters;
    private final FileReader fileReader;
    private final StatisticExtractor<Collection<InternalReference>> statisticExtractor;
    private final PropertiesValidator propertiesValidator;
    private final DirectoryExplorer directoryExplorer;

    @Autowired
    public SecondTaskRunner(PropertyParameters propertyParameters, FileReader fileReader, StatisticExtractor<Collection<InternalReference>> statisticExtractor, PropertiesValidator propertiesValidator, DirectoryExplorer directoryExplorer) {
        this.propertyParameters = propertyParameters;
        this.fileReader = fileReader;
        this.statisticExtractor = statisticExtractor;
        this.propertiesValidator = propertiesValidator;
        this.directoryExplorer = directoryExplorer;
    }


    @Override
    public void run(String... args) throws Exception {
        propertiesValidator.validateProperties(propertyParameters);
        if (propertyParameters.getFilePathname() != null) {
            String content = fileReader.getContent(propertyParameters.getFilePathname());
            Collection<InternalReference> statistics = statisticExtractor.getStatistics(content);
            Map<InternalReference, Integer> printStats = new HashMap<>();
            statistics.forEach( ref -> {
                printStats.put(ref, printStats.getOrDefault(ref, 0) + 1);
            });

            LinkedHashMap<InternalReference, Integer> collect = printStats.entrySet().stream().sorted(Map.Entry.comparingByValue(Collections.reverseOrder())).collect((Collectors.toMap(
                    Map.Entry::getKey, Map.Entry::getValue, (e1, e2) -> e1, LinkedHashMap::new)));

            collect.forEach((k,v) -> System.out.println(k + " - " + v));
        }
    }
}
