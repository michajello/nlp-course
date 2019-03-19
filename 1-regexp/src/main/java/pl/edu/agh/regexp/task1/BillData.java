package pl.edu.agh.regexp.task1;

import lombok.*;

@Getter
@Setter
@EqualsAndHashCode(exclude = {"counter", "title", "details"})
@Builder
@ToString
public class BillData {
    private int counter;
    private int year;
    private int billNo;
    private int billPosition;
    private String title;
    private String details;
}
