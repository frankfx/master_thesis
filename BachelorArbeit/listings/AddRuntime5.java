	AnnotationMemberValue[] elements = new AnnotationMemberValue[len];

	for (int x = 0; x < len; x++) {

		if (fis[x].id().equals(faults[i].getId())) {
			subAnnotations[x] = new Annotation(
					"faults.FaultInj", constpool);
			subAnnotations[x].addMemberValue(
					"id",
					new StringMemberValue(faults[i].getId(), ccFile
						.getConstPool()));
			...
	
		} else {
			subAnnotations[x] = new Annotation(
					"faults.FaultInj", constpool);
			subAnnotations[x].addMemberValue(
					"id",
					new StringMemberValue(fis[x].id(), ccFile
							.getConstPool()));
			...
		}
		elements[x] = new AnnotationMemberValue(subAnnotations[x],
				ccFile.getConstPool());
	}

	ArrayMemberValue arrMemberValue = new ArrayMemberValue(
			ccFile.getConstPool());
	arrMemberValue.setValue(elements);
	annotations[i].addMemberValue("value", arrMemberValue);
