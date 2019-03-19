package pl.edu.agh.regexp.task2;

import lombok.*;

@Data
@Builder
public class InternalReference {
    private final int art;
    private final int ust;
    private final int point;

    @Getter(AccessLevel.NONE)
    @Setter(AccessLevel.NONE)
    private String string;

    @Override
    public String toString() {
        String s = string;
        if(s == null){
            s ="Art. " + art +" ust. " + ust ;
            if (point != 0) {
                s = s + " pkt. " + point;
            }
            string = s;
        }
        return string;
    }
}
