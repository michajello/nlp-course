package pl.edu.agh.fts.common;

import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.annotation.JsonValue;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.util.EntityUtils;
import org.elasticsearch.action.ActionFuture;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.Request;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.TransportAddress;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.transport.client.PreBuiltTransportClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import pl.edu.agh.fts.common.data.ResponseDTO;
import pl.edu.agh.fts.common.data.TextDTO;
import pl.edu.agh.fts.util.DirectoryExplorer;
import pl.edu.agh.fts.util.FileReader;

import javax.annotation.PreDestroy;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.nio.file.Path;
import java.util.Map;
import java.util.regex.Pattern;
import java.util.stream.Stream;

@Component
public class ElasticSearchClient {

    private static final String indexName = "bills";
    private static final String indexType = "_doc";
    private static final String indexSource = "{\n" +
            "        \"settings\": {\n" +
            "            \"analysis\": {\n" +
            "              \"analyzer\" : {\n" +
            "                    \"synonym\" : {\n" +
            "                        \"tokenizer\" : \"standard\",\n" +
            "                        \"filter\" : [\"pl_synonyms\", \"lowercase\",\"morfologik_stem\"]\n" +
            "                    }\n" +
            "                },\n" +
            "              \"filter\": {\n" +
            "                  \"pl_synonyms\" : {\n" +
            "                    \"type\" : \"synonym\",\n" +
            "                        \"synonyms\" : [\n" +
            "                            \"kpk => kodeks postępowania karnego\",\n" +
            "                            \"kpc => kodeks postępowania cywilnego\",\n" +
            "                            \"kk => kodeks karny\",\n" +
            "                            \"kc => kodeks cywilny\"\n" +
            "                        ]\n" +
            "                    }    \n" +
            "                  }\n" +
            "            }\n" +
            "        },\n" +
            "        \"mappings\": {\n" +
            "            \"_doc\": {\n" +
            "                \"properties\": {\n" +
            "                    \"text\": {\n" +
            "                        \"type\": \"text\",\n" +
            "                        \"analyzer\": \"morfologik\"\n" +
            "                    }\n" +
            "                }\n" +
            "            }\n" +
            "        }\n" +
            "}";
    private static String indexDoc =  "{\"text\": \"%s\"}";

    private Client client;

    private final PropertyParameters propertyParameters;
    private final DirectoryExplorer directoryExplorer;
    private final FileReader fileReader;
    private final ObjectMapper objectMapper;

    private RestClient restClient;

    @Autowired
    public ElasticSearchClient(PropertyParameters propertyParameters, DirectoryExplorer directoryExplorer, FileReader fileReader, ObjectMapper objectMapper) {
        this.propertyParameters = propertyParameters;
        this.directoryExplorer = directoryExplorer;
        this.fileReader = fileReader;
        this.objectMapper = objectMapper;
        restClient = RestClient.builder(new HttpHost("localhost", 9200, "http")).build();
        initClient();
    }

    private void initClient() {
        try {
            client = new PreBuiltTransportClient(
                    Settings.builder().put("client.transport.sniff", true)
                            .put("cluster.name", "elasticsearch").build())
                    .addTransportAddress(new TransportAddress(InetAddress.getByName("127.0.0.1"), 9300));
        } catch (UnknownHostException e) {
            client = null;
            e.printStackTrace();
        }

    }


    public void setup() {
        IndexRequest request = new IndexRequest(indexName, indexType);
        request.source(indexSource, XContentType.JSON);

        ActionFuture<IndexResponse> index = client.index(request);
        IndexResponse indexResponse = index.actionGet();
        try {
            Stream<Path> pathStream = directoryExplorer.extractFilePaths(propertyParameters.getDirPath());
            pathStream.forEach(f -> {
                try {
                    String content = fileReader.getContent(f);
                    IndexRequest request1 = new IndexRequest(indexName, indexType, f.getFileName().toString());
                    String body = objectMapper.writeValueAsString(new TextDTO(content));
                    request1.source(body, XContentType.JSON);
                    client.index(request1).actionGet();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    public void searchStatistics() throws IOException {
        Request request = new Request(HttpMethod.GET.toString(), String.format("/%s/%s/_search" ,indexName, indexType));
        request.setJsonEntity(Query.billCount);
        Response response = restClient.performRequest(request);

        System.out.println("Odmiany słowa \"ustawa\": " + extractNumberFromBody(response));

        request = new Request(HttpMethod.GET.toString(), String.format("/%s/%s/_search" ,indexName, indexType));
        request.setJsonEntity(Query.comesIntoForcePhrase);
        response = restClient.performRequest(request);

        System.out.println("Odmiany słowa \"wchodzi w życie\": " + extractNumberFromBody(response));

        request = new Request(HttpMethod.GET.toString(), String.format("/%s/%s/_search" ,indexName, indexType));
        request.setJsonEntity(Query.codeOfCivilProcedure);
        response = restClient.performRequest(request);
        System.out.println("Odmiany słowa \"kodeks postępowania cywilnego\": " + extractNumberFromBody(response));
        

    }

    private int extractNumberFromBody(Response response){
        Map<String, Object> map = null;
        try {
            map = objectMapper.readValue( EntityUtils.toString(response.getEntity()), new TypeReference<Map<String, Object>>() {});
        } catch (IOException e) {
            e.printStackTrace();
            return 0;
        }
        map = (Map<String, Object>) map.get("hits");
        return (int) map.get("total");
    }

    @PreDestroy
    private void teardown() {
        client.close();
        try {
            restClient.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
