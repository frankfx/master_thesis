	// pool creation
	private static ClassPool pool = ClassPool.getDefault();
	private static CtClass cc;
	...
	// reload classfile
	private static HotSwapper hs;

	public static void initHotSwapper(String port) ...{
		hs = new HotSwapper(port);
	}
	...
	private static StreamProcessor addFaultInjAnnotationToMethod(
			String className, FaultValue[] faults) {
		...
		// extracting the class
		cc = pool.getCtClass(className);
		...
	}
