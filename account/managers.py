from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self , full_name , email ):
        if not full_name:
            raise ValueError("User must be have full_name")
        if not email :
            raise ValueError("User must be have email")

        
        #Django validates the password.

        #creates a new user object form the model class connected to the manager. 
        user = self.model( email = self.normalize_email(email) ,full_name = full_name ) 
        user.save(using = self._db)#save the user in the database
        return user
    
    def create_superuser(self , full_name , email , password):
        if not password :
            raise ValueError("User must be have password")

        user = self.create_user( full_name , email)
        user.set_password(password)
        user.is_admin = True
        user.save(using = self._db)
        return user
