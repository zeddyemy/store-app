import os
import random
import string
import pathlib
from datetime import date
from werkzeug.utils import secure_filename
from flask import url_for
from PIL import Image as PillowImage

from app.extensions import db
from app.models.image import Image
from config import Config


def saveImage(imgFile):
    '''
    This takes a Image file,
    saves the Image file into the UPLOADS directory,
    and then return the image id after adding the image to Image Table
    '''
    WEBP_FORMAT = 'webp'
    JPG_FORMAT = 'jpeg'
    IMAGE_QUALITY = 80
    
    # create the path were image will be stored
    year = (str(date.today().year))
    month = (str(date.today().month).zfill(2))
    datePath = os.path.join(year, month)
    webpPath = os.path.join(datePath, 'webp')
    jpgPath = os.path.join(datePath, 'jpg')
    
    pathlib.Path(Config.UPLOADS_DIR, year).mkdir(exist_ok=True)
    pathlib.Path(Config.UPLOADS_DIR, year, month).mkdir(exist_ok=True)
    pathlib.Path(Config.UPLOADS_DIR, year, month, 'webp').mkdir(exist_ok=True)
    pathlib.Path(Config.UPLOADS_DIR, year, month, 'jpg').mkdir(exist_ok=True)
    
    # Generate a random string and append it to the original file name
    randString = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    imgName = secure_filename(imgFile.filename) # Grab file name of the selected image
    theImgName, theImgExt = os.path.splitext(os.path.basename(imgName)) # get the file name and extension
    webpIMG = f"{theImgName}-{randString}.webp"
    jpgIMG = f"{theImgName}-{randString}.jpg"
    
    # Save the original image
    # convert the image to webp and jpg format
    with PillowImage.open(imgFile) as img:
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, webpPath, webpIMG), WEBP_FORMAT, quality=IMAGE_QUALITY)
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, jpgPath, jpgIMG), JPG_FORMAT, quality=IMAGE_QUALITY)
        
        original_webp = url_for('static', filename=os.path.join("uploads", webpPath, webpIMG).replace(os.sep, '/'))
        original_jpg = url_for('static', filename=os.path.join("uploads", jpgPath, jpgIMG).replace(os.sep, '/'))
    
    # Create and save different sizes of the image
    with PillowImage.open(imgFile) as img:
        thumb_size = (100, 100)
        
        # Thumbnail size
        # Create and save the thumbnail image
        img.thumbnail(thumb_size)
        imgSize = img.size
        suffix = f"{imgSize[0]}x{imgSize[1]}"
        newWebpIMG = f"{theImgName}-{randString}-{suffix}.webp"
        newJpgIMG = f"{theImgName}-{randString}-{suffix}.jpg"
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, webpPath, newWebpIMG), WEBP_FORMAT, quality=IMAGE_QUALITY)
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, jpgPath, newJpgIMG), JPG_FORMAT, quality=IMAGE_QUALITY)
        
        thumb_webp = url_for('static', filename=os.path.join("uploads", webpPath, newWebpIMG).replace(os.sep, '/'))
        thumb_jpg = url_for('static', filename=os.path.join("uploads", jpgPath, newJpgIMG).replace(os.sep, '/'))
    
    with PillowImage.open(imgFile) as img:
        medium_size = (512, 512)
        
        # Medium size
        # Create and save the medium-sized image
        img.thumbnail(medium_size)
        imgSize = img.size
        suffix = f"{imgSize[0]}x{imgSize[1]}"
        newWebpIMG = f"{theImgName}-{randString}-{suffix}.webp"
        newJpgIMG = f"{theImgName}-{randString}-{suffix}.jpg"
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, webpPath, newWebpIMG), WEBP_FORMAT, quality=IMAGE_QUALITY)
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, jpgPath, newJpgIMG), JPG_FORMAT, quality=IMAGE_QUALITY)
        
        medium_webp = url_for('static', filename=os.path.join("uploads", webpPath, newWebpIMG).replace(os.sep, '/'))
        medium_jpg= url_for('static', filename=os.path.join("uploads", jpgPath, newJpgIMG).replace(os.sep, '/'))
    
    with PillowImage.open(imgFile) as img:
        large_size = (1024, 1024)
        
        # Large size
        # Create and save the large-sized image
        img.thumbnail(large_size)
        imgSize = img.size
        suffix = f"{imgSize[0]}x{imgSize[1]}"
        newWebpIMG = f"{theImgName}-{randString}-{suffix}.webp"
        newJpgIMG = f"{theImgName}-{randString}-{suffix}.jpg"
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, webpPath, newWebpIMG), WEBP_FORMAT, quality=IMAGE_QUALITY)
        img.convert('RGB').save(os.path.join(Config.UPLOADS_DIR, jpgPath, newJpgIMG), JPG_FORMAT, quality=IMAGE_QUALITY)
        
        large_webp = url_for('static', filename=os.path.join("uploads", webpPath, newWebpIMG).replace(os.sep, '/'))
        large_jpg = url_for('static', filename=os.path.join("uploads", jpgPath, newJpgIMG).replace(os.sep, '/'))
    
    # Add the image properties to database
    newImage = Image(filename=imgName, original_webp=original_webp, original_jpg=original_jpg, thumb_webp=thumb_webp, thumb_jpg=thumb_jpg, medium_webp=medium_webp, medium_jpg=medium_jpg, large_webp=large_webp, large_jpg=large_jpg)
    
    db.session.add(newImage)
    db.session.commit()
    img_id = newImage.id
    
    return img_id
