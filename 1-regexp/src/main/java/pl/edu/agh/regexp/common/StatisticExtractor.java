package pl.edu.agh.regexp.common;

import java.util.Collection;

public interface StatisticExtractor<T> {
    T getStatistics(String content);
}
