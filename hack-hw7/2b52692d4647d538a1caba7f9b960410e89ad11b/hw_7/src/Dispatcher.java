import com.oocourse.elevator3.ElevatorRequest;

import java.util.ArrayList;

public class Dispatcher extends Thread {
    private final ArrayList<Elevator> elevatorArrayList;

    private RequestQueue requestQueue;

    private Global global;

    private Input input;

    public void addElevator(ElevatorRequest elevatorRequest) {
        Elevator elevator = new Elevator(elevatorRequest.getElevatorId(),
                elevatorRequest.getCapacity(),
                elevatorRequest.getFloor(), requestQueue, elevatorRequest.getSpeed(),
                elevatorRequest.getAccess(), global);
        elevatorArrayList.add(elevator);
        elevator.start();
    }

    @Override
    public void run() {
        global = new Global();
        for (int i = 0; i < 6; i++) {
            Elevator elevator = new Elevator(requestQueue, i + 1, global);
            elevatorArrayList.add(elevator);
            elevator.start();
        }
        while (true) {
            if (!input.isAlive() && requestQueue.isEnd() && requestQueue.isEmpty() &&
                    !requestQueue.maintain()) {
                break;
            }
            synchronized (this) {
                try {
                    sleep(100);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public void setRequestQueue(RequestQueue requestQueue) {
        this.requestQueue = requestQueue;
    }

    public void setInputHandler(Input input) {
        this.input = input;
    }

    public Dispatcher(ArrayList<Elevator> elevatorArrayList) {
        this.elevatorArrayList = elevatorArrayList;
    }
}
