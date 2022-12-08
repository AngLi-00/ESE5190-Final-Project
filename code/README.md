We still working on the code of MPU6050.  
### note
To know the angle of your sitting posture, we have write a function to compute it.

    uint8_t Anglefunction(int16_t acc_x, int16_t acc_y, int16_t acc_z)
    {

      float angle_x,angle_y,angle_z;
        uint8_t  temp_x, temp_y, temp_z;

      angle_x=(atan(acc_x/(sqrt(acc_y*acc_y+acc_z*acc_z))))*180.0/M_PI;
      angle_y=(atan(acc_y/(sqrt(acc_x*acc_x+acc_z*acc_z))))*180.0/M_PI;
      angle_z=(atan(acc_z/(sqrt(acc_x*acc_x+acc_y*acc_y))))*180.0/M_PI;
        temp_x = 90-(uint8_t )angle_x;
        temp_y = 90-(uint8_t )angle_y;
      temp_z = 90-(uint8_t )angle_z;

      return temp_x, temp_y, temp_z;
    }
