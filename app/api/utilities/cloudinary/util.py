
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


#// Config
cloudinary.config(
  cloud_name = "",
  api_key = "",
  api_secret = "",
  secure = True
)



# opttion if user wants to save
def getImgUrl(width,height, )
    pass
#// Upload image url we get from stable diffusion
cloudinary.upload("https://upload.wikimedia.org/wikipedia/commons/a/ae/Olympic_flag.jpg", public_id="olympic_flag")

#// Transform n
url, options = cloudinary_url("olympic_flag", width=100, height=150, crop="fill")