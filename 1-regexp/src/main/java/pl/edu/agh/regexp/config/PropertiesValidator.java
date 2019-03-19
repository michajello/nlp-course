package pl.edu.agh.regexp.config;


import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class PropertiesValidator {

    public void validateProperties(PropertyParameters propertyParameters) {
        if (StringUtils.isEmpty(propertyParameters.getFilePathname()) && StringUtils.isEmpty(propertyParameters.getDirPath())) {
            throw new IllegalArgumentException("dirPath property and filePathname property cannot be empty at once");
        }

        if (!StringUtils.isEmpty(propertyParameters.getFilePathname()) && !StringUtils.isEmpty(propertyParameters.getDirPath())) {
            throw new IllegalArgumentException("dirPath property and filePathname property cannot be set at once. One of them need to be empty");
        }
    }
}
