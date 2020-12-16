#pip install jinja2
from fastapi.templating import Jinja2Templates

#pip install googletrans==3.1.0a0
from googletrans import Translator

from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
#pip install python-multipart << baseModel
#from googletrans import Translator

app = FastAPI(debug=True)
templates = Jinja2Templates(directory="template")


@app.get('/')
def form_translate(request: Request):
    text = request.get('input_text')
    selection = request.get('lang_select')
   #json input
    data = jsonable_encoder({'text': text, 'selection': selection})
    return JSONResponse(content=data)

    #template get input
    #return templates.TemplateResponse('translates.html', context={'request': request, 'text': text,'selection' : selection})


@app.post("/")
def form_translate(request: Request, text: str = Form(...),selection: str = Form(...)):

    # connect the translator
    translator = Translator(service_urls=['translate.googleapis.com'])

    # detect input langguage
    dt = translator.detect(text)
    dt2 = dt.lang

    # pronouce input text
    try:
        inputTranslate = translator.translate(text, dest=dt2)
        input_pronouce = inputTranslate.pronunciation
    except:
        input_pronouce=" "

    # translate into output text
    translated = translator.translate(text, dest=selection)
    text_translate = translated.text
    text_pronouce = translated.pronunciation

    # json return
    data = jsonable_encoder( {'text': text, 'selection': selection,'input_pronouce':input_pronouce, 'text_translate': text_translate,'text_pronouce': text_pronouce})
    return JSONResponse(content=data)

    #template post front-end
     #return templates.TemplateResponse('translates.html', context={'request': request, 'text': text,'selection' : selection,'text_translate':text_translate,'text_pronouce':text_pronouce})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)