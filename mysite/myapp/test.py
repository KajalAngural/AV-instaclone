from clarifai.rest import ClarifaiApp

app = ClarifaiApp(api_key='a5f07c4b20b84ff8a66790faedaf9314')

model = app.models.get('general-v1.3')
image = ClImage(url='https://samples.clarifai.com/metro-north.jpg')
model.predict([image])