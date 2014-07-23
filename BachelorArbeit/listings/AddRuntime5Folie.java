  for (int x = 0; x < len; x++) {

	if (fis[x].id().equals(faults[i].getId())) {
	  subAnnotations[x] = new Annotation(
		"faults.FaultInj", constpool);
		subAnnotations[x].addMemberValue(
			"id",
			new StringMemberValue(faults[i].getId(),
				ccFile.getConstPool()));
		subAnnotations[x].addMemberValue(
			"rate",
			new DoubleMemberValue(faults[i].getRate(),
				ccFile.getConstPool()));
		...
	...
