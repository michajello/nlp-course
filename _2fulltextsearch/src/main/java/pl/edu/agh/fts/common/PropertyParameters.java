package pl.edu.agh.fts.common;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@ConfigurationProperties
@Component
public class PropertyParameters {
    private String dirPath;
}
