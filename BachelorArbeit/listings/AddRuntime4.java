  for (int i = 0; i < faults.length; i++) {

	if (injectFieldDescriptor[i].hasAnnotation(FaultInjects.class)) {
		annotations[i] = new Annotation(
				"faults.FaultInjects", constpool);
		...
	} else {
		annotations[i] = new Annotation("faults.FaultInj",
				constpool);
		...
	}
  }
