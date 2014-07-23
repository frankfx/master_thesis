	if (args.length >= 2) {
		LocateRegistry.createRegistry(Integer.parseInt(args[1]));

		JMXServiceURL url = new JMXServiceURL(
				"service:jmx:rmi:///jndi/rmi://" + args[0] + ":" + args[1]
						+ "/server");

		JMXConnectorServer cs = JMXConnectorServerFactory
				.newJMXConnectorServer(url, null, mbs);
		...
		cs.start();
	}
