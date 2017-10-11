package us.dot.its.jpo.ode.model;

public class OdeTimSpecificMetadataLocation extends OdeObject {

   private static final long serialVersionUID = 3174683494132372801L;

   String latitude;
   String longitude;
   String elevation;
   String speed;
   String heading;

   public OdeTimSpecificMetadataLocation() {
      super();
   }

   public OdeTimSpecificMetadataLocation(String latitude, String longitude, String elevation, String speed, String heading) {
      super();
      this.latitude = latitude;
      this.longitude = longitude;
      this.elevation = elevation;
      this.speed = speed;
      this.heading = heading;
   }

}