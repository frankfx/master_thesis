	public String[] getAnnotatedValues(){
		...
		for (Field f : fields) {
			if (f.isAnnotationPresent(FaultInjects.class)) {
				...				
				for(FaultInj fi : fis){
					list.add(new FaultValue(fi.id(), fi.type(), fi.rate(), fi.blocksize()).toString());
				}
			}
			else{
				if (f.isAnnotationPresent(FaultInj.class)) {
					...
				}				
		...

