	public @interface FaultInj {
		String id();
		String type() default "NONE";
		double rate() default 0.0;
		long blocksize() default 1024;
	}
