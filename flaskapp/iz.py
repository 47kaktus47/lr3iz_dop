from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
 return " <html><head></head> <body> Введите в поисковую строку: https://lr3iz_dop.herokuapp.com/net </body></html>"

from flask import render_template
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Le2kPwcAAAAAAjXJ5YpKnaf1KfO3fLMjVsHDcTI'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Le2kPwcAAAAAAgnOBdJG2OEh_c2trx_8wb7AJ9O'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
 openid = StringField('Изменить: по вертикали - 0, по горизонтали - 1.', validators = [DataRequired()])
 upload = FileField('Загрузите изображение', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
 recaptcha = RecaptchaField()
 submit = SubmitField('Передать')
 
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
 
def f(filename,openid):
 print(filename)
 imag= Image.open(filename)
 x, y = imag.size
 openid=int(openid)
 height = 224
 width = 224
 img1 = Image.open(filename)
 img0= np.array(img.resize((height,width)))/255.0
 img1=img0[:,:,0]=0
 img2=img0[:,:,1]=0
 img3=img0[:,:,2]=0
 img1.save(filename+'1')
 img2.save(filename+'2')
 img3.save(filename+'3')
 if openid==0: 
  a = imag.crop((0, 0, int(y * 0.5), x))
  b = imag.crop((int(y * 0.5), 0, x, y))
  imag.paste(b, (0, 0))
  imag.paste(a, (int(x * 0.5), 0))
  output_filename = filename
  imag.save(output_filename)
 if openid==1:
  imag=imag.rotate(90)
  a = imag.crop((0, 0, int(y * 0.5), x))
  b = imag.crop((int(y * 0.5), 0, x, y))
  imag.paste(b, (0, 0))
  imag.paste(a, (int(y * 0.5), 0))
  imag=imag.rotate(270)
  output_filename = filename
  imag.save(output_filename)
  
 fig = plt.figure(figsize=(6, 4))
 ax = fig.add_subplot()
 data = np.random.randint(0, 255, (100, 100))
 ax.imshow(imag, cmap='plasma')
 b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
 fig.colorbar(b, ax=ax)
 gr_path = "./static/newgr.png"
 sns.displot(data)
 plt.savefig(gr_path)
 plt.close()
  
 return output_filename,gr_path,img1,img2,img3

@app.route("/net",methods=['GET', 'POST'])
def net():
 form = NetForm()
 filename=None
 newfilename=None
 grname=None
 img1=None
 img2=None
 img3=None
 
 if form.validate_on_submit():
  filename = os.path.join('./static', secure_filename(form.upload.data.filename))
  fcount,fimage=neuronet.read_image_files(10,'./ststic')
  
  ch=form.openid.data
  newfilename,grname,img1,img2,img3 = f(filename,ch)
  
 return render_template('net.html',form=form,image_name=newfilename,gr_name=grname, im1=img1, im2=img2, im3=img3)

if __name__ == "__main__":
 app.run(host='127.0.0.1',port=5000)
