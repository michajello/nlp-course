package pl.edu.agh.regexp.task1;

import org.springframework.stereotype.Component;
import pl.edu.agh.regexp.common.StatisticExtractor;

import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Component
public class StatisticExtractor1 implements StatisticExtractor<Collection<BillData>> {

    private static final String WC = "\\s*\n*\\s*"; //whitechars
    private static final Pattern DIGITS_PATERN = Pattern.compile("[1-9]\\d*");
    private static final String BILL_HEADER_REGEX = "^Dz.U. z (?<year>\\d{4}) r. Nr (?<nr>[1-9][0-9]{0,5}), poz. (?<poz>[1-9][0-9]{0,5})\\s*\n";
    private static final Pattern BILL_HEADER = Pattern.compile(BILL_HEADER_REGEX, Pattern.MULTILINE);
    private static final String BILL_TITLE_REGEX = "\\s*USTAWA\\s*\n+\\s*z dnia \\d+ \\p{Ll}+\\s+(?<year>\\d{4})\\s+r\\.\\s+(?<title>.*(?=Art\\. 1\\.))";
    private static final Pattern BILL_TITLE = Pattern.compile(BILL_TITLE_REGEX, Pattern.DOTALL);
    private static final String BILL_REFERENCE_REGEX = "[Uu]staw\\p{Ll}{0,3}" + WC + "z"  + WC + "dnia" + WC + "\\d+" + WC + "\\p{Ll}+" + WC + "(?<year>\\d{4})" + WC +
            "r\\.\\s+(?<title>.*?)(?<details>\\(Dz.U." + WC + "(z\\s*\n*\\s*(?<submitYear>\\d{4})\\s*\n*\\s*r.)??" + WC +"Nr"+ WC +"(?<nr>[1-9][0-9]{0,5}),"+ WC +"poz."+ WC +"(?<poz>[1-9][0-9]{0,5}).*?\\))\\s?";
    private static final Pattern BILL_REFERENCE = Pattern.compile(BILL_REFERENCE_REGEX, Pattern.DOTALL);


    @Override
    public Collection<BillData> getStatistics(String content) {
        content = content.replaceAll("(^\\s*\n(\\s*\n)*)", "");
        Matcher billInfo = BILL_HEADER.matcher(content);

        BillData billData = null;
        if (billInfo.find()) {
            String phrase = billInfo.group();
            content = content.replaceAll(phrase, "");
            billData = extractBillData(billInfo);
            Matcher titleBill = BILL_TITLE.matcher(content);
            if (titleBill .find()) {
                phrase = titleBill.group();
                content = content.replaceAll(phrase, "");
                billData.setTitle(titleBill.group("title").replaceAll("\n\\s*", " ").trim());
            }
        }else{
            throw new RuntimeException("Incorrect data input: " + content);
        }



        Matcher billExternalReferences = BILL_REFERENCE.matcher(content);
        List<BillData> data = new ArrayList<>();
        while (billExternalReferences.find()){
            String phrase = billExternalReferences.group();
            BillData billData1 = extractBillDataReference(billExternalReferences);

            data.add(billData1);
        }

        return data;
    }

    private BillData extractBillDataReference(Matcher billExternalReferences){
        String title = billExternalReferences.group("title").replaceAll("\\r\\n|\\r|\\n"," ").replaceAll("\\s{2,}", " ");
        String year = billExternalReferences.group("year");
        String submitYear = billExternalReferences.group("submitYear");
        String nr = billExternalReferences.group("nr");
        String poz = billExternalReferences.group("poz");
        String details = billExternalReferences.group("details");

        return BillData.builder()
                .year(year != null ? Integer.parseInt(year):Integer.parseInt(submitYear))
                .billNo(Integer.parseInt(nr))
                .billPosition(Integer.parseInt(poz))
                .title(title)
                .details(details)
                .counter(1)
                .build();
    }


    private BillData extractBillData(Matcher billInfo){
        return BillData.builder()
                .year(Integer.parseInt(billInfo.group("year")))
                .billNo(Integer.parseInt(billInfo.group("nr")))
                .billPosition(Integer.parseInt(billInfo.group("poz")))
                .build();
    }
}
