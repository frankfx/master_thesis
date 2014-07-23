 InjectionStrategy getStrategy(List data, FaultValue fault){
	 
   if(fault.getType().equals(FaultType.ZERO.name()))
	 return new StrategyZero(data,fault);
   else if(fault.getType().equals(FaultType.RANDOM.name()))
	 return new StrategyRandom(data, fault);
	 ...
   
   throw new NoSuchTypeException(fault.getType());
 }
	
