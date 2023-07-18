import com.oocourse.elevator3.ElevatorInput;
import com.oocourse.elevator3.Request;

public class Input extends Thread {

    private ElevatorInput elevatorInput;

    private RequestQueue requestQueue;

    public Input(ElevatorInput elevatorInput, RequestQueue requestQueue) {
        this.elevatorInput = elevatorInput;
        this.requestQueue = requestQueue;
    }

    @Override
    public void run() {
        while (true) {
            Request request = elevatorInput.nextRequest();
            if (request != null) {
                requestQueue.addRequest(request);
            } else {
                requestQueue.setEnd(true);
                break;
            }
        }
    }
}
