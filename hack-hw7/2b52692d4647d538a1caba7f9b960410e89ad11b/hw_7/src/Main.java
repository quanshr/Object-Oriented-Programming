import com.oocourse.elevator3.ElevatorInput;
import com.oocourse.elevator3.TimableOutput;

import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        TimableOutput.initStartTimestamp();
        ElevatorInput elevatorInput = new ElevatorInput(System.in);
        ArrayList<Elevator> elevatorArrayList = new ArrayList<>();
        Dispatcher dispatcher = new Dispatcher(elevatorArrayList);
        RequestQueue requestQueue = new RequestQueue(dispatcher,elevatorArrayList);
        Input handler = new Input(elevatorInput, requestQueue);
        dispatcher.setRequestQueue(requestQueue);
        dispatcher.setInputHandler(handler);
        handler.start();
        dispatcher.start();
    }
}