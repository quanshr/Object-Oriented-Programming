import com.oocourse.elevator3.ElevatorRequest;
import com.oocourse.elevator3.MaintainRequest;
import com.oocourse.elevator3.PersonRequest;
import com.oocourse.elevator3.Request;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;

public class RequestQueue {
    private boolean isEnd = false;

    private final ArrayList<Elevator> elevatorArrayList;

    private final ArrayList<Integer> accessElevator = new ArrayList<>();

    private final Dispatcher dispatcher;

    private final HashSet<Integer> hashSet = new HashSet<>();

    public RequestQueue(Dispatcher dispatcher, ArrayList<Elevator> elevatorArrayList) {
        this.dispatcher = dispatcher;
        requestArrayList = new ArrayList<>();
        this.elevatorArrayList = elevatorArrayList;
        for (int i = 0; i < 6; i++) {
            accessElevator.add(0b11111111111);
        }
    }

    private final ArrayList<Request> requestArrayList;

    public synchronized void setEnd(boolean end) {
        isEnd = end;
    }

    public synchronized void addRequest(Request request) {
        if (request instanceof MaintainRequest) {
            requestArrayList.add(request);
            changeStrategy();
        } else if (request instanceof PersonRequest) {
            ArrayList<Integer> arrayList = strategy((PersonRequest) request);
            Person person = new Person((PersonRequest) request, arrayList.get(0), arrayList.get(1));
            hashSet.add(person.getPersonId());
            requestArrayList.add(person);
        } else if (request instanceof ElevatorRequest) {
            dispatcher.addElevator((ElevatorRequest) request);
            accessElevator.add(((ElevatorRequest) request).getAccess());
            changeStrategy();
        }
    }

    public synchronized boolean isEnd() {
        return isEnd;
    }

    public synchronized boolean isEmpty() {
        return requestArrayList.size() == 0;
    }

    public synchronized ArrayList<Request> getRequestArrayList() {
        return requestArrayList;
    }

    public synchronized boolean maintain() {
        Iterator<Request> iterator = requestArrayList.iterator();
        while (iterator.hasNext()) {
            Request request = iterator.next();
            if (request instanceof MaintainRequest) {
                return true;
            }
        }
        return false;
    }

    public synchronized boolean isNotMatch(int access) {
        Iterator<Request> iterator = requestArrayList.iterator();
        while (iterator.hasNext()) {
            Request request = iterator.next();
            if (request instanceof Person) {
                Person person = (Person) request;
                if ((access & (person.getStart() | person.getEnd())) ==
                        (person.getEnd() | person.getStart())) {
                    return false;
                }
            }
        }
        return true;
    }

    public ArrayList<Integer> strategy(PersonRequest personRequest) {
        int size = elevatorArrayList.size();
        ArrayList<ArrayList<Integer>> arrayListAccess = new ArrayList<>();
        int[] flag;
        flag = new int[size];
        ArrayList<Integer> elevatornum = new ArrayList<>();
        int start = 1 << (personRequest.getFromFloor() - 1);
        int end = 1 << (personRequest.getToFloor() - 1);
        dfs(arrayListAccess, 0, start, end, flag, elevatornum);
        ArrayList<Integer> arrayListMin = new ArrayList<>();
        int min = 100;
        for (int i = 0; i < arrayListAccess.size(); i++) {
            ArrayList<Integer> arrayList1 = arrayListAccess.get(i);
            if (min > arrayList1.size()) {
                min = arrayList1.size();
                arrayListMin = arrayList1;
            }
        }
        ArrayList<Integer> ans = new ArrayList<>();
        ans.add(0, start);
        int access0 = start;
        ArrayList<Integer> arrayListAns = new ArrayList<>();
        for (int i = 0; i < arrayListMin.size(); i++) {
            arrayListAns.add(accessElevator.get(arrayListMin.get(i)));
        }
        for (int i = 0; i < arrayListAns.size() - 1; i++) {
            int access1 = arrayListAns.get(i) & arrayListAns.get(i + 1);
            access0 = nextFloor(access0, access1, access1 - access0);
            ans.add(access0);
        }
        ans.add(end);
        return ans;
    }

    private void dfs(ArrayList<ArrayList<Integer>> arrayList, int depth, int start,
                     int end, int[] flag, ArrayList<Integer> elevatornum) {
        if (depth > 7) {
            return;
        }
        int access = 0;
        int size = elevatornum.size();
        for (int i = 0; i < size; i++) {
            access |= accessElevator.get(elevatornum.get(i));
        }
        int size1 = elevatorArrayList.size();
        for (int i = 0; i < size1; i++) {
            Elevator elevator = elevatorArrayList.get(i);
            if (!elevator.isAlive() || elevator.isMaintain()) {
                continue;
            }
            int access1;
            if (((access & accessElevator.get(i)) != 0) || (depth == 0)) {
                access1 = access | accessElevator.get(i);
            } else {
                access1 = 0;
            }
            if ((access1 & start) == 0) {
                continue;
            }
            if (flag[i] != 0) {
                continue;
            }
            flag[i] = 1;
            elevatornum.add(i);
            if ((access1 & (start | end)) == (start | end)) {
                ArrayList<Integer> arrayList1 = new ArrayList<>();
                arrayList1.addAll(elevatornum);
                arrayList.add(arrayList1);
            } else {
                dfs(arrayList, depth + 1, start, end, flag, elevatornum);
            }
            elevatornum.remove(elevatornum.size() - 1);
            flag[i] = 0;
        }
    }

    private int nextFloor(int access0, int access1, int direction) {
        int top = 0;
        int bottom = 0;
        int temp = access0 * 2;
        while (temp <= access1) {
            if ((access1 & temp) != 0) {
                top = (access1 & temp);
                break;
            }
            temp = temp * 2;
        }
        temp = access0 / 2;
        while (temp > 0) {
            if ((access1 & temp) != 0) {
                bottom = (access1 & temp);
                break;
            }
            temp = temp / 2;
        }
        if (direction > 0) {
            if (top > 0) {
                return top;
            } else {
                return bottom;
            }
        } else {
            if (bottom > 0) {
                return bottom;
            } else {
                return top;
            }
        }
    }

    public synchronized void remove(int id) {
        hashSet.remove(id);
    }

    public synchronized boolean allSent() {
        return hashSet.isEmpty();
    }

    private synchronized void changeStrategy() {
        for (int i = 0; i < requestArrayList.size(); i++) {
            Request request = requestArrayList.get(i);
            if (request instanceof Person) {
                Person person = (Person) request;
                ArrayList<Integer> arrayList = strategy(person.getPersonRequest());
                person.changestrategy(arrayList.get(0), arrayList.get(1));
            }
        }
    }
}