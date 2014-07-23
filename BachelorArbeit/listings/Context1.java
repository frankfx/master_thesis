	public class Context<E extends Serializable> {
	...	
		public void write(Long key, List<E> data)  {
		
			if (outHashtable.containsKey(key)) {
				outHashtable.get(key).addAll(data);
			} else {
				outHashtable.put(key, data);
			}	
			return;
	}
	...
