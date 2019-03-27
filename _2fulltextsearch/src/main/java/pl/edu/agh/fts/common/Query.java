package pl.edu.agh.fts.common;

public class Query {
    public static final String billCount = "{\n" +
            "        \"query\": {\n" +
            "            \"match\": {\n" +
            "                \"text\": {\n" +
            "                    \"query\": \"ustawa\"\n" +
            "                }\n" +
            "            }\n" +
            "        }\n" +
            "}";
    public static final String comesIntoForcePhrase = "{\n" +
            "        \"query\": {\n" +
            "            \"match_phrase\": {\n" +
            "                \"text\": {\n" +
            "                    \"query\": \"wchodzi w życie\",\n" +
            "                    \"slop\":2\n" +
            "                }\n" +
            "            }\n" +
            "        }\n" +
            "}";

    public static final String codeOfCivilProcedure = "{\n" +
            "        \"query\": {\n" +
            "            \"match_phrase\": {\n" +
            "                \"text\": {\n" +
            "                    \"query\": \"kodeks postępowania cywilnego\"\n" +
            "                }\n" +
            "            }\n" +
            "        }\n" +
            "}";
}
