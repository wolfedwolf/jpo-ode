package us.dot.its.jpo.ode.model;

public class OdePayloadViolation {

	private String fieldName;
    private double value;
	private double validMin;
	private double validMax;

	public OdePayloadViolation() {
		super();
		fieldName = null;
		value = Double.NaN;
		validMin = Double.NaN;
		validMax = Double.NaN;
	}
	
	public OdePayloadViolation(String fieldName, double value, double validMin, double validMax) {
        super();
        this.fieldName = fieldName;
        this.value = value;
        this.validMin = validMin;
        this.validMax = validMax;
    }

    public String getFieldName(){
		return fieldName;
	}

	public OdePayloadViolation setFieldName(String fieldName){
		this.fieldName = fieldName;
		return this;
	}

	public double getValue() {
        return value;
    }

    public void setValue(double value) {
        this.value = value;
    }

    public double getValidMin(){
		return validMin;
	}

	public OdePayloadViolation setValidMin(double validMin){
		this.validMin = validMin;
		return this;
	}

	public double getValidMax(){
		return validMax;
	}

	public OdePayloadViolation setValidMax(double validMax){
		this.validMax = validMax;
		return this;
	}

	@Override
    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((fieldName == null) ? 0 : fieldName.hashCode());
        long temp;
        temp = Double.doubleToLongBits(validMax);
        result = prime * result + (int) (temp ^ (temp >>> 32));
        temp = Double.doubleToLongBits(validMin);
        result = prime * result + (int) (temp ^ (temp >>> 32));
        temp = Double.doubleToLongBits(value);
        result = prime * result + (int) (temp ^ (temp >>> 32));
        return result;
    }

	@Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        OdePayloadViolation other = (OdePayloadViolation) obj;
        if (fieldName == null) {
            if (other.fieldName != null)
                return false;
        } else if (!fieldName.equals(other.fieldName))
            return false;
        if (Double.doubleToLongBits(validMax) != Double.doubleToLongBits(other.validMax))
            return false;
        if (Double.doubleToLongBits(validMin) != Double.doubleToLongBits(other.validMin))
            return false;
        if (Double.doubleToLongBits(value) != Double.doubleToLongBits(other.value))
            return false;
        return true;
    }
}
