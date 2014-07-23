	// looking for the field to apply the annotation on
	CtField injectFieldDescriptor[] = new CtField[faults.length];

	for (int i = 0; i < faults.length; i++)
		...
		injectFieldDescriptor[i] = cc
			.getDeclaredField(getFieldName(faults[i].getId()));
		...
