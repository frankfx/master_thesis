	MBeanServer server = ...

	...

	HtmlAdaptorServer adaptor = new HtmlAdaptorServer(9992);
	ObjectName adaptorName = new ObjectName("adaptor:proptocol=HTTP");
	server.registerMBean(adaptor, adaptorName);
	adaptor.start();
