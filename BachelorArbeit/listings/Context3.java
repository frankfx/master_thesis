	...
	for(Tupel<Long,FaultValue> tplInj : registeredFaultInjectors) {
		if(tplInj.getFst()<len){
			outHashtable.put(tplInj.getFst(), (List<E>) 
			this.getStrategy(outHashtable.get(tplInj.getFst()), tplInj.getSnd()).runInjection());					
		}
	}
	...
