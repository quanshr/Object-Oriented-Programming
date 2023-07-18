import com.oocourse.elevator3.MaintainRequest;
import com.oocourse.elevator3.PersonRequest;
import com.oocourse.elevator3.Request;
import com.oocourse.elevator3.TimableOutput;

import java.util.ArrayList;
import java.util.Iterator;

public class Elevator extends Thread {
    private final ArrayList<Person> personArrayList = new ArrayList<>();

    private final RequestQueue requestQueue;

    private final double speed;

    private final int access;

    private final int id;

    private final ArrayList<Person> waitList = new ArrayList<>();

    private final int capacity;

    private int direction;

    private int curFloor;

    private boolean maintain = false;

    private final Global global;

    @Override
    public void run() {
        while (true) {
            if (requestQueue.isNotMatch(access) && personArrayList.size() == 0) {
                if (requestQueue.isEnd() && !requestQueue.maintain() && requestQueue.allSent()
                        && requestQueue.isEmpty()) {
                    break;
                } else {
                    synchronized (this) {
                        try {
                            sleep(100);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
            if (maintain()) {
                openAndClose1();
                TimableOutput.println("MAINTAIN_ABLE-" + id);
                break;
            }
            if (judge()) {
                openAndClose();
            }
            look();
            move();

        }
    }

    public int outsize() {
        int sum = 0;
        for (int i = 0; i < personArrayList.size(); i++) {
            Person person = personArrayList.get(i);
            if (person.getEnd() == (1 << (curFloor - 1))) {
                sum++;
            }
        }
        return sum;
    }

    public boolean judge() {
        if ((access & (1 << (curFloor - 1))) == 0) {
            return false;
        }
        boolean b = false;
        synchronized (requestQueue) {
            Iterator<Request> iterator = requestQueue.getRequestArrayList().iterator();
            while (iterator.hasNext()) {
                Request request = iterator.next();
                if (request instanceof Person) {
                    Person person = (Person) request;
                    if (person.getStart() == 1 << (curFloor - 1) &&
                            canTouch(person) &&
                            (samedirection(person) ||
                                    (personArrayList.size() == 0 && !keepdirection()))
                            && waitList.size() - outsize() + personArrayList.size() < capacity) {
                        waitList.add(person);
                        iterator.remove();
                        b = true;
                    }
                }
            }
        }
        for (Person person : personArrayList) {
            if (person.getEnd() == 1 << (curFloor - 1)) {
                b = true;
                break;
            }
        }
        return b;
    }

    public boolean maintain() {
        synchronized (requestQueue) {
            for (int i = 0; i < requestQueue.getRequestArrayList().size(); i++) {
                Request request = requestQueue.getRequestArrayList().get(i);
                if (request instanceof MaintainRequest &&
                        ((MaintainRequest) request).getElevatorId() == id) {
                    maintain = true;
                    return true;
                }
            }
        }
        return false;
    }

    public boolean isMaintain() {
        return maintain;
    }

    public synchronized void open() {
        TimableOutput.println("OPEN" + "-" + curFloor + "-" + id);
        try {
            sleep(200);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public synchronized void close() {
        try {
            sleep(200);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        TimableOutput.println("CLOSE" + "-" + curFloor + "-" + id);
    }

    public void openAndClose() {
        global.acquireSemaphore1(curFloor);
        if (onlyIn()) {
            global.acquireSemaphore2(curFloor);
        }
        open();
        final boolean b = onlyIn();
        Iterator<Person> personIterator = personArrayList.iterator();
        while (personIterator.hasNext()) {
            Person person = personIterator.next();
            if (person.getEnd() == 1 << (curFloor - 1)) {
                TimableOutput.println("OUT-" + person.getPersonId()
                        + "-" + curFloor + "-" + id);
                if (person.getToFloor() != curFloor) {
                    PersonRequest personRequest1 = new
                            PersonRequest(curFloor, person.getToFloor(),
                            person.getPersonId());
                    requestQueue.addRequest(personRequest1);
                } else {
                    requestQueue.remove(person.getPersonId());
                }
                personIterator.remove();
            }
        }
        Iterator<Person> iterator = waitList.iterator();
        while (iterator.hasNext()) {
            Person person = iterator.next();
            TimableOutput.println("IN-" + person.getPersonId() + "-" + curFloor + "-" + id);
            personArrayList.add(person);
            iterator.remove();
        }
        close();
        if (b) {
            global.releaseSemaphore2(curFloor);
        }
        global.releaseSemaphore1(curFloor);
    }

    public void openAndClose1() {
        if (personArrayList.size() != 0) {
            global.acquireSemaphore1(curFloor);
            open();
            removeAll();
            close();
            global.releaseSemaphore1(curFloor);
        }
        synchronized (requestQueue) {
            Iterator<Request> iterator = requestQueue.getRequestArrayList().iterator();
            while (iterator.hasNext()) {
                Request request = iterator.next();
                if (request instanceof MaintainRequest &&
                        ((MaintainRequest) request).getElevatorId() == id) {
                    iterator.remove();
                    break;
                }
            }
        }
    }

    public void removeAll() {
        Iterator<Person> iterator = personArrayList.iterator();
        while (iterator.hasNext()) {
            Person person = iterator.next();
            if (person.getToFloor() != curFloor) {
                PersonRequest personRequest1 =
                        new PersonRequest(curFloor,
                                person.getToFloor(), person.getPersonId());
                requestQueue.addRequest(personRequest1);
            } else {
                requestQueue.remove(person.getPersonId());
            }
            TimableOutput.println("OUT-" + person.getPersonId()
                    + "-" + curFloor + "-" + id);
            iterator.remove();
        }
    }

    public void move() {
        if (direction > 0) {
            up();
        } else if (direction < 0) {
            down();
        }
    }

    public void look() {
        synchronized (requestQueue) {
            if (!keepdirection()) {
                direction = -direction;
                if (!keepdirection()) {
                    direction = 0;
                }
            } else if (direction == 0) {
                if (personArrayList.size() > 0) {
                    direction = personArrayList.get(0).getToFloor() -
                            personArrayList.get(0).getFromFloor();
                }
            }
        }
    }

    public boolean keepdirection() {
        for (int i = 0; i < requestQueue.getRequestArrayList().size(); i++) {
            Request request = requestQueue.getRequestArrayList().get(i);
            if (request instanceof Person) {
                Person person = (Person) request;
                if (!canTouch(person)) {
                    continue;
                }
                if (direction > 0 && person.getStart() > 1 << (curFloor - 1)) {
                    return true;
                }
                if (direction < 0 && person.getStart() < 1 << (curFloor - 1)) {
                    return true;
                }
                if (direction == 0) {
                    direction = person.getStart() - (1 << (curFloor - 1));
                    return true;
                }
            }
        }
        Iterator<Person> iterator1 = personArrayList.iterator();
        while (iterator1.hasNext()) {
            Person person = iterator1.next();
            if (samedirection(person)) {
                return true;
            }
        }
        return false;
    }

    public boolean samedirection(Person person) {
        if (person.getEnd() - person.getStart() > 0 && direction > 0) {
            return true;
        }
        if (person.getEnd() - person.getStart() < 0 && direction < 0) {
            return true;
        }
        if (direction == 0) {
            direction = person.getStart() - (1 << (curFloor - 1));
            return true;
        }
        return false;
    }

    public void up() {
        curFloor++;
        try {
            sleep((long) (speed * 1000));
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        TimableOutput.println("ARRIVE-" + curFloor + "-" + id);
    }

    public void down() {
        curFloor--;
        try {
            sleep((long) (speed * 1000));
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        TimableOutput.println("ARRIVE-" + curFloor + "-" + id);
    }

    public Elevator(RequestQueue requestQueue, int id, Global global) {
        this.requestQueue = requestQueue;
        this.id = id;
        curFloor = 1;
        direction = 0;
        capacity = 6;
        speed = 0.4;
        access = 0b11111111111;
        this.global = global;
    }

    public Elevator(int id, int capacity, int curFloor, RequestQueue requestQueue,
                    double speed, int access, Global global) {
        this.id = id;
        this.requestQueue = requestQueue;
        this.capacity = capacity;
        this.curFloor = curFloor;
        direction = 0;
        this.speed = speed;
        this.access = access;
        this.global = global;
    }

    private boolean onlyIn() {
        Iterator<Person> iterator = personArrayList.iterator();
        while (iterator.hasNext()) {
            Person person = iterator.next();
            if (person.getEnd() == 1 << (curFloor - 1)) {
                return false;
            }
        }
        return true;
    }

    private boolean canTouch(Person person) {
        return (access & (person.getEnd() | person.getStart())) ==
                (person.getEnd() | person.getStart());
    }
}
