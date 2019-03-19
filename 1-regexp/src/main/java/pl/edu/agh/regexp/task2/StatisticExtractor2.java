package pl.edu.agh.regexp.task2;
import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class StatisticExtractor2 implements StatisticExtractor<Collection<InternalReference>> {

    private static final String WC = "\\s*\n*\\s*"; //whitechars
    private static final String ARTICLE_REGEX = "(Art\\. (?<ArtNo>\\d+)\\.)" + "(?<content>.+?)" + "(?=Art\\. \\d+\\.)";
    private static final Pattern ARTICLE = Pattern.compile(ARTICLE_REGEX, Pattern.MULTILINE|Pattern.DOTALL);
    private static final Pattern INT_REF1 = Pattern.compile("([Aa]rt\\." + WC + "(?<ArtNo>\\d+))?" + WC +"ust\\." + WC +  "(?<ustNo>\\d+)" + WC + "(pkt" + WC + "(?<pktBegin>\\d+)"  + "(-(?<pktEnd>\\d+))?)?" );

    @Override
    public Collection<InternalReference> getStatistics(String content) {
        content = content.replaceAll("(^\\s*\n(\\s*\n)*)", "");
        Matcher matcher = ARTICLE.matcher(content);
        List<InternalReference> stats = new ArrayList<>();

        while(matcher.find()){
            String result = matcher.group("content");
            String artNo = matcher.group("ArtNo");
            Matcher matcher1 = INT_REF1.matcher(result);

            while(matcher1.find()){
                Collection<InternalReference> ref = extractData(matcher1, artNo);
                stats.addAll(ref);
            }
        }
        return stats;
    }

    private Collection<InternalReference> extractData(Matcher matcher, String parsedArtNo) {
        String artNo = matcher.group("ArtNo");
        String ustNo = matcher.group("ustNo");
        String pktBegin = matcher.group("pktBegin");
        String pktEnd = matcher.group("pktEnd");
        if (artNo == null) {
            artNo = parsedArtNo;
        }if(pktBegin == null){
            return Collections.singletonList(InternalReference.builder()
                    .art(Integer.parseInt(artNo))
                    .ust(Integer.parseInt(ustNo))
                    .build());
        }

        Collection<InternalReference> refs = new ArrayList<>();

        if(pktEnd != null) {
            for (int i = Integer.parseInt(pktBegin); i <=  Integer.parseInt(pktEnd); i++) {
                refs.add(InternalReference.builder()
                .art(Integer.parseInt(artNo))
                .ust(Integer.parseInt(ustNo))
                .point(i)
                .build());
            }
        }
        return refs;
    }
}
