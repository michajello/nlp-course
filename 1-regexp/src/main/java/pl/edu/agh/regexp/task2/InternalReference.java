package pl.edu.agh.regexp.task2;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class InternalReference {
    private int art;
    private int ust;
    private int point;
}
