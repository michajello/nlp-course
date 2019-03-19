package pl.edu.agh.regexp.task1;

import org.junit.Test;
import pl.edu.agh.regexp.Samples;
import pl.edu.agh.regexp.common.StatisticExtractor;

import java.util.Collection;

public class StatisticExtractor1Test {

    private static StatisticExtractor<Collection<BillData>> statisticExtractor1 = new StatisticExtractor1();

    @Test
    public void billTest1993_599_txt(){
        statisticExtractor1.getStatistics(Samples.bill_1993_599_txt);
    }

    @Test
    public void billTest1993_646_txt(){
        statisticExtractor1.getStatistics(Samples.bill_1993_646_txt);
    }
}
