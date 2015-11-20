public class PoolSizeCalculatorApp extends PoolSizeCalculator {

 public static void main(String[] args) throws InterruptedException,
                                               InstantiationException,
                                               IllegalAccessException,
                                               ClassNotFoundException {
  MyThreadSizeCalculator calculator = new MyThreadSizeCalculator();
  calculator.calculateBoundaries(new BigDecimal(1.0),
                                 new BigDecimal(100000));
 }

 protected long getCurrentThreadCPUTime() {
  return ManagementFactory.getThreadMXBean().getCurrentThreadCpuTime();
 }

 protected Runnable creatTask() {
  return new AsynchronousTask(0, "IO", 1000000);
 }

 protected BlockingQueue<Runnable> createWorkQueue() {
  return new LinkedBlockingQueue<>();
 }

}