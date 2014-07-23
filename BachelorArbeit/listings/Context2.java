	InjectionStrategy getStrategy(List data, FaultValue fault) ....{
		if(fault.getType().equalsIgnoreCase(FaultType.ZERO.name()))
			return new StrategyZero(data,fault);
		else if(fault.getType().equalsIgnoreCase(FaultType.RANDOM.name()))
			return new StrategyRandom(data, fault);
		else if(fault.getType().equalsIgnoreCase(FaultType.LOSS.name()))
			return new StrategyLoss(data, fault);
		...
	}	
