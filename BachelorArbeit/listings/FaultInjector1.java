	...
	public abstract List<Byte> runInjection();
	
	protected static boolean isInjected (double rate) ...
		if(rate < 0 || rate > 1){
			...
			throw new RateOutOfBoundsException(msg);
		}  
		return Math.random() < rate;
	}
