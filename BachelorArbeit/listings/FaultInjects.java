	@Documented
	@Target(java.lang.annotation.ElementType.FIELD)
	@Retention(java.lang.annotation.RetentionPolicy.RUNTIME )

	public @interface FaultInjects {
		FaultInj[] value();
	}
