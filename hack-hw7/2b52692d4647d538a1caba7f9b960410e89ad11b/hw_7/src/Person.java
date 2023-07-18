import com.oocourse.elevator3.PersonRequest;
import com.oocourse.elevator3.Request;

public class Person extends Request {
    private final PersonRequest personRequest;

    private int start;

    private int end;

    public Person(PersonRequest personRequest, int start, int end) {
        this.personRequest = personRequest;
        this.start = start;
        this.end = end;
    }

    public int getPersonId() {
        return personRequest.getPersonId();
    }

    public int getStart() {
        return start;
    }

    public int getEnd() {
        return end;
    }

    public int getFromFloor() {
        return personRequest.getFromFloor();
    }

    public int getToFloor() {
        return personRequest.getToFloor();
    }

    public void changestrategy(int start,int end) {
        this.start = start;
        this.end = end;
    }

    public PersonRequest getPersonRequest() {
        return personRequest;
    }
}
