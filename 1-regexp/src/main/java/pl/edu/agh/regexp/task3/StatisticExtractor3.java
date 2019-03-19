package pl.edu.agh.regexp.task3;

import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class StatisticExtractor3 implements StatisticExtractor<Integer> {

    private static final String BILL_OCCURRENCE_REGEX = "\\bustawa\\b|\\bustawy\\b|\\bustawie\\b|\\bustawę\\b|\\bustawą\\b|\\bustawo\\b|\\bustaw\\b|\\bustawom\\b|\\bustawami\\b|\\bustawach\\b";
    //
    private static final Pattern BILL_OCCURRENCE = Pattern.compile(BILL_OCCURRENCE_REGEX, Pattern.CASE_INSENSITIVE);

    @Override
    public Integer getStatistics(String content) {
        Matcher matcher = BILL_OCCURRENCE.matcher(content);

        int count = 0;
        while (matcher.find()) {
            count++;
        }
        return count;
    }
}
