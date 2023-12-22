from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        normalized_email=self.normalize_email(email)
        email_org=normalized_email.lower()

        user = self.model(email=email_org,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password=None,**extra_fields):
        user = self.create_user(email,password=password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    



class CustomUser(AbstractBaseUser):
    Role_Choices = [
      ("admin","Admin"),
      ("user","User"),
      ("driver","Driver")
    ]
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20,choices=Role_Choices, default= "user")
    
    is_driver = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def save(self, *args, **kwargs):
        if self.is_staff:
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True
    

class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M','Male'
        FEMALE = 'F', 'Female'
    gender = models.CharField(max_length=10, choices=Gender.choices)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="profile_info")
    dob = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    alternate_phone = models.CharField(max_length=15)
    profile_image = models.ImageField(upload_to="profile_images/",default="profile_images/download(2).png",blank=True, null=True)

  
  

class AccountInfo(models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE , related_name="account_info")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pin_code = models.IntegerField()
    latitude =models.DecimalField(max_digits=30, decimal_places=20)
    longitude =models.DecimalField(max_digits=30, decimal_places=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return  f"{self.user} {self.latitude}{self.longitude}"
    


class VehicleInfo(models.Model):
   

    class VehicleType(models.TextChoices):
        SEDAN = "sedan", "Sedan"
        HATCHBACK = "hatch", "Hatchback"
        XUV = "xuv","Xuv"

    user = models.ForeignKey(CustomUser,on_delete = models.CASCADE, related_name="vehicle_info")
    registration_number = models.CharField(max_length=10,unique=True)
    vehicle_brand = models.CharField(max_length=30)
    vehicle_name = models.CharField(max_length=30)
    vehicle_type = models.CharField(max_length=20,choices=VehicleType.choices)
    vehicle_color = models.CharField(max_length=30)
    vehicle_year = models.DateField(null=True, blank=True)
    insurance_end_date = models.DateField(null=True, blank=True)
    license_validity = models.DateField(null=True, blank=True)
    seat_capacity = models.IntegerField()
    mileage = models.IntegerField()
    status = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    vehicle_image1 = models.ImageField(upload_to="vehicle_images/",default=None,blank=True, null=True)

    def __str__(self):
        return self.registration_number
    
class ActiveDrivers(models.Model):
    user = models.ForeignKey( CustomUser,on_delete=models.CASCADE)
    active_vehicle = models.ForeignKey(VehicleInfo,on_delete=models.CASCADE)
    existing_address = models.ForeignKey(AccountInfo,on_delete=models.CASCADE, null=True,blank=True)
    latitude =models.DecimalField(max_digits=30, decimal_places=20)
    longitude =models.DecimalField(max_digits=30, decimal_places=20) 
    active_time = models.TimeField()
    

class Trip(models.Model):
    class PaymentMethod(models.TextChoices):
        Payaffter = 'payafter', 'Payafter'
        Online = 'online','Online'

    class TripStatus(models.TextChoices):
        Pending = 'pending', 'Pending'
        Accepted = 'accepted','Accepted'
        Started = 'started','Started'
        finished = 'finished','Finished'


    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='user_ride')
    driver = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='driver_ride')
    vehicle = models.ForeignKey(VehicleInfo,on_delete = models.DO_NOTHING,related_name='ride_vehicle')
    start_lat = models.DecimalField(max_digits=30,decimal_places=20)
    start_long = models.DecimalField(max_digits=30,decimal_places=20)
    end_lat = models.DecimalField(max_digits=30,decimal_places=20)
    end_long = models.DecimalField(max_digits=30,decimal_places=20)
    start_location_name = models.CharField(default=None, null=True, max_length=256)
    end_location_name = models.CharField(default=None, null=True, max_length=256)
    created_at = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    razorpay_order_id = models.CharField(max_length=256,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=256,null=True,blank=True)
    trip_status = models.CharField(max_length=10,default=TripStatus.Pending, choices=TripStatus.choices)
    total_distance = models.DecimalField(max_digits=10,decimal_places=3)
    payment_status = models.BooleanField(default = False)


class FinishedTrips(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='finish_ride_user')
    driver = models.ForeignKey(CustomUser,on_delete=models.DO_NOTHING,related_name='finish_ride_driver')
    vehicle = models.ForeignKey(VehicleInfo,on_delete = models.DO_NOTHING,related_name='finish_ride_vehicle')
    start_lat = models.DecimalField(max_digits=30,decimal_places=20)
    start_long = models.DecimalField(max_digits=30,decimal_places=20)
    end_lat = models.DecimalField(max_digits=30,decimal_places=20)
    end_long = models.DecimalField(max_digits=30,decimal_places=20)
    start_location_name = models.CharField(default=None, null=True, max_length=256)
    end_location_name = models.CharField(default=None, null=True, max_length=256)
    created_at =  models.DateTimeField( null=True)
    amount = models.FloatField()
    Trip_end_time = models.DateTimeField( null=True)
    payment_method = models.CharField(max_length=10)
    razorpay_order_id = models.CharField(max_length=256,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=256,null=True,blank=True)
    total_distance = models.DecimalField(max_digits=10,decimal_places=3)
    payment_status = models.BooleanField(default=False)


     






