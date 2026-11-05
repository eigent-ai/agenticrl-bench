import java.util.ArrayList;

public class DataMerger {

    public ArrayList merge(ArrayList list1, ArrayList list2) {
        ArrayList mergedList = new ArrayList(list1);
        mergedList.add(list2);
        return mergedList;
    }
}
