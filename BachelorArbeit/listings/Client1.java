	...
	// Get an MBeanServerConnection
	MBeanServerConnection mbsc = jmxc.getMBeanServerConnection();
	ObjectName mbeanName = new ObjectName("jmx:type=Controller");
		
    Attribute att = new Attribute("UseObjectOutputStream", true);
		        
	// Invoke the runInjection op
	String[] sig = {"java.lang.String"};
	Object[] opArgs = {"/home/../Tyson.jpg"};
		
	mbsc.setAttribute(mbeanName, att);
	mbsc.setAttribute(mbeanName, re);
	... mbsc.getAttribute(mbeanName, "CurrentFaults");
	...
		
	mbsc.invoke(mbeanName, "runInjection", opArgs, sig);
	
