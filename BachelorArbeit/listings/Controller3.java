	// Get the Platform MBean Server
	MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

	// Construct the ObjectName for the Controller MBean we will register
	ObjectName mbeanName = new ObjectName("jmx:type=Controller");

	// Create the Controller MBean
	Controller mbean = new Controller();

	// Register the Controller MBean
	mbs.registerMBean(mbean, mbeanName);
	...
	// Wait forever
	System.out.println("Server is running now");
	Thread.sleep(Long.MAX_VALUE);
}
