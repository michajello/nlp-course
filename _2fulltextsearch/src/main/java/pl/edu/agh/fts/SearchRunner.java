package pl.edu.agh.fts;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.stereotype.Component;
import pl.edu.agh.fts.common.ElasticSearchClient;
import pl.edu.agh.fts.common.PropertyConstants;

@ConditionalOnProperty(name = PropertyConstants.TASK, havingValue = PropertyConstants.TASK_SEARCH)
@Component
public class SearchRunner implements CommandLineRunner{

    private final ElasticSearchClient elasticSearchClient;

    @Autowired
    public SearchRunner(ElasticSearchClient elasticSearchClient) {
        this.elasticSearchClient = elasticSearchClient;
    }

    @Override
    public void run(String... args) throws Exception {
        elasticSearchClient.setup();
    }
}
